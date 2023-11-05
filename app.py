from flask import Flask, render_template
from flask_pymongo import PyMongo
    
from flask import Flask, request, jsonify
import numpy as np
import cv2
import easyocr
from ultralytics.yolo.engine.predictor import BasePredictor
from ultralytics.yolo.utils import DEFAULT_CONFIG, ROOT, ops
from ultralytics.yolo.utils.checks import check_imgsz

app = Flask(__name__)
app.config['TEMPLATE_FOLDER']='TEMPLATES'

#setting connection with mongodb
client=pymongo.MongoClient("mongodb+srv://jiyarosejoshy2004:Jiya%4006122004@cluster0.jfpdaiu.mongodb.net/")
db=client["vehicles"]
c1=db["owners"]
c2=db["tickets"]

#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #fetching username and password
        username=request.form.get('username')
        password=request.form.get('password')
        data=c1.find_one({'username':username,'password':password})
        #cross check with c1:
        if data:
            return redirect('/welcome')
        else:
            return render_template('login.html',error='Invalid login credentials')
                
#register
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        phone=request.form.get('phone_number')
        username=request.form.get('username')
        password=request.form.get('password')
        data=c1.find_one({'name':name,'phone_number':phone})
        datas=c1.find_one({'username':username,'password':password})
        #check if data exists 
        if data:
            return redirect('/login')
        elif datas:
            return render_template('register.html',error="Already used login credentials") 
        c1.insert_one({'name':name,'phone_number':phone,'username':username,'password':password})       
        return render_template('welcome.html',name)


# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Load YOLO model
cfg = DEFAULT_CONFIG
cfg.model = "yolov8n.pt"
cfg.imgsz = check_imgsz(cfg.imgsz, min_dim=2)
cfg.source = ROOT / "assets"
predictor = BasePredictor(cfg)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image = request.files['image']
    img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)

    # Process image using YOLO and get detected objects
    preds = predictor.process_image(img)

    # Extract and process OCR from detected objects
    ocr_results = []
    for pred in preds:
        for detection in pred:
            x1, y1, x2, y2, conf, cls = detection
            # Crop and process the region of interest for OCR
            roi = img[int(y1):int(y2), int(x1):int(x2)]
            gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
            results = reader.readtext(gray)
            for result in results:
                if len(result[1]) > 6 and result[2] > 0.2:
                    ocr_results.append(result[1])

    return jsonify({'ocr_results': ocr_results})

@app.route('/store_result',methods=['POST'])
def store_result():
    if request.method=='POST':
        f_result=request.json
        data=c1.find_one({nm:f_result},{name:1,phone_number:1,model:1,_id:0})
        if data:
            c2.insert_one({
                'nm':data[nm],
                'name':data[name],
                'phone_number':data[phone],
                'model':data[model],
                'ticket':1000
            })

@app.route('/api/endpoint',methods=['GET'])
def show_ticket():
    if request.method=='GET':
        data=list(c2.find())
        return render_template('display_data.html',data=data)
            

if __name__ == '__main__':
    app.run(debug=True)    
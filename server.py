from model.predictWithOCR import predict


cfg = { "model" : "", "source": ""}

cfg.model = "./model/best.pt"
cfg.source =  "./model/image1.jpg"
result = predict(cfg)
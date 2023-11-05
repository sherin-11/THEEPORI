import cv2
import numpy as np

def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(canny):
    height, width = canny.shape
    mask = np.zeros_like(canny)
    polygon = np.array([[
        (200, height),
        (800, 350),
        (1200, height),
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image

def houghLines(cropped_canny):
    return cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100,
                           np.array([]), minLineLength=40, maxLineGap=5)

def display_lines(img, lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)
    return line_image

def make_points(image, line):
    slope, intercept = line
    y1 = image.shape[0]
    y2 = int(y1 * 3.0 / 5)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)
    averaged_lines = [left_line, right_line]
    return averaged_lines

# Load the image
image = cv2.imread('sample_ (1).jpg')

# Process the image
canny_image = canny(image)
cropped_canny = region_of_interest(canny_image)
lines = houghLines(cropped_canny)
averaged_lines = average_slope_intercept(image, lines)
line_image = display_lines(image, averaged_lines)

# Overlay the detected lines on the original image
combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)

# Display the processed image
cv2.imshow('Lane Detection', combo_image)

# Wait for a key press and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
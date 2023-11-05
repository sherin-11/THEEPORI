import cv2
import numpy as np

# Load the image
image = cv2.imread('sample_ (1).jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a binary threshold to isolate white lines
_, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image
result_image = image.copy()

# Iterate through the detected contours
for contour in contours:
    # Calculate the contour area
    area = cv2.contourArea(contour)

    # Filter out small contours (adjust the area threshold as needed)
    if area > 100:
        # Draw the contour on the result image
        cv2.drawContours(result_image, [contour], -1, (0, 0, 255), 2)

# Display or save the result image
cv2.imshow('White Lines Detection', result_image)
cv2.imwrite('result_image.jpg', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

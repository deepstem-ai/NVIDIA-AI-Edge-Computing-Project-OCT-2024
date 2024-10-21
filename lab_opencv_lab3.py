# Coding Lab 3: Sharpening Images for Document Scanning
# Situation Story:
# You are working with a document scanning team. When scanning documents,
#  some images are too blurry or lack sharpness, making them difficult to read.
# Your goal is to create a program that
# allows users to sharpen scanned images in real-time to enhance text clarity.
# Task:
# 1. Capture an image from the webcam or load an image of a document.
# 2. Use a trackbar to toggle sharpening on and off.
# 3. Display both the original and sharpened image side by side.

#

import cv2
import numpy as np

# Function to sharpen the image using a kernel
def sharpen_image(image):
    # Define the sharpening kernel
    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, sharpening_kernel)
    return sharpened

# Function to toggle sharpening based on the trackbar
def toggle_sharpening(x):
    sharpen = cv2.getTrackbarPos('Sharpen', 'Sharpen Effect')
    if sharpen == 1:
        sharpened_img = sharpen_image(frame)
    else:
        sharpened_img = frame
    # Combine original and sharpened images side by side
    combined = np.hstack((frame, sharpened_img))
    cv2.imshow('Sharpen Effect', combined)

# Capture video from the webcam or load an image
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Read a frame to initialize the window and trackbars
ret, frame = cap.read()

# Create window to display sharpening effect
cv2.namedWindow('Sharpen Effect')

# Create a trackbar to toggle sharpening (0: Off, 1: On)
cv2.createTrackbar('Sharpen', 'Sharpen Effect', 0, 1, toggle_sharpening)

# Display the original and sharpened images side by side
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break
    
    # Update the window based on the current trackbar value
    toggle_sharpening(0)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

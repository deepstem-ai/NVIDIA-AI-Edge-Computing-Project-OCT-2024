# Coding Lab 2: Creating an Image Editing App for Blur Effect
# Situation Story:
# A local printing company wants to offer customers a blur effect on their photos
# before printing them out.
# You are tasked with creating an application that allows customers to control the
# strength of the blur effect on their photos.
# Task:
# 1. Capture an image from the webcam.
# 2. Use a trackbar to control the blur strength (from 0 to 10).
# 3. Display both the original and blurred images side by side in real-time.

import cv2
import numpy as np

# Function to apply blur effect
def apply_blur(image, ksize):
    if ksize > 0:
        return cv2.GaussianBlur(image, (ksize, ksize), 0)
    else:
        return image

# Function to update blur strength from the trackbar
def update_blur(x):
    blur_strength = cv2.getTrackbarPos('Blur', 'Blur Effect')
    # Ensure that blur kernel size is odd and >= 1
    ksize = max(1, blur_strength * 2 + 1)
    blurred_img = apply_blur(frame, ksize)
    # Combine original and blurred images side by side
    combined = np.hstack((frame, blurred_img))
    cv2.imshow('Blur Effect', combined)

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Read a frame to initialize the windows and trackbars
ret, frame = cap.read()

# Create window to display the blur effect
cv2.namedWindow('Blur Effect')

# Create a trackbar to control the blur strength (0 to 10)
cv2.createTrackbar('Blur', 'Blur Effect', 0, 10, update_blur)

# Display the original and blurred images side by side
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break
    
    # Update the window with the current trackbar value
    update_blur(0)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

# Coding Lab 1: Adjusting Brightness and Contrast for Photography Studio
# Situation Story:
# You work at a photography studio and need to develop a program that automatically adjusts the brightness and contrast of photos taken under different lighting conditions. Some photos are too dark or too bright, and the contrast needs to be adjusted to enhance the quality of the image.
# Your task is to create a program that allows you to manually adjust brightness and contrast using trackbars, so the photographer can fine-tune the image on the spot.
# Task:
# Capture an image from the webcam.
# Create trackbars to adjust brightness (range -50 to +50) and contrast (range 0.5 to 2.0).
# Display the original image and the adjusted image side by side

import cv2
import numpy as np

# Function to adjust brightness and contrast
def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    # Apply brightness and contrast adjustments
    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted

# Function to update the brightness and contrast from trackbars
def update_values(x):
    # Get values from trackbars
    brightness = cv2.getTrackbarPos('Brightness', 'Adjustments') - 50
    contrast = cv2.getTrackbarPos('Contrast', 'Adjustments') / 50.0
    # Apply adjustments
    adjusted_img = adjust_brightness_contrast(frame, brightness, contrast)
    # Combine original and adjusted images side by side
    combined = np.hstack((frame, adjusted_img))
    cv2.imshow('Adjustments', combined)

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Read a frame to initialize the windows and trackbars
ret, frame = cap.read()

# Create window to display adjustments
cv2.namedWindow('Adjustments')

# Create trackbars for brightness and contrast adjustment
cv2.createTrackbar('Brightness', 'Adjustments', 50, 100, update_values)
cv2.createTrackbar('Contrast', 'Adjustments', 50, 100, update_values)

# Display the original and adjusted images side by side
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break
    
    # Update the window with current trackbar values
    update_values(0)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()



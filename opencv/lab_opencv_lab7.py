# Coding Lab 7: Monitoring Elderly Patient’s Movement in Bed Using Motion
# Detection
# Situation Story:
# You are working on a healthcare project to monitor elderly patients who are bedridden. The goal
# is to detect any unusual movements (e.g., if the patient is trying to get out of bed or moving
# excessively), which could indicate discomfort or a potential fall. Your task is to create a program
# that captures video and detects any significant motion. If motion is detected, it will highlight the
# movement.
# Task:
# 1. Capture a video feed from the webcam.
# 2. Implement motion detection by comparing the current frame with the previous frame.
# 3. If significant movement is detected, highlight the area of motion.
# 4. Display both the original frame and a motion-highlighted frame side by side.

import cv2
import numpy as np

# Function to detect and highlight motion
def detect_motion(prev_frame, current_frame):
    # Convert both frames to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to both frames to reduce noise
    prev_blur = cv2.GaussianBlur(prev_gray, (21, 21), 0)
    current_blur = cv2.GaussianBlur(current_gray, (21, 21), 0)

    # Compute the absolute difference between the previous and current frames
    diff_frame = cv2.absdiff(prev_blur, current_blur)

    # Threshold the difference to get the regions with significant motion
    _, thresh_frame = cv2.threshold(diff_frame, 25, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded frame to fill in gaps
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contours of the motion
    contours, _ = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and highlight areas with significant motion
    motion_frame = current_frame.copy()
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            # Ignore small movements to reduce noise
            continue
        # Get the bounding box for the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # Draw a rectangle around the motion area
        cv2.rectangle(motion_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return motion_frame

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Read the first frame to initialize the previous frame
ret, prev_frame = cap.read()
if not ret:
    print("Error: Could not read video feed")
    exit()

# Create a window for displaying the monitoring feed
cv2.namedWindow('Motion Detection', cv2.WINDOW_NORMAL)

# Main loop to process the video feed
while True:
    # Capture the current frame
    ret, current_frame = cap.read()
    if not ret:
        break

    # Detect motion and highlight the areas
    motion_highlighted_frame = detect_motion(prev_frame, current_frame)

    # Combine the original and motion-highlighted frames side by side
    combined_frame = np.hstack((current_frame, motion_highlighted_frame))

    # Display the combined frames
    cv2.imshow('Motion Detection', combined_frame)

    # Update the previous frame to the current frame for the next iteration
    prev_frame = current_frame

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

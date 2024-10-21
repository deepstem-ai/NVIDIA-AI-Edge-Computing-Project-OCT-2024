# Coding Lab 12: Real-Time Medical Gesture Recognition for Robotic Surgery Assistance
# Situation Story:
# In robotic-assisted surgeries, doctors may use gestures to control surgical robots without touching any devices (e.g., to maintain sterility). You are developing a system to detect and recognize hand gestures in real-time that can be used to issue commands to a surgical robot.
# Task:
# Capture a video feed from the webcam.
# Detect hand gestures using contour detection and convexity defects.
# Recognize a simple gesture (e.g., the number of raised fingers) and display the gesture in real-time.
# Optionally, send the recognized gesture as a command to control a robotic surgery assistant.


import cv2
import numpy as np
import math

# Function to detect hand gestures based on contours and convexity defects
def detect_gesture(frame, contour):
    # Create a convex hull around the hand
    hull = cv2.convexHull(contour)
    
    # Draw the convex hull around the hand
    cv2.drawContours(frame, [hull], -1, (0, 255, 0), 2)

    # Calculate convexity defects
    hull_indices = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull_indices)

    # Count the number of raised fingers (based on convexity defects)
    finger_count = 0

    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])

            # Calculate the angle between the fingers using the cosine rule
            a = math.dist(start, end)
            b = math.dist(start, far)
            c = math.dist(end, far)
            angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c))

            # If the angle is less than 90 degrees, we consider it a finger
            if angle <= math.pi / 2:
                finger_count += 1
                cv2.circle(frame, far, 5, [0, 0, 255], -1)

    # The number of raised fingers is finger_count + 1 (because of the thumb)
    finger_count += 1

    # Display the detected number of fingers
    cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    return frame, finger_count

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Create a window to display the gesture recognition feed
cv2.namedWindow('Gesture Recognition', cv2.WINDOW_NORMAL)

# Main loop to process the video feed
while True:
    # Capture the current frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale and apply Gaussian blur
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame, (35, 35), 0)

    # Threshold the image to segment the hand
    _, thresh_frame = cv2.threshold(blur_frame, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If any contours are found, detect gestures
    if len(contours) > 0:
        # Find the largest contour, which is assumed to be the hand
        max_contour = max(contours, key=cv2.contourArea)

        # Detect hand gestures
        frame, finger_count = detect_gesture(frame, max_contour)

        # Optionally, send the detected gesture to control the robotic surgery assistant
        # robotic_surgery_assistant.execute_command(finger_count)

    # Display the frame with the gesture recognition
    cv2.imshow('Gesture Recognition', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

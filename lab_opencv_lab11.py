# Coding Lab 11: Real-Time Object Tracking for Robotic Arm Control
# Situation Story:
# You are working on a robotics project where a robotic arm needs to follow and pick up an object (e.g., a ball or block) that moves within the camera's field of view. Your task is to create a program that tracks a specific colored object in real-time and provides feedback to control the movement of the robotic arm.
# Task:
# Capture a video feed from the webcam.
# Implement color-based object tracking using HSV color space (e.g., tracking a blue object).
# Display the video feed with the tracked object highlighted, and show the real-time coordinates of the object.
# Optionally, send the coordinates of the object to a robotic arm control system for movement adjustments.


import cv2
import numpy as np

# Function to track a specific color (e.g., blue) and return the coordinates of the object
def track_object(frame, hsv_lower, hsv_upper):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the object based on the specified HSV range
    mask = cv2.inRange(hsv_frame, hsv_lower, hsv_upper)

    # Find contours of the masked object
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize the center coordinates of the object
    object_center = None

    # If any contours are found, process the largest one
    if len(contours) > 0:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding box coordinates for the largest contour
        (x, y, w, h) = cv2.boundingRect(largest_contour)

        # Draw a rectangle around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the center of the object
        object_center = (int(x + w / 2), int(y + h / 2))

        # Draw a circle at the center of the object
        cv2.circle(frame, object_center, 5, (255, 0, 0), -1)

        # Display the object's coordinates on the frame
        cv2.putText(frame, f"Coordinates: {object_center}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame, object_center

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Define the HSV range for the object color (e.g., blue)
hsv_lower = np.array([100, 150, 50])  # Lower bound for blue color
hsv_upper = np.array([140, 255, 255])  # Upper bound for blue color

# Create a window to display the tracking feed
cv2.namedWindow('Object Tracking', cv2.WINDOW_NORMAL)

# Main loop to process the video feed
while True:
    # Capture the current frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Track the object based on the specified color
    frame, object_center = track_object(frame, hsv_lower, hsv_upper)

    # Display the frame with the tracked object
    cv2.imshow('Object Tracking', frame)

    # Optionally, send the object's coordinates to the robotic arm control system
    if object_center:
        # Send object_center coordinates to the robotic arm system (pseudo-code)
        # robotic_arm.move_to(object_center)
        pass

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

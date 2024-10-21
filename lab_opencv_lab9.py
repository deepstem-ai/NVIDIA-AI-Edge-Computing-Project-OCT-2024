# Coding Lab 9: Real-Time People Counter for Visitor Tracking
# Situation Story:
# You are developing a visitor counting system for a museum. The goal is to track how many people walk past a designated area (e.g., an entrance or hallway) using a webcam. The system should count each person that crosses the frame and update the visitor count in real-time. This system could help museum staff keep track of the number of visitors during the day.
# Task:
# Capture a video feed from the webcam.
# Use OpenCV’s object detection to detect people walking past the camera.
# Count and display the number of people detected as they walk through a specific region (e.g., a line on the screen).
# Display the real-time video feed with the count overlayed on the screen.

import cv2

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Initialize variables
visitor_count = 0
crossing_line = 250  # Line on the screen that people must cross
frame_count = 0      # To track frames for detection frequency

# Function to detect people and update the count
def detect_people(frame, visitor_count):
    global crossing_line

    # Resize the frame for faster processing
    frame_resized = cv2.resize(frame, (640, 480))

    # Detect people in the frame
    rects, _ = hog.detectMultiScale(frame_resized, winStride=(8, 8), padding=(16, 16), scale=1.05)

    # Draw a horizontal line where people will be counted
    cv2.line(frame_resized, (0, crossing_line), (640, crossing_line), (0, 255, 255), 2)

    # Loop over the detected people
    for (x, y, w, h) in rects:
        # Draw rectangles around detected people
        cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Check if the person has crossed the counting line
        if y + h > crossing_line:
            visitor_count += 1
            # Adjust the crossing line temporarily to avoid multiple counts for the same person
            crossing_line += 50

    # Reset crossing line to original position for future frames
    crossing_line = 250

    return frame_resized, visitor_count

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Create a window for displaying the real-time visitor count
cv2.namedWindow('Visitor Counter', cv2.WINDOW_NORMAL)

# Main loop to process the video feed
while True:
    # Capture the current frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Only run detection every 5 frames to reduce processing load
    if frame_count % 5 == 0:
        # Detect people and update the visitor count
        frame, visitor_count = detect_people(frame, visitor_count)

    # Display the visitor count on the frame
    cv2.putText(frame, f"Visitors: {visitor_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display the frame with the visitor count
    cv2.imshow('Visitor Counter', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()



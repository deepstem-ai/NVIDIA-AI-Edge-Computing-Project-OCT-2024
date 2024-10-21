# Coding Lab 8: Real-Time Attention Monitoring in the Classroom Using Face
# Detection
# Situation Story:
# You are developing a tool to help teachers monitor students' attention during a lecture. The
# system will use a webcam to detect students' faces in real-time. If a student's face is not
# detected for a certain period, it will be highlighted, indicating that the student might not be
# paying attention (e.g., looking away or leaving the seat).
# Task:
# 1. Capture a video feed from the webcam.
# 2. Use OpenCV's face detection to track the presence of students' faces.
# 3. If no face is detected for a few seconds, highlight the absence by drawing a red box
# where the face should be.
# 4. Display both the original video feed and a status frame that shows whether each
# student's face is detected.

import cv2
import time

# Load the pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to check face detection and monitor attention
def monitor_attention(frame, last_seen_time, face_position, attention_threshold=2):
    # Convert frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the current frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If faces are detected, update the last seen time and position
    if len(faces) > 0:
        last_seen_time = time.time()
        face_position = faces[0]  # Assuming one face, update the position

        # Draw a green rectangle around the detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # If no face is detected, check how long it's been since the last face was seen
    else:
        elapsed_time = time.time() - last_seen_time

        # If the face hasn't been seen for a certain threshold, highlight absence
        if elapsed_time > attention_threshold:
            # Draw a red rectangle where the face was last seen
            (x, y, w, h) = face_position
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "No Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return frame, last_seen_time, face_position

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for face tracking
last_seen_time = time.time()
face_position = (0, 0, 0, 0)  # Initialize with no face position

# Create a window for displaying the attention monitoring feed
cv2.namedWindow('Attention Monitoring', cv2.WINDOW_NORMAL)

# Main loop to process the video feed
while True:
    # Capture the current frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Monitor attention using face detection
    frame, last_seen_time, face_position = monitor_attention(frame, last_seen_time, face_position)

    # Display the frame with attention monitoring
    cv2.imshow('Attention Monitoring', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Coding Lab 10: Real-Time Eye Masking for People Walking or Running By
# Situation Story:
# You are tasked with developing a privacy-preserving surveillance system where people's eyes are automatically masked when they walk or run past a camera. The goal is to maintain privacy by obscuring the eyes of people detected in real-time using computer vision techniques.
# Task:
# Capture a video feed from the webcam.
# Detect people’s faces as they walk or run by the camera.
# Automatically detect the eyes and apply a black mask over them.
# Display the video feed with the masked eyes in real-time.


import cv2

# Load the pre-trained face and eye detection Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to mask eyes in detected faces
def mask_eyes(frame, faces):
    # Loop over each detected face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face (optional, for debugging or display purposes)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Get the region of interest (ROI) for the face
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Loop over the detected eyes
        for (ex, ey, ew, eh) in eyes:
            # Mask the eyes by drawing black rectangles over them
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 0), -1)

    return frame

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Create a window for displaying the video feed with masked eyes
cv2.namedWindow('Eye Masking', cv2.WINDOW_NORMAL)

# Main loop to process the video feed
while True:
    # Capture the current frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for face and eye detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Mask the eyes in the detected faces
    frame_with_masks = mask_eyes(frame, faces)

    # Display the frame with masked eyes
    cv2.imshow('Eye Masking', frame_with_masks)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

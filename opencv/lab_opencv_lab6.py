# Coding Lab 6: Stress Detection Using Color Changes in a Person’s Face
# Situation Story:
# You are working on a stress management project where you aim to monitor a
# person's stress levels based on changes in facial color (e.g., redness in the face,
# which may indicate stress or anxiety). You are tasked with building a program
# that captures a video feed, identifies the face, and allows you to enhance the red
# channel of the image to detect changes in skin tone.
# Task:
# 1. Capture a video feed from the webcam.
# 2. Detect a face in the video stream using OpenCV’s face detection.
# 3. Use a trackbar to enhance the red color in the detected face region,
# simulating stress detection.
# 4. Display the original and enhanced images side by side.


import cv2
import numpy as np

# Load the pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to enhance the red channel of the detected face region
def enhance_red_channel(image, enhancement_value):
    # Convert image to RGB (OpenCV reads images as BGR by default)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Split the image into its color channels
    r, g, b = cv2.split(img_rgb)

    # Enhance the red channel by adding the enhancement value
    r = cv2.add(r, enhancement_value)

    # Merge the channels back together
    enhanced_img = cv2.merge([r, g, b])

    # Convert back to BGR format for displaying with OpenCV
    enhanced_img_bgr = cv2.cvtColor(enhanced_img, cv2.COLOR_RGB2BGR)

    return enhanced_img_bgr

# Function to update the red enhancement using the trackbar
def update_red_enhancement(val):
    global frame
    enhancement_value = cv2.getTrackbarPos('Red Enhancement', 'Stress Detection')

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    # Create a copy of the original frame to enhance red channel only on faces
    frame_copy = frame.copy()

    # Loop through all detected faces
    for (x, y, w, h) in faces:
        # Extract the face region from the original frame
        face_roi = frame_copy[y:y+h, x:x+w]

        # Enhance the red channel of the face region
        enhanced_face = enhance_red_channel(face_roi, enhancement_value)

        # Replace the face region in the frame with the enhanced face
        frame_copy[y:y+h, x:x+w] = enhanced_face

    # Combine original and enhanced images side by side
    combined_frame = np.hstack((frame, frame_copy))

    # Display the combined image
    cv2.imshow('Stress Detection', combined_frame)

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Create a window for displaying the stress detection
cv2.namedWindow('Stress Detection', cv2.WINDOW_NORMAL)

# Create a trackbar to control the red enhancement value
cv2.createTrackbar('Red Enhancement', 'Stress Detection', 0, 100, update_red_enhancement)

# Main loop to process the video feed
while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()

    # If frame was not captured successfully, exit the loop
    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Update the red enhancement
    update_red_enhancement(0)

    # Exit the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

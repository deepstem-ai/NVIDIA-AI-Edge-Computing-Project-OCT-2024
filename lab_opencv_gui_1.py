import cv2
import numpy as np

# Function to adjust brightness and contrast
def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

# Function to apply smoothing (blurring)
def apply_smoothing(image, blur_strength=1):
    if blur_strength > 0:
        return cv2.GaussianBlur(image, (2 * blur_strength + 1, 2 * blur_strength + 1), 0)
    else:
        return image

# Function to apply sharpening
def apply_sharpening(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

# Callback functions for trackbars (dummy function, trackbars will update via getTrackbarPos)
def on_trackbar_change(val):
    pass

# Setup the OpenCV window with trackbars
cv2.namedWindow('Adjustments')

# Create trackbars for brightness, contrast, blur strength, and sharpening
cv2.createTrackbar('Brightness', 'Adjustments', 50, 100, on_trackbar_change)  # Default brightness 50
cv2.createTrackbar('Contrast', 'Adjustments', 10, 30, on_trackbar_change)     # Default contrast 10 (mapped to 1.0)
cv2.createTrackbar('Blur', 'Adjustments', 0, 10, on_trackbar_change)          # Blur strength from 0 (off) to 10
cv2.createTrackbar('Sharpen', 'Adjustments', 0, 1, on_trackbar_change)        # Sharpen off (0) or on (1)

# Start capturing video from camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image. Exiting...")
        break

    # Get the values from the trackbars
    brightness = cv2.getTrackbarPos('Brightness', 'Adjustments') - 50   # Adjust brightness (-50 to 50)
    contrast = cv2.getTrackbarPos('Contrast', 'Adjustments') / 10.0     # Adjust contrast (0.1 to 3.0)
    blur_strength = cv2.getTrackbarPos('Blur', 'Adjustments')           # Blur strength (0 to 10)
    sharpen = cv2.getTrackbarPos('Sharpen', 'Adjustments')              # Sharpen (0 or 1)

    # Adjust brightness and contrast
    adjusted_image = adjust_brightness_contrast(frame, brightness, contrast)

    # Apply blur (smoothing)
    smoothed_image = apply_smoothing(adjusted_image, blur_strength)

    # Apply sharpening if requested
    if sharpen == 1:
        output_image = apply_sharpening(smoothed_image)
    else:
        output_image = smoothed_image

    # Display original and adjusted images side by side
    combined_image = np.hstack((frame, output_image))
    cv2.imshow('Original (Left) | Adjusted (Right)', combined_image)

    # Wait for key press
    key = cv2.waitKey(1)

    # Press 's' to save both the original and processed images
    if key == ord('s'):
        cv2.imwrite('original_image.png', frame)
        cv2.imwrite('adjusted_image.png', output_image)
        print("Images saved as original_image.png and adjusted_image.png")

    # Press 'q' to exit the loop
    if key == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

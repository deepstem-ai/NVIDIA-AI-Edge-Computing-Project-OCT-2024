import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

# Function to apply a blur filter to reduce noise
def apply_blur(image, ksize):
    # If the kernel size is greater than 1, apply GaussianBlur
    if ksize > 1:
        return cv2.GaussianBlur(image, (ksize, ksize), 0)
    else:
        # If kernel size is 1, return the original image (no blurring)
        return image

# Function to update the blur strength using the trackbar
def update_blur(val):
    # Get the blur strength value from the trackbar
    blur_strength = cv2.getTrackbarPos('Blur Strength', 'Noise Reduction')

    # Ensure that the kernel size is odd and greater than or equal to 3
    ksize = blur_strength * 2 + 1 if blur_strength > 0 else 1

    # Apply the blur to reduce noise
    blurred_img = apply_blur(frame_resized.copy(), ksize)

    # Combine the original and blurred images side by side for comparison
    combined = np.hstack((frame_resized, blurred_img))

    # Display the combined image
    cv2.imshow('Noise Reduction', combined)

# Function to open a file dialog to select an ultrasound image
def get_image_path():
    # Initialize the Tkinter root and hide the main window
    root = Tk()
    root.withdraw()

    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(title="Select an Ultrasound Image", 
                                           filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")])

    # Destroy the Tkinter root window
    root.destroy()

    # Return the selected file path
    return file_path

# Function to resize image to fit a window size limit
def resize_image(image, max_width=600, max_height=600):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        return cv2.resize(image, (int(width * scaling_factor), int(height * scaling_factor)))
    return image

# Ask the user to select an ultrasound image file
file_path = get_image_path()

# Check if the selected file exists and load the image
if os.path.exists(file_path):
    # Load the image in grayscale mode
    frame = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded successfully
    if frame is None:
        print("Error: Could not load image")
        exit()
else:
    # If no file was selected or file not found, exit
    print("Error: No file selected or file not found")
    exit()

# Resize the image to fit within the window
frame_resized = resize_image(frame)

# Create a window to display the noise reduction effect
cv2.namedWindow('Noise Reduction', cv2.WINDOW_NORMAL)

# Create a trackbar to control the blur strength (0 to 10)
cv2.createTrackbar('Blur Strength', 'Noise Reduction', 0, 10, update_blur)

# Display the initial image
update_blur(0)

# Display the original and noise-reduced images side by side
while True:
    # Wait for user input to adjust the trackbar and update the window
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release all OpenCV windows
cv2.destroyAllWindows()

import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

# Function to adjust brightness and contrast
def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    # Apply brightness and contrast adjustments
    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted

# Function to update brightness and contrast from trackbars
def update_values(x):
    # Get values from trackbars
    brightness = cv2.getTrackbarPos('Brightness', 'Adjustments') - 50
    contrast = cv2.getTrackbarPos('Contrast', 'Adjustments') / 50.0
    # Apply adjustments
    adjusted_img = adjust_brightness_contrast(frame, brightness, contrast)
    # Combine original and adjusted images side by side
    combined = np.hstack((frame, adjusted_img))
    cv2.imshow('Adjustments', combined)

# Function to open a file dialog for image selection
def get_image_path():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select an X-ray Image", 
                                           filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
    root.destroy()
    return file_path

# Ask user to select an image file
file_path = get_image_path()

# Load the selected image
if os.path.exists(file_path):
    frame = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if frame is None:
        print("Error: Could not load image")
        exit()
else:
    print("Error: No file selected or file not found")
    exit()

# Create window to display adjustments
cv2.namedWindow('Adjustments')

# Create trackbars for brightness and contrast adjustment
cv2.createTrackbar('Brightness', 'Adjustments', 50, 100, update_values)
cv2.createTrackbar('Contrast', 'Adjustments', 50, 100, update_values)

# Display the original and adjusted images side by side
while True:
    # Update the window with the current trackbar values
    update_values(0)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

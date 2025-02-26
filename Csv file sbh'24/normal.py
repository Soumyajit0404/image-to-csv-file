import cv2
from PIL import Image
from pytesseract import pytesseract
import matplotlib.pyplot as plt
import os

# Define the directory path
directory = "D:\\Hackathon\\"

# Function to add taskbar text on the image
def add_taskbar(image):
    text = "Press 's' to save, 'q' to quit"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = int((image.shape[1] - text_size[0]) / 2)
    text_y = image.shape[0] - 10
    cv2.putText(image, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

# Access camera
camera = cv2.VideoCapture(1)

# Loop for camera access
while True:
    _, image = camera.read()
    cv2.imshow('Text detection', image)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('s'):  # Press 's' to save the image and exit
        cv2.imwrite(os.path.join(directory, 'test1.jpg'), image)
        break
    elif key & 0xFF == ord('q'):  # Press 'q' to exit camera access
        break

# Release camera and close window
camera.release()
cv2.destroyAllWindows()

# Function to convert image to black and white
def convert_to_bw(input_image_path, output_bw_path):
    # Load the image
    img = cv2.imread(input_image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding for black and white conversion
    _, im_bw = cv2.threshold(gray_image, 160, 200, cv2.THRESH_BINARY)

    # Save the black and white image
    cv2.imwrite(output_bw_path, im_bw)

    # Display the black and white image
    plt.imshow(im_bw, cmap='gray')
    plt.axis('off')
    plt.title('Black and White Image')
    plt.show()

# Call convert_to_bw function with updated file paths
convert_to_bw(os.path.join(directory, 'test1.jpg'), os.path.join(directory, 'bw_output.jpg'))

# Function to perform OCR using Tesseract
def tesseract():
    # Set path to Tesseract executable
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path = os.path.join(directory, 'bw_output.jpg')

    # Configure pytesseract
    pytesseract.tesseract_cmd = path_to_tesseract

    # Perform OCR and print the detected text
    text = pytesseract.image_to_string(Image.open(image_path))
    print(text[:-1])  # Print without the last character (usually a newline)

# Call tesseract function
tesseract()

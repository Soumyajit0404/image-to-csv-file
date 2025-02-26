import cv2
from PIL import Image
from pytesseract import pytesseract
import matplotlib.pyplot as plt
import os
from google.cloud import vision

# Define the directory path
directory = ("C:\\Users\\Sangbed\\Desktop\\New folder\\Hackathon\\")

def add_taskbar(image):
    text = "Press 's' to save, 'q' to quit"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = int((image.shape[1] - text_size[0]) / 2)
    text_y = image.shape[0] - 10
    cv2.putText(image, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

camera = cv2.VideoCapture(1)

while True:
    _, image = camera.read()
    add_taskbar(image)
    cv2.imshow('Text detection', image)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('s'):
        cv2.imwrite(os.path.join(directory, 'test1.jpg'), image)
        break
    elif key & 0xFF == ord('q'):  # Press 'q' to exit the camera access
        break
camera.release()
cv2.destroyAllWindows()

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

# Call convert_to_bw function with file paths
convert_to_bw(os.path.join(directory, 'test1.jpg'), os.path.join(directory, 'bw_output.jpg'))

def tesseract():
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path = os.path.join(directory, 'bw_output.jpg')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Sangbed\Desktop\New folder\Hackathon\text-recognition-418918-5e1733e20694.json'
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Performs text detection on the image
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Print detected text
    for text in texts:
        print('\n"{}"'.format(text.description))

# Call tesseract function
tesseract()

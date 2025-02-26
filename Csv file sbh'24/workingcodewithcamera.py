import cv2
import pytesseract
import csv
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Initialize the camera
camera = cv2.VideoCapture(1)

while True:
    _, image = camera.read()
    cv2.imshow('Text detection', image)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('test1.jpg', image)
        
        # Perform OCR on the captured image
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img)

        # Split text into sentences based on full stops
        sentences = re.split(r'\.\s*', text)

        # Save the recognized text to a CSV file
        with open('recognized_text.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for sentence in sentences:
                csvwriter.writerow([sentence])

        # Print the recognized text
        print("Recognized text:")
        for sentence in sentences:
            print(sentence)

        # Display the image with bounding boxes
        hImg, wImg, _ = img.shape
        boxes = pytesseract.image_to_boxes(img)
        for b in boxes.splitlines():
            b = b.split()
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 3)
            cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

        cv2.imshow('Result', img)
        cv2.waitKey(0)
        
        break
        
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the camera access
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()

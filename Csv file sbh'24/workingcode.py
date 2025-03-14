import cv2
import pytesseract
import csv


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def detect_new_lines(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform OCR
    text = pytesseract.image_to_string(img)
    words = text.split()

    # Save the recognized text to a CSV file
    with open('recognized_text.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for word in words:
            if word == '<nl>':  # New line token detected
                csvwriter.writerow([])  # Write an empty row
            else:
                csvwriter.writerow([word + ','])  # Add comma after each word

    # Print the recognized text
    print("Recognized text:")
    for word in words:
        if word == '<nl>':  # New line token detected
            print()  # Print an empty line
        else:
            print(word, end=', ')  # Print each word with a comma after it

    # Display the image with bounding boxes
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 3)
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 1)

    cv2.imshow('Result', img)
    cv2.waitKey(0)

# Example usage:
detect_new_lines('test2.jpg')

import cv2
import pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def split_into_columns(text, words_per_column):
    words = text.split()
    num_words = len(words)
    num_columns = (num_words + words_per_column - 1) // words_per_column
    columns = [words[i:i+words_per_column] for i in range(0, num_words, words_per_column)]
    return columns, num_columns

def detect_new_lines(image_path, words_per_column=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform OCR
    text = pytesseract.image_to_string(img)

    # Split text into columns
    columns, num_columns = split_into_columns(text, words_per_column)

    # Create a DataFrame from the columns
    df = pd.DataFrame(columns)

    # Write the DataFrame to a CSV file
    df.to_csv('recognized_text.csv', index=False, header=False)

    print(f"CSV file 'recognized_text.csv' has been created with {num_columns} columns, each containing {words_per_column} words.")

    # Display the image with bounding boxes
    hImg, wImg, _ = img.shape
    cv2.imshow('Result', img)
    cv2.waitKey(0)

# Example usage:
detect_new_lines('test2.jpg', words_per_column=5)

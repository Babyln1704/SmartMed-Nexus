import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread("prescription.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

text = pytesseract.image_to_string(gray)

print("Raw OCR Text:")
print(text)

lines = [line.strip() for line in text.split('\n') if line.strip()]

if len(lines) >= 3:
    print("\nExtracted Information")
    print("Medicine:", lines[0])
    print("Dose:", lines[1])
    print("Frequency:", lines[2])
else:
    print("Could not extract complete information")
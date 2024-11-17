import cv2
from pytesseract import image_to_string

image = cv2.imread('IMG_8008.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite('preprocessed_IMG_8008.png', thresh_image)
text = image_to_string(thresh_image)

print("Extracted Text after preprocessing:")
print(text)
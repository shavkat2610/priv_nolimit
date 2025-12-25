import pytesseract
import cv2
import time
from PIL import Image

# # If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'D:/Programme/tesseract/tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'


custom_oem_psm_config = r'--oem 0 '

print()


# measure time
start = time.time()
img2 = cv2.imread('row.png',)
# im = Image.open('A.png')
end = time.time()
print(end - start)

# print("type of img2: "+str(type(img2)))
# im = im


# img2 = img2.crop((3, 20, 100, 100))
# img2.show()


start = time.time()
data = pytesseract.image_to_string(img2)
end = time.time()
print(end - start)

print()

print(data)
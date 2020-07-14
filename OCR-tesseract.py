# import the necessary packages
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  
import argparse
import cv2
import os
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
	help="path to IC image")

ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="can add other preprocessing later if thresh not ok")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	# gray = cv2.threshold(gray, 0, 255,
	# 	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    gray = cv2.threshold(gray, 127, 255,
      cv2.THRESH_TRUNC)[1]

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)
# show the output images
cv2.imshow("Original IC", image)
cv2.imshow("preprocessed IC", gray)
cv2.waitKey(0)

#  C:\Program Files\Tesseract-OCR
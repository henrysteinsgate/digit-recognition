import cv2
import argparse as ap
import numpy as np

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Load the image
img = cv2.imread(args["image"])

# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_blurred_bilateral = cv2.bilateralFilter(img, 9, 10, 100)

edges = cv2.Canny(img_blurred_bilateral, 200, 300)

cv2.imshow("Original", img)
cv2.waitKey()

cv2.imshow("bilateral", img_blurred_bilateral)
cv2.waitKey()

cv2.imshow("edges", edges)
cv2.waitKey()
import cv2
import argparse as ap
import numpy as np

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Load the image
img = cv2.imread(args["image"])
img = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blurred = cv2.medianBlur(gray, 7)
# thresh = cv2.threshold(img_blurred, 95, 255, cv2.THRESH_BINARY)[1]
# thresh = cv2.bitwise_not(thresh)
#
# kernel = np.ones((5,5),np.uint8)
# dilate = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

edges = cv2.Canny(img_blurred, 200, 300)

# for bitwise_or the shape needs to be the same, so we need to add an axis,
# since our input image has 3 axis while the canny output image has only one 2 axis
out = np.bitwise_or(img, edges[:, :, np.newaxis])

cv2.imshow("Original", img)
cv2.waitKey()

cv2.imshow("Edges Labeled", edges)
cv2.waitKey()
cv2.destroyAllWindows()

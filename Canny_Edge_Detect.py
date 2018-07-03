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

# Result using OpenCV Canny Edge
edges = cv2.Canny(img_blurred, 200, 300)


# for bitwise_or the shape needs to be the same, so we need to add an axis,
# since our input image has 3 axis while the canny output image has only one 2 axis
out = np.bitwise_or(img, edges[:, :, np.newaxis])

cv2.imshow("Original", img)
cv2.waitKey()

cv2.imshow("OpenCV", edges)
cv2.waitKey()

cv2.destroyAllWindows()

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

img_blurred_bilateral = cv2.bilateralFilter(img, 20, 50, 50)

edges = cv2.Canny(img_blurred_bilateral, 200, 300)

lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

out = np.bitwise_or(img, edges[:, :, np.newaxis])

cv2.imshow("Original", img)
cv2.waitKey()

cv2.imshow("edges", edges)
cv2.waitKey()

cv2.imshow("Output", out)
cv2.waitKey()
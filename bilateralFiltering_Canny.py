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
#
# img_blurred_bilateral = cv2.bilateralFilter(img, 20, 50, 50)
# edges = cv2.Canny(img_blurred_bilateral, 200, 300)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)


# lines = cv2.HoughLines(edges, 1, np.pi/180, 10)
#
# for line in lines:
#     for rho, theta in line:
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 1000 * (-b))
#         y1 = int(y0 + 1000 * (a))
#         x2 = int(x0 - 1000 * (-b))
#         y2 = int(y0 - 1000 * (a))
#
#         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

#########################
# Produce a image with labeled lines
height, width, channel = img.shape
blank_image = np.zeros((height, width, channel), np.uint8)

#########################
# 18 8 20

lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30, minLineLength=40, maxLineGap=10)

line_cnt = 1
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.line(blank_image, (x1, y1), (x2, y2), (255, 255, 255), 1)

        # Label Line Recognized
        center_x = (x1 + x2)/2
        center_y = (y1 + y2)/2
        cv2.putText(img, str(line_cnt), (center_x, center_y), cv2.FONT_HERSHEY_DUPLEX, 0.5 , (0, 255, 255), 1)

    line_cnt = line_cnt + 1


########################################################################

# Fill out incomplete Rectangle
canvas = blank_image.copy()
kernel = np.ones((8,8),np.uint8)
erosion = cv2.erode(canvas,kernel,iterations=10)
dilate = cv2.dilate(erosion,kernel,iterations=10)

cv2.imshow("Post-Processinged Image", canvas)
cv2.waitKey()

# out = np.bitwise_or(img, edges[:, :, np.newaxis])

# cv2.imshow("Original", img)
# cv2.waitKey()

cv2.imshow("edges", edges)
cv2.waitKey()

cv2.imshow("Output", img)
cv2.waitKey()
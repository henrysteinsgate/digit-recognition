import cv2
import argparse as ap
import numpy as np
from sympy import Symbol, solve
import math


#########################################################
#########################################################
# TODO: Make the following method and class a separate file and import it as module
# Check intersection of two points, if there is return the
# point, angle, and True; if not, return none and False
def check_intersect(line_1, line_2):
    # Endpoints of the first line
    pt1 = (line_1[0], line_1[0])
    pt2 = (line_1[2], line_1[3])
    # Endpoints of the first line
    pt3 = (line_2[0], line_2[0])
    pt4 = (line_2[2], line_2[3])

    m1 = (pt2[1] - pt1[1]) // (pt2[0] - pt1[0])
    b1 = pt1[1] - pt1[0] // m1

    m2 = (pt4[1] - pt3[1]) // (pt4[0] - pt3[0])
    b2 = pt3[1] - pt3[0] // m2

    x = Symbol('x')
    solution = solve((m1 - m2) * x + b1 - b2, x)

    if len(solution) != 1:
        return None, None, None, False
    else:
        print("Solution is " + str(solution))

        x_intersect = int(solution[0])
        y_intersect = int(m1 * solution[0] + b1)
        # TODO Check the following algorithm, due to coordinate frame might affect calculation
        theta1 = math.atan(m1)
        theta2 = math.atan(m2)
        theta = int(math.degrees(theta2 - theta1))
        print("Theta is " + str(theta))
        # if (theta < 100 and theta > 80) or (theta > -100 and theta < -80):
        #     return x_intersect, y_intersect, theta, True
        # else:
        #     return None, None, None, False
        return x_intersect, y_intersect, theta, True


def extend_line(line):
    x1, y1, x2, y2 = line[0]
    length = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    # TODO: Adjust the following threshold to pass the lines
    threshold = 40
    if length < threshold:
        return line
    else:
        # TODO: Extends to about 1.4 of its original length, might need change ratio
        ratio = 0.2
        delta_x = int((x2 - x1) * ratio)
        delta_y = int((y2 - y1) * ratio)

        extended = [x1 - delta_x, y1 - delta_x, x2 + delta_x, y2 + delta_y]
        return [extended]


class Intersect:
    def __init__(self, x_intersect, y_intersect, theta):
        self.x = x_intersect
        self.y = y_intersect
        self.theta = theta


######################################################################
######################################################################

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

#########################
# Produce a image with labeled lines
height, width, channel = img.shape
blank_image = np.zeros((height, width, channel), np.uint8)

#########################
# Threshold Value: 18 8 20

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=40, maxLineGap=10)

line_cnt = 1
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.line(blank_image, (x1, y1), (x2, y2), (255, 255, 255), 2)

        # Label Line Recognized
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        cv2.putText(img, str(line_cnt), (center_x, center_y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255), 1)

    line_cnt = line_cnt + 1

########################################################################
# Extend the lines if they are too short
ext_lines = []
for line in lines.copy():
    new_line = extend_line(line)
    ext_lines.append(new_line)
    # Draw Lines after extension
    cv2.line(img, (new_line[0][0], new_line[0][1]), (new_line[0][2], new_line[0][3]), (0, 0, 255), 2)

intersections = []

# i, j prevent from checking two same lines' intersection
i, j = 0, 0
for line_1 in ext_lines:
    for line_2 in ext_lines:
        if i != j:
            x_center, y_center, theta, found = check_intersect(line_1[0], line_2[0])
            if found:
                print("Found intersection")
                new_point = Intersect(x_center, y_center, theta)
                intersections.append(new_point)
        j = j + 1
    i = i + 1

if len(intersections) == 0:
    print("There is no intersection points")

# Label all the intersections
for point in intersections:
    cv2.circle(img, (point.x, point.y), 7, (255, 255, 255), -1)
#########################################################################

# Fill out incomplete Rectangle
canvas = blank_image.copy()
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(canvas, kernel, iterations=20)
dilate = cv2.dilate(erosion, kernel, iterations=20)

cv2.imshow("Post-Processinged Image", canvas)
cv2.waitKey()

# out = np.bitwise_or(img, edges[:, :, np.newaxis])

# cv2.imshow("Original", img)
# cv2.waitKey()

cv2.imshow("edges", edges)
cv2.waitKey()

cv2.imshow("Output", img)
cv2.waitKey()

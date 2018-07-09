from __future__ import division

import argparse as ap
import numpy as np
import interceptHelper as iH
import cv2

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Load the image
img = cv2.imread(args["image"])
img = img.copy()

##################
# # Gamma Correction
# gamma = 2.0
# img = iH.adjust_gamma(img, gamma=gamma)
# cv2.imshow("Gamma Corrected", img)
# cv2.waitKey()
##################

# img = iH.increase_contrast(img)

img_shadowless = iH.rm_shadow(img)
cv2.imshow("Removed Shadow", img)

#####################################
# Pre-Process Image
kernel = np.ones((5, 5), np.uint8)
img_erosion = cv2.erode(img_shadowless, kernel, iterations=1)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)
####################################

# 20, 50, 50
# Finding the edge of the block with bilateral filter
img_blurred_bilateral = cv2.bilateralFilter(img_dilation, 20, 50, 50)
edges = cv2.Canny(img_blurred_bilateral, 200, 300)

# Since this is using bilateral filtering method, I dont think we need to convert the picture to grey scale anymore
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Display the result of the edge detection
cv2.imshow("edges", edges)
cv2.waitKey()

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
# threshold=30, minLineLength=20, maxLineGap=60

lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=32, minLineLength=20, maxLineGap=60)
line_cnt = 0
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1)

        # Label Line Recognized
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        cv2.putText(img, str(line_cnt), (center_x, center_y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255), 1)

    line_cnt = line_cnt + 1

########################################################################
# Extend the lines if they are too short
ext_lines = []
for line in lines.copy():
    new_line = iH.extend_line(line)
    ext_lines.append(new_line)
    # Draw Lines after extension
    cv2.line(img, (new_line[0][0], new_line[0][1]), (new_line[0][2], new_line[0][3]), (0, 0, 255), 1)

print("There are " + str(len(ext_lines)) + " lines detected in the frame")

intersections = []


# i, j prevent from checking two same lines' intersection
i = 0

for line_1 in ext_lines:
    j = 0
    for line_2 in ext_lines:
        if i < j:
            x_center, y_center, theta, found = iH.check_intersect(line_1[0], line_2[0])
            if found:
                new_point = iH.Intersect(x_center, y_center, theta)
                # print("The coordinate is (" + str(new_point.x) + ", " + str(new_point.y) + ")")

                # new_img = img.copy()
                # cv2.line(new_img, (line_1[0][0], line_1[0][1]), (line_1[0][2], line_1[0][3]), (0, 0, 255), 2)
                # cv2.line(new_img, (line_2[0][0], line_2[0][1]), (line_2[0][2], line_2[0][3]), (0, 0, 255), 2)
                # cv2.circle(new_img, (new_point.x, new_point.y), 9, (255, 255, 255), -1)
                # cv2.imshow("Result", new_img)
                # cv2.waitKey()
                # cv2.destroyAllWindows()
                intersections.append(new_point)

        j = j + 1
    i = i + 1

intersections = iH.rm_nearby_intersect(intersections)

print("First line is: " + str(ext_lines[1]))
print("Second line is: " + str(ext_lines[5]))
print("Intersection is" + str(iH.check_intersect(ext_lines[1][0], ext_lines[5][0])))

print("Number of Intersections: " + str(len(intersections)))

if len(intersections) == 0:
    print("There is no intersection points")

# Label all the intersections
for point in intersections:
    cv2.circle(img, (point.x, point.y), 5, (255, 255, 255), -1)

#########################################################################

# Fill out incomplete Rectangle

# kernel = np.ones((5, 5), np.uint8)
# erosion = cv2.erode(canvas, kernel, iterations=20)
# dilate = cv2.dilate(erosion, kernel, iterations=20)

# cv2.imshow("Post-Processinged Image", canvas)
# cv2.waitKey()

# out = np.bitwise_or(img, edges[:, :, np.newaxis])

# cv2.imshow("edges", edges)
# cv2.waitKey()

cv2.imshow("Output", img)
cv2.waitKey()

height, width, _ = img.shape
blank_image = np.zeros((height,width,3), np.uint8)
for point in intersections:
    cv2.circle(blank_image, (point.x, point.y), 5, (255, 255, 255), -1)
cv2.imshow("Only the dots", blank_image)
cv2.waitKey()

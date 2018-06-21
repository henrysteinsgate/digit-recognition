import imutils
import cv2
import numpy as np
import argparse as ap

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

#load the image, convert it to grayscale, blur it slightly, and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(gray, 7)
blurred = cv2.GaussianBlur(img, (5, 5), 0)
thresh = cv2.threshold(blurred, 95, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.bitwise_not(thresh)

kernel = np.ones((5,5),np.uint8)
dilate = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# cv2.imshow("Blurred", th3)
# cv2.imshow("Originl Threshholding", thresh)
cv2.imshow("Erosion with Dilation", dilate)
cv2.waitKey(0)




# # find contours in the thresholded image
# cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2()else cnts[1]

# num_block = []
# rect = []

# # loop over for contours
# for c in cnts:
#     # compute the bounding box of the contour
#     (x, y, w, h) = cv2.boundingRect(c)

#     # if the contour is sufficiently large, it must be a number
#     if (w >= 40) and (h >= 40):
#         num_block.append(c)
#         rect.append(cv2.rectangle(dilate,(x,y),(x+w,y+h),(0,255,0),2))

# i = 1
# for c in num_block:
#     # compute the center of the contour
#     M = cv2.moments(c)
#     if(M["m00"] == 0):
#         M["m00"] = 1
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])

#     # draw the contour and center of the shape on the image
#     cv2.drawContours(image, [c], -1, (0,255,0), 2)
#     cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
#     cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_COMPLEX,
#                 0.5, (255, 255, 255), 2)

#     rect = cv2.minAreaRect(c)
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     cv2.drawContours(image,[box], -1, (0,0,255,2))
#     i = i + 1
# #show the image
# cv2.imshow("Image", image)
# cv2.waitKey(0)
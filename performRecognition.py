#!/usr/bin/python

# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import argparse as ap
import time

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-c", "--classiferPath", help="Path to Classifier File", required="True")
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Load the classifier
clf, pp = joblib.load(args["classiferPath"])

# Read the input image 
im = cv2.imread(args["image"])

# Convert to grayscale and apply Gaussian filtering
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.medianBlur(im_gray, 7)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

# Threshold the image
# ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
ret, im_th = cv2.threshold(im_gray, 100, 255, cv2.THRESH_BINARY_INV)

# Find contours in the image
_, ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



# Debuggin
colored = cv2.cvtColor(im_th, cv2.COLOR_GRAY2RGB)

for ctr in ctrs:
    x,y,w,h = cv2.boundingRect(ctr)
    if(w >= 5 and h >= 40):
        # cv2.rectangle(colored,(x,y),(x+w,y+h),(0,255,0),2)
        time.sleep(0.01)
    else:
        cv2.drawContours(colored,[ctr],0,(0,0,0),-1)

colored = cv2.cvtColor(colored, cv2.COLOR_BGR2GRAY)

_, ctrs, hier = cv2.findContours(colored.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#for ctr in ctrs:
#	x,y,w,h = cv2.boundingRect(ctr)
#	cv2.bitwise_not(colored)
colored = cv2.bitwise_not(colored)

kernel = np.ones((3,3),np.uint8)
erode = cv2.erode(colored,kernel,iterations = 2)



# # Test Erosion
# erode_1 = erode
# erode_2 = cv2.erode(colored,kernel,iterations = 2)

# cv2.imshow("erode with 1 iterations", erode_1)
# cv2.waitKey()
# cv2.imshow("erode with 2 iterations", erode_2)
# cv2.waitKey()

global im_w, im_h, im_c
im_w, im_h, im_c = im.shape
# we do not need to print the size of the script anymore
# print "width", im_w, "height", im_h

center_x = im_h/2
center_y = im_w/2
# cv2.circle(colored,(center_x, center_y), 2, (0,0,255), -1)

cv2.imshow("Denoised", erode)
cv2.imshow("Original", colored)
cv2.waitKey()


# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

# Segment all the connected blocks
rects_split = []
for rect in rects:
    # If width is much greater that height, then 2 horizontal blocks in a row
    if rect[2] >= int(1.5 * rect[3]):
        new_rect_1 = (rect[0], rect[1], rect[2] // 2, rect[3])
        new_rect_2 = (rect[0] + rect[2] // 2, rect[1], rect[2] // 2, rect[3])

        rects_split.append(new_rect_1)
        rects_split.append(new_rect_2)
    # if height is much greater than width, then 2 vertical blocks in a row
    elif rect[3] >= int(1.5 * rect[2]):
        new_rect_1 = (rect[0], rect[1], rect[2], rect[3] // 2)
        new_rect_2 = (rect[0], rect[1] + rect[3] // 2, rect[2], rect[3] // 2)

        rects_split.append(new_rect_1)
        rects_split.append(new_rect_2)
    else:
        rects_split.append(rect)


# For each rectangular region, calculate HOG features and predict
# the digit using Linear SVM.

crop_pixel = 15

for rect in rects_split:
    # Draw the rectangles
    cv2.rectangle(im, (rect[0] + crop_pixel, rect[1] + crop_pixel), (rect[0] + rect[2] - crop_pixel, rect[1] + rect[3] - crop_pixel), (0, 255, 0), 3)
    # Make the rectangular region around the digit
    # leng = int(rect[3] * 1.6 - crop_pixel)
    # pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    # pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    pt1 = int(rect[1] + crop_pixel)
    pt2 = int(rect[1] + rect[3] - crop_pixel)
    pt3 = int(rect[0] + crop_pixel)
    pt4 = int(rect[0] + rect[2] - crop_pixel)
    roi = im_th[pt1:pt2, pt3:pt4]
    # Resize the image
    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    roi = cv2.dilate(roi, (3, 3))
    # Calculate the HOG features
    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    roi_hog_fd = pp.transform(np.array([roi_hog_fd], 'float64'))
    nbr = clf.predict(roi_hog_fd)
    cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

cv2.imshow("Blah", im)
cv2.waitKey()

cv2.namedWindow("Resulting Image with Rectangular ROIs", cv2.WINDOW_NORMAL)
cv2.imshow("Resulting Image with Rectangular ROIs", im)
cv2.waitKey()
cv2.destroyAllWindows()

#Henry's Method to crop the center part of the number off
def centerCorrection(x, y, w, h, correct_amount_x=None, correctAmountY=None):

    # Adding default options so that you do not have to input the correctAmount values
    if correctAmountY is None:
        correctAmountY = 1

    if correct_amount_x is None:
        correct_amount_x = 2

    z = 25 // 35 * 10
    t = (w - z) * (1 if x > im_w // 2 else -1) # if the number is to the left or to the right of the center
    xp = x + t
    wp = z
    zp = 25 // 35 * correct_amount_x
    tp = wp - zp
    xpp = xp + tp // 2
    wpp = zp

    z = 25 // 35 * 10
    t = (h - z) * (1 if y > im_h // 2 else -1) # if the number is to the upper or to the lower of the center
    yp = y + t
    hp = z
    zp = 25 // 35 * correctAmountY
    tp = hp - zp
    ypp = yp + tp // 2
    hpp = zp
    return xpp, ypp, wpp, hpp



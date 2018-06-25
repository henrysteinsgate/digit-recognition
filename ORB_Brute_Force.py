import cv2
import numpy as np
import os
import argparse as ap

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Load the image and the templates
img = cv2.imread(args["image"])
img_show = img.copy()

templates = load_images_from_folder("/home/hud/Summer_ws/digit-recognition/Templates")

for template in templates:
        orb = cv2.ORB_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = orb.detectAndCompute(img_show, None)
        kp2, des2 = orb.detectAndCompute(template, None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1, des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)

        # Draw first 10 matches.
        # img3 = cv2.drawMatches(img_show, kp1, template, kp2, matches[:10], None, flags=2)
        img3 = cv2.drawMatches(img_show, kp1, template, kp2, matches, None, flags=2)
        cv2.imshow("Matching Features", img3)

        cv2.waitKey()
        cv2.destroyAllWindows()

import cv2
import os
import argparse as ap


# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Load the image and the templates
img = cv2.imread(args["image"])


def load_images_from_folder(folder):
    images = []
    file_list = os.listdir(folder)

    def last_5chars(x):
        return x[-5:]

    for filename in sorted(file_list, key=last_5chars):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def detect_block(block_num, image):
    img_show = image.copy()

    templates = load_images_from_folder("/home/hud/Summer_ws/digit-recognition/Templates")

    template_index = 1
    locations = []
    numbers = []

    for template in templates:

        w, h, _ = template.shape
        # All the 6 methods for comparison in a list
        # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
        #             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        # #Below are the two methods that are working
        meth = 'cv2.TM_CCOEFF_NORMED'
        img = img_show.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        if max_val >= 0.7:
            cv2.rectangle(img_show, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(img_show, str(template_index), (top_left[0], top_left[1]), cv2.FONT_HERSHEY_DUPLEX, 2,
                        (0, 255, 255), 3)
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            center = (center_x, center_y)
            # number stores the block number found in frame
            locations.append(center)
            numbers.append(template_index)

        template_index = template_index + 1

    cv2.imshow("Result", img_show)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print(numbers)

    if block_num not in numbers:
        print("Could not find the block you are asking for.")
        return None
    else:
        index = numbers.index(block_num)

        # Return the coordinate of the desired block
        cv2.circle(img_show, (locations[index][0], locations[index][1]), 10, (0, 0, 0), 4)
        cv2.imshow("Final output", img_show)
        print("Found block at")
        print(locations[index])
        cv2.waitKey()
        return locations[index]


detect_block(9, img)
from __future__ import division
from sympy.solvers import solve
from sympy import Symbol
import math
import warnings


#########################################################
#########################################################
# Check intersection of two points, if there is return the
# point, angle, and True; if not, return none and False

def check_intersect(line_1, line_2):
    # Endpoints of the first line
    pt1 = (line_1[0], line_1[1])
    pt2 = (line_1[2], line_1[3])
    # Endpoints of the second line
    pt3 = (line_2[0], line_2[1])
    pt4 = (line_2[2], line_2[3])

    # Calculate slope and y-intersect of each line
    m1 = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
    b1 = pt1[1] - pt1[0] * m1

    m2 = (pt4[1] - pt3[1]) / (pt4[0] - pt3[0])
    b2 = pt3[1] - pt3[0] * m2

    # Ignore warning when getting a infinity slope
    warnings.filterwarnings("ignore")

    # Consider if the lines are horizontal or vertical to cause a non-resolvable slope for intersection
    if m1 == m2:
        return None, None, None, False
    elif m1 == -float('Inf') and abs(m2) <= 0.05:
        if pt3[0] <= pt1[0] <= pt4[0] and min(pt1[1], pt2[1]) <= pt3[1] <= max(pt1[1], pt2[1]):
            x_intersect = pt1[0]
            y_intersect = pt3[1]
            theta = 90
            return x_intersect, y_intersect, theta, True
    elif abs(m1) <= 0.05 and m2 == -float('Inf'):
        if pt1[0] <= pt3[0] <= pt2[0] and min(pt3[1], pt4[1]) <= pt1[1] <= max(pt3[1], pt4[1]):
            x_intersect = pt3[0]
            y_intersect = pt1[1]
            theta = 90
            return x_intersect, y_intersect, theta, True

    # Solve for intersection
    x = Symbol('x')
    solution = solve((m1 - m2) * x + b1 - b2, x)
    if len(solution) != 1:
        return None, None, None, False

    # Check if intersects fall in the range of two lines
    elif pt1[0] <= solution <= pt2[0] and pt3[0] <= solution <= pt4[0]:
        # print("Solution is " + str(float(solution[0])))

        x_intersect = int(solution[0])
        y_intersect = int(m2 * solution[0] + b2)

        theta1 = math.atan(m1)
        theta2 = math.atan(m2)
        theta = int(math.degrees(theta2 - theta1))

        # Adjust the threshold angle below to check for perpendicular lines
        if (100 > theta > 80) or (-100 < theta < -80):
            return x_intersect, y_intersect, theta, True
        else:
            return None, None, None, False
    else:
        return None, None, None, False


def extend_line(line):
    x1, y1, x2, y2 = line[0]
    length = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    # TODO: Adjust the following threshold to pass the lines
    threshold = 40
    if length < threshold:
        return line
    else:
        # TODO: Extends to about 2.2 of its original length, might need change ratio
        ratio = 0.6
        delta_x = int(abs(x2 - x1) * ratio)
        delta_y = int(abs(y2 - y1) * ratio)
        x1_p = x1 - delta_x
        x2_p = x2 + delta_x
        if y1 > y2:
            y1_p = y1 + delta_y
            y2_p = y2 - delta_y
        else:
            y1_p = y1 - delta_y
            y2_p = y2 + delta_y
        extended = [x1_p, y1_p, x2_p, y2_p]

        return [extended]


def rm_nearby_lines(lines):
    for line_1 in lines:
        # Endpoints of the first line
        pt1 = (line_1[0], line_1[1])
        pt2 = (line_1[2], line_1[3])

        # Calculate slope and y-intersect of each line
        m1 = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
        b1 = pt1[1] - pt1[0] * m1

        for line_2 in lines:
            # Endpoints of the second line
            pt3 = (line_2[0], line_2[1])
            pt4 = (line_2[2], line_2[3])

            m2 = (pt4[1] - pt3[1]) / (pt4[0] - pt3[0])
            b2 = pt3[1] - pt3[0] * m2

            if abs(m1 - m2) < 0:
                return None


def rm_nearby_intersect(intersections):
    if len(intersections) != 0:
        i = 0
        for line_1 in intersections:
            j = 0
            for line_2 in intersections:
                if i != j:
                    x1, y1 = line_1.x, line_1.y
                    x2, y2 = line_2.x, line_2.y
                    if abs(x1 - x2) <= 15 and abs(y1 - y2) <= 15:
                        print(str(abs(x1 - x2)))
                        intersections.remove(line_2)
                j = j + 1
            i = i + 1

def categorize_rect(intersections):


def mid_point(point1, point2):
    return Intersect((point1.x + point2.x)/2, (point1.y + point2.y)/2)

class Intersect:
    def __init__(self, x_intersect, y_intersect, theta=None):
        self.x = x_intersect
        self.y = y_intersect
        if theta is not None:
            self.theta = theta

class Rectangle:
    def __init__(self, index, point1, point2, point3, point4 = None):
        self.center = Intersect(0,0)
        self.index = index
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        if point4 is None:
            self.center = self.find_its_center_3(self)
        else:
            self.center = self.find_its_center_4(self)

    def find_its_center_3(self):
        length1 = math.hypot(self.point1, self.point2)
        length2 = math.hypot(self.point2, self.point3)
        length3 = math.hypot(self.point1, self.point3)
        if length1 >= length2 and length1 >= length3:
            center = mid_point(self.point1,self.point2)
        elif length2 >= length1 and length2 >= length3:
            center = mid_point(self.point2,self.point3)
        else:
            center = mid_point(self.point1, self.point3)
        return center

# TODO: add method for 4 points given
    def find_its_center_4(self):
        center = Intersect(0,0)
        return center

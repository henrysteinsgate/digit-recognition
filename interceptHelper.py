from __future__ import division
from sympy.solvers import solve
from sympy import Symbol
import math

#########################################################
#########################################################
# TODO: Make the following method and class a separate file and import it as module
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

    # Solve for intersection
    x = Symbol('x')
    solution = solve((m1 - m2) * x + b1 - b2, x)
    if len(solution) != 1:
        return None, None, None, False

    # Check if intersects fall in the range of two lines
    elif solution > pt1[0] and solution < pt2[0] and solution > pt3[0] and solution < pt4[0]:
        # print("Solution is " + str(float(solution[0])))

        x_intersect = int(solution[0])
        y_intersect = int(m2 * solution[0] + b2)

        theta1 = math.atan(m1)
        theta2 = math.atan(m2)
        theta = int(math.degrees(theta2 - theta1))
        # print("Theta is " + str(theta))

        # Adjust the threshold angle below to check for perpendicular lines
        if (theta < 100 and theta > 80) or (theta > -100 and theta < -80):
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
        # TODO: Extends to about 1.8 of its original length, might need change ratio
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


class Intersect:
    def __init__(self, x_intersect, y_intersect, theta):
        self.x = x_intersect
        self.y = y_intersect
        self.theta = theta

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import math


# Internal methods
def get_angle_between_points(segm_s, q, segm_e):
    """
    Calculate the angle between the segments defined by points segm_s, q and q, segm_e.
    Returns the angle in radians.
    """
    # Calculate vectors
    v1_x = segm_s.x() - q.x()
    v1_y = segm_s.y() - q.y()
    v2_x = segm_e.x() - q.x()
    v2_y = segm_e.y() - q.y()
    # Calculate norms
    norm1 = math.sqrt(v1_x ** 2 + v1_y ** 2)
    norm2 = math.sqrt(v2_x ** 2 + v2_y ** 2)
    # Calculate dot product
    dot_product = v1_x * v2_x + v1_y * v2_y
    # Calculate cross product
    cross_product = v1_x * v2_y - v2_x * v1_y
    # Calculate the angle in radians
    angle = math.atan2(cross_product, dot_product)
    return angle


def get_relative_position(segm_s, segm_e, q):
    """
    Get relative position of point q against segment defined by
    Returns:
        -1 if q is to the right of the segment,
         0 if q is on the segment or collinear with it,
         1 if q is to the left of the segment.
    """
    # Calculate the components of the cross product
    dx1 = segm_e.x() - q.x()
    dy1 = segm_e.y() - q.y()
    dx2 = segm_s.x() - q.x()
    dy2 = segm_s.y() - q.y()

    # Compute the cross product
    cross_product = dx1 * dy1 - dx2 * dy2

    # Point is collinear with segment
    if abs(cross_product) < 1e-9:
        return 0
    # Point in the left half-plane
    elif cross_product > 0:
        return 1
    # Point in the right half-plane
    else:
        return -1


# Processing data
class Algorithms:
    def __init__(self):
        pass

    @staticmethod
    def analyze_point_polygon_position(q: QPointF, pol: QPolygonF):
        """
        Implementation fo Ray Crossing algorithm
        :param q: QPointF
        :param pol: QPolygonF
        :return: bool value as int (1 - point is within polygon, 0 - not within polygon)
        """
        # Initialize amount of intersections
        k = 0
        # Amount of vertices
        n = len(pol)
        # Process all segments
        for i in range(n):
            # Reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            xi1r = pol[(i + 1) % n].x() - q.x()
            yi1r = pol[(i + 1) % n].y() - q.y()
            if ((yi1r > 0) and (yir <= 0)) or ((yir > 0) and (yi1r <= 0)):
                # Compute intersection
                xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)
                # Right half plane
                if xm > 0:
                    k += 1
        # Point q inside polygon?
        if k % 2 == 1:
            return 1
        # Point q outside polygon
        return 0

    @staticmethod
    def winding_number(q: QPointF, pol: QPolygonF, tolerance=1e-10):
        """
        Implementation of winding number algorithm
        :param q point as QPointF object
        :param pol polygon as QPolygonF object
        :param tolerance value from 2pi multiplied
        :return 1 if the point is inside the polygon, 0 otherwise.
        """
        omega = 0
        for i in range(len(pol)):
            xi, yi = pol[i].x(), pol[i].y()
            xj, yj = pol[(i + 1) % len(pol)].x(), pol[(i + 1) % len(pol)].y()
            dx1, dy1 = xi - q.x(), yi - q.y()
            dx2, dy2 = xj - q.x(), yj - q.y()
            cross_product = dx1 * dy2 - dx2 * dy1
            dot_product = dx1 * dx2 + dy1 * dy2
            distance = math.sqrt((dx1 ** 2 + dy1 ** 2) * (dx2 ** 2 + dy2 ** 2))
            if distance == 0:  # point intersects edge
                return 1
            wn = dot_product / distance
            omega_temp = math.acos(wn)
            if cross_product > 0:
                omega += omega_temp
            elif cross_product < 0:
                omega -= omega_temp
            else:
                pass
        k = round(abs(omega) / math.pi)
        if abs(omega - k * math.pi) < tolerance and k > 0:
            return 1
        else:
            return 0

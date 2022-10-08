import cv2
import numpy as np
import math


def __get_center(points):
    corners = points.reshape((4, 2))
    (topLeft, topRight, bottomRight, bottomLeft) = corners

    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
    cY = int((topLeft[1] + bottomRight[1]) / 2.0)

    return cX, cY

def _get_center(p1, p2):
    cX = int((p1[0] + p2[0]) / 2.0)
    cY = int((p1[1] + p2[1]) / 2.0)

    return cX, cY


def _get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    diff1 = abs(x2 - x1)**2
    diff2 = abs(y2 - y1)**2
    return int(math.sqrt(diff1 + diff2))


def find_marker(image):
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
    
    marker_positions = []
    marker_sizes = []
    for points in corners:
        corners = points.reshape((4, 2))
        p1, _, p2, _ = corners
        marker_positions.append(_get_center(p1, p2))
        marker_sizes.append(_get_distance(p1, p2))
        #marker_positions.append(_get_center(points))

    return marker_positions, marker_sizes

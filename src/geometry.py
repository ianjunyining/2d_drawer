import math
import numpy as np

def distance_point_to_segment(pt1, pt2, pt):
    # Convert points to numpy arrays
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    pt = np.array(pt)
    
    # Vector from pt1 to pt2
    d = pt2 - pt1
    # Vector from pt1 to pt
    v = pt - pt1
    
    # Dot products
    d_dot_d = np.dot(d, d)
    v_dot_d = np.dot(v, d)
    
    # Parameter t of the projection
    t = v_dot_d / d_dot_d
    
    # Clamping t to the segment
    if t < 0.0:
        closest_point = pt1
    elif t > 1.0:
        closest_point = pt2
    else:
        closest_point = pt1 + t * d
    
    # Distance from pt to the closest point
    distance = np.linalg.norm(pt - closest_point)
    
    return distance

def rotate(pt, theta, center=(0, 0)):
    x0, y0 = pt
    u, v = center
    x1 = (x0 - u) * math.cos(theta) - (y0 - v) * math.sin(theta) + u
    y1 = (x0 - u) * math.sin(theta) + (y0 - v) * math.cos(theta) + v
    return (x1, y1)

def distance(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def translate(point : tuple, delta : tuple):
    return (point[0] + delta[0], point[1] + delta[1])

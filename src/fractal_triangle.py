from src.shape import *
import src.geometry as geo
import turtle

def make_triangle(points, color):
    pen = turtle.Turtle()
    pen.color(color)
    return Polygon(pen, points)

def get_mid(p1, p2):
    return geo.avg_points([p1, p2])

def sierpinski(points, degree, triangles:list):
    colormap = [
        "blue", "red", "green", "black", "blue", "red", "green", "black",
        "blue", "red", "green", "black", "blue", "red", "green", "black", 
    ]
    triangles.append(make_triangle(points, colormap[degree]))
    if degree <= 0:
        return
    
    sierpinski(
        [
            points[0],
            get_mid(points[0], points[1]),
            get_mid(points[0], points[2]),
        ],
        degree-1, 
        triangles,
    )
    sierpinski(
        [
            points[1],
            get_mid(points[0], points[1]),
            get_mid(points[1], points[2]),
        ],
        degree-1, 
        triangles,
    )
    sierpinski(
        [
            points[2],
            get_mid(points[2], points[1]),
            get_mid(points[0], points[2]),
        ],
        degree-1, 
        triangles,
    )

def make_fractal_triangle(degree, points, color):
    triangles = []
    sierpinski(points, degree, triangles)
    triangles.reverse()
    return triangles

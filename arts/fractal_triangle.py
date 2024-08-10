import turtle
from src.shape import *
import src.geometry as geo
from arts.art_base import ArtBase


class FractalTriangle(ArtBase):

    def __init__(self) -> None:
        super().__init__()
        self.degree = 6
        self.points = [[-300.0, -150.0], [0.0, 300.0], [300.0, -150.0]]
        self.color = "blue"

    def make_triangle(self, points, color):
        pen = turtle.Turtle()
        pen.color(color)
        return Polygon(pen, points)

    def sierpinski(self, points, degree, triangles:list):
        colormap = [
            "blue", "red", "green", "black", "blue", "red", "green", "black",
            "blue", "red", "green", "black", "blue", "red", "green", "black", 
        ]
        triangles.append(self.make_triangle(points, colormap[degree]))
        if degree <= 0:
            return
        
        self.sierpinski(
            [
                points[0],
                geo.avg_points([points[0], points[1]]),
                geo.avg_points([points[0], points[2]]),
            ],
            degree-1, 
            triangles,
        )
        self.sierpinski(
            [
                points[1],
                geo.avg_points([points[0], points[1]]),
                geo.avg_points([points[1], points[2]]),
            ],
            degree-1, 
            triangles,
        )
        self.sierpinski(
            [
                points[2],
                geo.avg_points([points[2], points[1]]),
                geo.avg_points([points[0], points[2]]),
            ],
            degree-1, 
            triangles,
        )

    def create_shapes(self):
        triangles = []
        self.sierpinski(self.points, self.degree, triangles)
        triangles.reverse()
        return triangles

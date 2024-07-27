import turtle
from src.shape import *

class Canvas():
    def __init__(self) -> None:
        self.shapes = []

    def draw(self):
        for shape in self.shapes:
            shape.draw()
        
    def select_shapes(self, point):
        for shape in self.shapes:
            selected_old = shape.selected
            selected_new = shape.point_in_shape(point)
            shape.selected = selected_new
            if selected_old != selected_new:
                shape.draw()

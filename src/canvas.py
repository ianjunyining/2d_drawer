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

    def delete_selected(self):
        pass

    # delta: (dx, dy)
    def translate_selected(self, delta):
        pass

    # if only one shape is selected, rotate around the center of the selected shape
    # otherwise, compute the center from the selection points of all selected shapes, 
    # and rotate all selected shapes around this center.
    def rotate_selected(self, angle_in_deg):
        pass

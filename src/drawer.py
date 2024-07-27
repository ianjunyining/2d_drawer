from src.canvas import Canvas
from src.shape import *
import turtle, enum

class Action(enum.Enum):
    SELECT = 1
    LINE = 2
    CIRCLE = 3
    POLYGON = 4

class State(enum.Enum):
    START = 1
    END = 2

class Drawer():
    def __init__(self, screen):
        self.canvas = Canvas()
        self.action = Action.SELECT
        self.state = State.END

        self.temp_line = None

        self.canvas.shapes = [
            Line(turtle.Turtle(), (-10, -10), (50, 50)),
            Line(turtle.Turtle(), (-10, 40), (50, -50)),
        ]
        self.canvas.draw()
    
    def make_line(self, x, y):
        if self.action != Action.LINE:
            return
        if self.state == State.END:
            self.state = State.START
            self.temp_line = Line(turtle.Turtle(), (x, y), (x, y))
            self.temp_line.draw()
        elif self.state == State.START:
            self.state = State.END
            self.temp_line.point2 = (x, y)
            self.temp_line.draw()
            self.canvas.shapes.append(self.temp_line)

    def onclick(self, x, y): 
        if self.action == Action.LINE:
            self.make_line(x, y)
        elif self.action == Action.SELECT:
            self.canvas.select_shapes((x, y))

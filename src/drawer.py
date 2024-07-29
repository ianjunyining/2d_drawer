from src.canvas import Canvas
from src.shape import *
from src.button import Button
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
        self.screen = screen
        self.screen.screensize(700, 600)
        screen_sz = self.screen.screensize()
        print("screen_sz: ", screen_sz)
        self.hw = screen_sz[0] / 2
        self.hh = screen_sz[1] / 2 
        self.gap = 5
        self.btn_sz = (60, -30)

        self.create_buttons()

        self.canvas = Canvas()
        self.action = Action.SELECT
        self.state = State.END

        self.temp_line = None

        # self.canvas.shapes = [
        #     Circle(turtle.Turtle(), 10, (0, 0)),
        #     Line(turtle.Turtle(), (-10, 40), (50, -50)),
        # ]
        # self.canvas.draw()
    
    def create_buttons(self):
        btn_gap = self.btn_sz[0] + self.gap
        self.buttons_map = {
            Action.SELECT: Button(turtle.Turtle(), (-self.hw + self.gap, self.hh - self.gap), self.btn_sz, "Select"),
            Action.LINE: Button(turtle.Turtle(), (-self.hw + self.gap + btn_gap * 1, self.hh - self.gap), self.btn_sz, "Line"),
            Action.CIRCLE: Button(turtle.Turtle(), (-self.hw + self.gap + btn_gap * 2, self.hh - self.gap), self.btn_sz, "Circle"),
        }
        self.buttons_map[Action.SELECT].selected = True
        for act, btn in self.buttons_map.items():
            btn.draw()

    def click_on_button(self, x, y):
        old_act = self.action
        new_act = None
        for act, btn in self.buttons_map.items():
            if btn.inbox((x, y)):
                new_act = act
                break
        if new_act and new_act != old_act:
            self.action = new_act
            self.buttons_map[old_act].set_selection(False)
            self.buttons_map[new_act].set_selection(True)
        return new_act          

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

    def make_circle(self, x, y):
        if self.action != Action.CIRCLE:
            return
        if self.state == State.END:
            self.state = State.START
            self.temp_circle = Circle(turtle.Turtle(), 0, (x, y))
            self.temp_circle.draw()
        elif self.state == State.START:
            self.state = State.END
            self.temp_circle.r = geo.distance(self.temp_circle.center, (x, y)) 
            self.temp_circle.draw()
            self.canvas.shapes.append(self.temp_circle)

    def onclick(self, x, y): 
        if self.click_on_button(x, y):
            # don't draw
            pass
        elif self.action == Action.SELECT:
            self.canvas.select_shapes((x, y))
        elif self.action == Action.LINE:
            self.make_line(x, y)
        elif self.action == Action.CIRCLE:
            self.make_circle(x, y)
    
    def onkeyarrow(self, key_pressed):
        key_translation = {
            "up" : [0, 1],
            "down" : [0, -1],
            "left" : [-1, 0],
            "right" : [1, 0],
        }
        for key in key_translation.keys():
            if key == key_pressed:
                for shape in self.canvas.shapes:
                    x0, y0 = shape.center
                    if shape.selected:
                        shape.center = (
                            x0 + key_translation[key][0], 
                            y0 + key_translation[key][1]
                        )
        for shape in self.canvas.shapes:
            shape.draw()
    
    def onkeydelete(self):
        print("enter: ")
        for i in range(len(self.canvas.shapes)):
            if self.canvas.shapes[i].selected:
                self.canvas.shapes[i].clear()
                del self.canvas.shapes[i]

    def onkeyup(self):
        self.onkeyarrow("up")

    def onkeydown(self):
        self.onkeyarrow("down")

    def onkeyleft(self):
        self.onkeyarrow("left")

    def onkeyright(self):
        self.onkeyarrow("right")




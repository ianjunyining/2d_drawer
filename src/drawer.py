from src.canvas import Canvas
from src.shape import *
from src.button import Button
import turtle, enum, math

class Action(enum.Enum):
    SELECT = 1
    DESELECT = 2
    LINE = 3
    CIRCLE = 4
    POLYGON = 5
    RPOLYGON = 6


class State(enum.Enum):
    START = 1
    END = 2

class Drawer():
    def __init__(self, screen):
        self.shift_pressed = False
        self.screen = screen
        self.screen.screensize(700, 600)
        screen_sz = self.screen.screensize()
        print("screen_sz: ", screen_sz)
        self.hw = screen_sz[0] / 2
        self.hh = screen_sz[1] / 2 
        self.gap = 5
        self.polygon_sides = -1
        self.btn_sz = (60, -30)

        self.create_buttons()

        self.canvas = Canvas()
        self.action = Action.SELECT
        self.state = State.END
    
    def create_buttons(self):
        btn_gap = self.btn_sz[0] + self.gap
        self.buttons_map = {
            Action.SELECT: Button(turtle.Turtle(), (-self.hw + self.gap, self.hh - self.gap), self.btn_sz, "Select"),
            Action.LINE: Button(turtle.Turtle(), (-self.hw + self.gap + btn_gap * 1, self.hh - self.gap), self.btn_sz, "Line"),
            Action.CIRCLE: Button(turtle.Turtle(), (-self.hw + self.gap + btn_gap * 2, self.hh - self.gap), self.btn_sz, "Circle"),
            Action.POLYGON: Button(turtle.Turtle(), (-self.hw + self.gap + btn_gap * 3, self.hh - self.gap), self.btn_sz, "Polygon"),
            Action.RPOLYGON: Button(turtle.Turtle(), (-self.hw + self.gap + btn_gap * 4, self.hh - self.gap), self.btn_sz, "RPolygon"),
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

    def make_polygon(self):
        pass

    def make_regular_polygon(self, x, y):
        if self.action != Action.RPOLYGON:
            return
        if self.state == State.END:
            self.state = State.START
            self.temp_rpolygon = RegularPolygon(turtle.Turtle(), (x, y), 0, 0)
        elif self.state == State.START:
            self.state = State.END
            sides = self.screen.textinput("Enter sides", "How many sides?")
            self.screen.listen()
            if sides:
                self.temp_rpolygon.r = geo.distance(self.temp_rpolygon.center, (x, y)) 
                self.temp_rpolygon.num_sides = int(sides)
                self.temp_rpolygon.draw()
                self.canvas.shapes.append(self.temp_rpolygon)

    def onclick(self, x, y): 
        if self.click_on_button(x, y):
            # don't draw
            pass
        elif self.action == Action.SELECT:
            self.canvas.select_shapes((x, y))
        elif self.action == Action.DESELECT:
            self.canvas.deselect_all()
        elif self.action == Action.LINE:
            self.make_line(x, y)
        elif self.action == Action.CIRCLE:
            self.make_circle(x, y)
        elif self.action == Action.RPOLYGON:
            self.make_regular_polygon(x, y)
    
    def onkeyarrow(self, key_pressed):
        key_translation = {
            "up" : (0, 1),
            "down" : (0, -1),
            "left" : (-1, 0),
            "right" : (1, 0),
        }
        magnitude = 10 if self.shift_pressed else 1
        for key in key_translation.keys():
            if key == key_pressed:
                self.canvas.translate_selected((key_translation[key][0] * magnitude,
                                                key_translation[key][1] * magnitude))
                
    def onkeyrotate(self, key_pressed, magnitude=1):
        key_rotate = {
            "a" : -math.pi / 180 * magnitude,
            "d" : math.pi / 180 * magnitude,
        }
        for key in key_rotate.keys():
            if key == key_pressed:
                self.canvas.rotate_selected(key_rotate[key])
    
    def onkeydelete(self):
        self.canvas.delete_selected()

    def onkeyup(self):
        self.onkeyarrow("up")

    def onkeydown(self):
        self.onkeyarrow("down")

    def onkeyleft(self):
        self.onkeyarrow("left")

    def onkeyright(self):
        self.onkeyarrow("right")

    def onkeyclockwise(self):
        self.onkeyrotate("d")

    def onkeycounterclockwise(self):
        self.onkeyrotate("a")





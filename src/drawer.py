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
    FRACTAL_TRI = 7


class Color(enum.Enum):
    BLACK = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4


class State(enum.Enum):
    START = 1
    END = 2


class Drawer():
    def __init__(self, screen):
        self.screen = screen
        self.shift_pressed = False
        self.w = screen.window_width()
        self.h = screen.window_height()
        self.hw = self.w / 2 
        self.hh = self.h / 2 
        self.gap = 5
        self.btn_sz = (60, -30)

        self.create_buttons()

        self.canvas = Canvas()
        self.action = Action.SELECT
        self.color = Color.BLUE
        self.state = State.END
    
    def get_color_str(self, color: Color):
        color_map = {
            Color.BLACK : "black",
            Color.RED : "red",
            Color.BLUE : "blue",
            Color.GREEN : "green",
            Color.YELLOW : "yellow",
        }
        return color_map[color]
    
    def create_buttons(self):
        btn_gap = self.btn_sz[0] + self.gap
        btn_st_y = self.hh - self.gap
        btn_st_x = -self.hw + self.gap
        self.action_buttons = {
            Action.SELECT: Button(turtle.Turtle(), (btn_st_x, btn_st_y), self.btn_sz, "Select"),
            Action.LINE: Button(turtle.Turtle(), (btn_st_x + btn_gap * 1, btn_st_y), self.btn_sz, "Line"),
            Action.CIRCLE: Button(turtle.Turtle(), (btn_st_x + btn_gap * 2, btn_st_y), self.btn_sz, "Circle"),
            Action.POLYGON: Button(turtle.Turtle(), (btn_st_x + btn_gap * 3, btn_st_y), self.btn_sz, "Polygon"),
            Action.RPOLYGON: Button(turtle.Turtle(), (btn_st_x + btn_gap * 4, btn_st_y), self.btn_sz, "RPolygon"),
            Action.FRACTAL_TRI: Button(turtle.Turtle(), (btn_st_x + btn_gap * 5, btn_st_y), self.btn_sz, "FractalTri"),
        }
        self.action_buttons[Action.SELECT].selected = True
        for _, btn in self.action_buttons.items():
            btn.draw()

        # btn_st_x += len(self.action_buttons.items()) * btn_gap + 20
        btn_st_y += self.btn_sz[1] - self.gap
        self.color_buttons = {
            Color.BLUE: Button(turtle.Turtle(), (btn_st_x + btn_gap * 0, btn_st_y), self.btn_sz, "Blue"),
            Color.RED: Button(turtle.Turtle(), (btn_st_x + btn_gap * 1, btn_st_y), self.btn_sz, "Red"),
            Color.GREEN: Button(turtle.Turtle(), (btn_st_x + btn_gap * 2, btn_st_y), self.btn_sz, "Green"),
            Color.YELLOW: Button(turtle.Turtle(), (btn_st_x + btn_gap * 3, btn_st_y), self.btn_sz, "Yellow"),
            Color.BLACK: Button(turtle.Turtle(), (btn_st_x + btn_gap * 4, btn_st_y), self.btn_sz, "Black"),
        }
        self.color_buttons[Color.BLUE].selected = True

        for _, btn in self.color_buttons.items():
            btn.draw()

    def on_window_resize(self, w, h):
        delta = (-(w - self.w) / 2, (h - self.h) / 2)
        self.w = w
        self.h = h

        for _, btn in self.action_buttons.items():
            btn.move(delta)

        for _, btn in self.color_buttons.items():
            btn.move(delta)

    def click_on_action_button(self, x, y):
        old_act = self.action
        new_act = None
        for act, btn in self.action_buttons.items():
            if btn.inbox((x, y)):
                new_act = act
                break
        if new_act and new_act != old_act:
            self.action = new_act
            self.action_buttons[old_act].set_selection(False)
            self.action_buttons[new_act].set_selection(True)
        return new_act     

    def click_on_color_button(self, x, y):
        old_color = self.color
        new_color = None
        for color, btn in self.color_buttons.items():
            if btn.inbox((x, y)):
                new_color = color
                break
        if new_color and new_color != old_color:
            self.color = new_color
            self.color_buttons[old_color].set_selection(False)
            self.color_buttons[new_color].set_selection(True)
        return new_color     

    def make_line(self, x, y):
        if self.action != Action.LINE:
            return
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_line = Line(pen, (x, y), (x, y))
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
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_circle = Circle(pen, 0, (x, y))
            self.temp_circle.draw()
        elif self.state == State.START:
            self.state = State.END
            self.temp_circle.r = geo.distance(self.temp_circle.center, (x, y)) 
            self.temp_circle.draw()
            self.canvas.shapes.append(self.temp_circle)

    def make_polygon(self, x, y):
        if self.action != Action.POLYGON:
            return
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_polygon = Polygon(pen, [(x, y)])
            self.temp_polygon.draw()
        elif self.state == State.START:
            self.temp_polygon.points.append((x, y))
            self.temp_polygon.draw()
            if self.shift_pressed:
                self.state = State.END
                self.canvas.shapes.append(self.temp_polygon)


    def make_regular_polygon(self, x, y):
        if self.action != Action.RPOLYGON:
            return
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_rpolygon = RegularPolygon(pen, (x, y), 0, 0)
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
        if self.click_on_action_button(x, y):
            if self.action == Action.FRACTAL_TRI:
                self.canvas.create_customized_arts("fractal_triangle")
        elif self.click_on_color_button(x, y):
            # don't draw
            pass
        elif self.action == Action.SELECT:
            self.canvas.select_shapes((x, y), self.shift_pressed)
        elif self.action == Action.LINE:
            self.make_line(x, y)
        elif self.action == Action.CIRCLE:
            self.make_circle(x, y)
        elif self.action == Action.RPOLYGON:
            self.make_regular_polygon(x, y)
        elif self.action == Action.POLYGON:
            self.make_polygon(x, y)

        if self.action != Action.SELECT:
            self.canvas.deselect_all()
        

    def onkeygroup(self):
        self.canvas.combine_selected()

    def onkeycopy(self):
        self.canvas.copy_selected()
        
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

    def onkeyscale(self, key_pressed, magnitude=1):
        key_scale = {
            "w" : 1 + magnitude * 0.01,
            "s" : 1 - magnitude * 0.01,
        }
        for key in key_scale.keys():
            if key == key_pressed:
                self.canvas.scale_selected(key_scale[key])
    
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

    def onkeyclockwisebig(self):
        self.onkeyrotate("d", 10)

    def onkeycounterclockwisebig(self):
        self.onkeyrotate("a", 10)

    def onkeyscaleup(self):
        self.onkeyscale("w")

    def onkeyscaledown(self):
        self.onkeyscale("s")

    def onkeyscaleupbig(self):
        self.onkeyscale("w", 10)

    def onkeyscaledownbig(self):
        self.onkeyscale("s", 10)






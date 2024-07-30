import src.geometry as geo
import turtle, math

class NotImplemented(Exception):
    pass

class Shape():
    def __init__(self, pen: turtle.Turtle) -> None:
        self.selected = False
        self.pen = pen
        self.sr = 5
        self.pen.hideturtle()

    def draw(self):
        pass

    def get_selection_points(self):
        raise NotImplemented("Shape: get_selection_points() is not implemented")

    def draw_selection_points(self):
        for point in self.get_selection_points():
            self.pen.penup()
            self.pen.goto(point[0], point[1] - self.sr/2)
            self.pen.pendown()
            self.pen.circle(self.sr)
            self.pen.penup()

    def clear(self):
        self.pen.clear()

    def point_in_shape(self, point):
        raise NotImplemented("Shape: point_in_shape() is not implemented")
    
    # delta: (dx, dy)
    def translate(self, delta):
        raise NotImplemented("Shape: translate() is not implemented")

    # rotate around center.
    # if center is None, rotate round the shape center
    def rotate(self, angle_in_deg, center=None):
        raise NotImplemented("Shape: rotate() is not implemented")


class Circle(Shape):
    def __init__(self, pen: turtle.Turtle, r, center) -> None:
        super().__init__(pen)
        self.r = r
        self.center = center

    def draw(self):
        self.clear()
        self.pen.penup()
        x0, y0 = self.center
        self.pen.goto(x0, y0 - self.r)
        self.pen.pendown()
        self.pen.circle(self.r)
        self.pen.penup()
        if self.selected and self.r > 0:
            self.draw_selection_points()
    
    def get_selection_points(self):
        x0, y0 = self.center
        points = []
        for i in range(4):
            rnd = i * math.pi / 2
            points.append(
                (
                    x0 + self.r * math.cos(rnd), 
                    y0 + self.r * math.sin(rnd)
                )
            )
        return points


    def point_in_shape(self, point):
        return geo.distance(self.center, point) < self.r
    
    def translate(self, delta):
        self.center = geo.translate(self.center, delta)


class Line(Shape):
    def __init__(self, pen: turtle.Turtle, point1, point2) -> None:
        super().__init__(pen)
        self.point1 = point1
        self.point2 = point2

    def draw(self):
        self.clear()
        self.pen.penup()
        self.pen.goto(self.point1)
        self.pen.pendown()
        self.pen.goto(self.point2)
        self.pen.penup()
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        return [self.point1, self.point2]
    
    def point_in_shape(self, point):
        return geo.distance_point_to_segment(self.point1, self.point2, point) <= 5
    
    def translate(self, delta):
        self.point1 = geo.translate(self.point1, delta)
        self.point2 = geo.translate(self.point2, delta)


class Polygon(Shape):
    def __init__(self, pen: turtle.Turtle, sides) -> None:
        super().__init__()
        self.sides = sides
        self.pen = pen

    def draw(self):
        for side in self.sides:
            self.pen.goto(side)

    def get_selection_points(self):
        return self.sides
    
    def point_in_shape(self, point):
        for side in self.sides:
            bool1 = side[0] > point[0] if side[0] < 0 else side[0] < point[0]
            bool2 = side[1] > point[1] if side[1] < 0 else side[1] < point[1]
            if bool1 or bool2:
                return False         
        return True
    
class RegularPolygon(Shape):
    def __init__(self, pen: turtle.Turtle, center, num_sides, r) -> None:
        super().__init__(pen)
        self.num_sides = num_sides
        self.r = r
        self.center = center

    def draw(self):
        x0, y0 = self.center
        self.clear()
        self.pen.penup()
        self.pen.goto(x0 + self.r, y0)
        self.pen.pendown()
        for point in self.get_selection_points():
            self.pen.goto(point)
        self.pen.penup()
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        points = []
        n = self.num_sides
        theta = 2 * math.pi / n
        x0, y0 = self.center
        for i in range(1, n + 1):
            points.append(
                (
                x0 + self.r * math.cos(theta * i),
                y0 + self.r * math.sin(theta * i)
                )
            )
        return points
    
    def point_in_shape(self, point):
        return geo.distance(self.center, point) < self.r
    
    def translate(self, delta):
        self.center = geo.translate(self.center, delta)
    
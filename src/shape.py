import src.geometry as geo
import turtle, math

class NotImplemented(Exception):
    pass

class Shape():
    def __init__(self, pen: turtle.Turtle) -> None:
        self.selected = False
        self.pen = pen
        self.pen.hideturtle()

    def draw(self):
        pass

    def clear(self):
        self.pen.clear()

    def point_in_shape(self, point):
        raise NotImplemented("Shape: point_in_shape() is not implemented")

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
        if self.selected:
            points = []
            for i in range(4):
                rnd = i * math.pi / 2
                points.append(
                    (
                        x0 + self.r * math.cos(rnd), 
                        y0 + self.r * math.sin(rnd)
                    )
                )
            sr = 5
            for point in points:
                self.pen.penup()
                self.pen.goto(point[0], point[1] - sr/2)
                self.pen.pendown()
                self.pen.circle(sr)
                self.pen.penup()


    def point_in_shape(self, point):
        return geo.distance(self.center, point) < self.r


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
        if self.selected:
            self.pen.circle(2)
        self.pen.goto(self.point2)
        if self.selected:
            self.pen.circle(2)
        self.pen.penup()

    def point_in_shape(self, point):
        return geo.distance_point_to_segment(self.point1, self.point2, point) <= 5


class Polygon(Shape):
    def __init__(self, sides, center, d, deg=0) -> None:
        super().__init__()
        self.sides = sides
        self.d = d
        self.center = center
        self.deg = deg

    def draw(self, pen: turtle):
        dsides = self.sides * 2
        pen.penup()
        pen.goto(self.center)
        pen.pendown()
        for angle in range(dsides):
            pen.goto
            (
                pen.xcor() + self.d * math.sin((angle + self.deg) * ((math.pi * 4) / dsides)), 
                pen.ycor() + self.d * math.cos((angle + self.deg) * ((math.pi * 4) / dsides))
            )
        pen.penup()
    

    
    


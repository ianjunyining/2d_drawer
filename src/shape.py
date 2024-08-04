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

    def _type(self):
        return self.__class__.__name__

    def draw(self):
        pass

    def get_selection_points(self):
        raise NotImplemented(f"{self._type()}: get_selection_points() is not implemented")

    def draw_selection_points(self):
        for point in self.get_selection_points():
            self.pen.penup()
            self.pen.goto(point[0], point[1] - self.sr/2)
            self.pen.pendown()
            self.pen.circle(self.sr)
            self.pen.penup()

    def clear(self):
        self.pen.clear()

    def get_center(self):
        raise NotImplemented(f"{self._type()}: get_center() is not implemented")
        
    def point_in_shape(self, point):
        raise NotImplemented(f"{self._type()}: point_in_shape() is not implemented")
    
    # delta: (dx, dy)
    def translate(self, delta):
        raise NotImplemented(f"{self._type()}: translate() is not implemented")

    # rotate around center.
    # if center is None, rotate round the shape center
    def rotate(self, theta, center=None):
        raise NotImplemented(f"{self._type()}: rotate() is not implemented")

    def scale(self, s):
        raise NotImplemented(f"{self._type()}: scale() is not implemented")

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

    def get_center(self):
        return self.center

    def rotate(self, theta, center=None):
        if center:
            self.center = geo.rotate(self.center, theta, center)

    def scale(self, s):
        self.r *= s


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

    def rotate(self, theta, center=None):
        rotate_center = center if center else self.get_center()
        self.point1 = geo.rotate(self.point1, theta, rotate_center)
        self.point2 = geo.rotate(self.point2, theta, rotate_center)

    def get_center(self):
        center = (
            (self.point1[0] + self.point2[0]) / 2,
            (self.point1[1] + self.point2[1]) / 2,
        )
        return center
    
    def scale(self, s):
        center = self.get_center()
        self.point1 = geo.scale(s, center, self.point1)
        self.point2 = geo.scale(s, center, self.point2)



class RegularPolygon(Shape):
    def __init__(self, pen: turtle.Turtle, center, num_sides, r) -> None:
        super().__init__(pen)
        self.num_sides = num_sides
        self.r = r
        self.center = center
        self.angle = 0

    def draw(self):
        self.clear()
        self.pen.penup()
        pts = self.get_selection_points()
        self.pen.goto(pts[-1])
        self.pen.pendown()
        for point in pts:
            self.pen.goto(point)
        self.pen.penup()
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        points = []
        n = self.num_sides
        theta = 2 * math.pi / n
        x0, y0 = self.center
        for i in range(n):
            points.append(
                (
                x0 + self.r * math.cos(theta * i + self.angle),
                y0 + self.r * math.sin(theta * i + self.angle)
                )
            )
        return points
    
    def point_in_shape(self, point):
        return geo.distance(self.center, point) < self.r
    
    def translate(self, delta):
        self.center = geo.translate(self.center, delta)

    def get_center(self):
        return self.center

    def rotate(self, theta, center=None):
        if center:
            self.center = geo.rotate(self.center, theta, center)
        self.angle += theta
    
    def scale(self, s):
        self.r *= s
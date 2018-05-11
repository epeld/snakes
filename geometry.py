import math

class Cartesian(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_length(self):
        return math.sqrt(self.get_x()**2 +
                         self.get_y()**2)

    def get_omega(self):
        return math.atan2(self.get_y(), self.get_x())

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def scale(self, factor):
        return Cartesian(self.get_x() * factor,
                         self.get_y() * factor)

    def add(self, other):
        x = self.get_x() + other.get_x()
        y = self.get_y() + other.get_y()
        return Cartesian(x, y)

    def sub(self, other):
        x = self.get_x() - other.get_x()
        y = self.get_y() - other.get_y()
        return Cartesian(x, y)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def to_cartesian(self):
        return self.copy()

    def to_tuple(self):
        return (self.get_x(), self.get_y())

    def copy(self):
        return Cartesian(self.get_x(),
                         self.get_y())


class Polar(object):
    def __init__(self, radius, omega):
        self.radius = radius
        self.omega = omega

    def get_length(self):
        return self.radius

    def get_omega(self):
        return self.omega

    def scale(self, factor):
        radius = self.get_length() * factor
        return Polar(radius, self.get_omega())

    def copy(self):
        return Polar(self.get_length(),
                     self.get_omega())

    def add(self, other):
        v = self.to_cartesian()
        v2 = other.to_cartesian()
        v3 = v.add(v2)
        return Polar(v3.get_length(),
                     v3.get_omega())

    def to_cartesian(self):
        r = self.get_length()
        omega = self.get_omega()
        x = r * math.cos(omega)
        y = r * math.sin(omega)
        return Cartesian(x, y)


class Rectangle(object):
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def get_top_left(self):
        return self.top_left

    def get_bottom_right(self):
        return self.bottom_right


def centered_square(point, width):
    height = width
    left_top = point - Cartesian(point.get_x() - width / 2.0,
                                 point.get_y() - height / 2.0)
    right_bottom = point + Cartesian(point.get_x() + width / 2.0,
                                     point.get_y() + height / 2.0)
    return Rectangle(left_top, right_bottom)

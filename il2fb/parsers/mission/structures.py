# -*- coding: utf-8 -*-


class Point2D(object):
    __slots__ = ['x', 'y', ]

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.x, self.y))


class Point3D(object):
    __slots__ = ['x', 'y', 'z', ]

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __eq__(self, other):
        if not isinstance(other, Point3D):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

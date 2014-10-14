# -*- coding: utf-8 -*-


class BaseObject(object):

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return all([
            getattr(self, x) == getattr(other, x)
            for x in self.__slots__
        ])

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(tuple(
            getattr(self, x) for x in self.__slots__
        ))


class Point2D(BaseObject):
    __slots__ = ['x', 'y', ]

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class Point3D(BaseObject):
    __slots__ = ['x', 'y', 'z', ]

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


class GroundRoutePoint(BaseObject):
    __slots__ = ['pos', 'is_checkpoint', 'delay', 'section_length', 'speed', ]

    def __init__(self, pos, is_checkpoint, delay=None, section_length=None,
                 speed=None):
        self.pos = pos
        self.is_checkpoint = is_checkpoint
        self.delay = delay
        self.section_length = section_length
        self.speed = speed


class Building(BaseObject):
    __slots__ = ['id', 'belligerent', 'code', 'pos', 'rotation_angle', ]

    def __init__(self, id, belligerent, code, pos, rotation_angle):
        self.id = id
        self.belligerent = belligerent
        self.code = code
        self.pos = pos
        self.rotation_angle = rotation_angle


class StaticCamera(BaseObject):
    __slots__ = ['belligerent', 'pos', ]

    def __init__(self, belligerent, pos):
        self.belligerent = belligerent
        self.pos = pos


class FrontMarker(BaseObject):
    __slots__ = ['id', 'belligerent', 'pos', ]

    def __init__(self, id, belligerent, pos):
        self.id = id
        self.belligerent = belligerent
        self.pos = pos


class Rocket(BaseObject):
    __slots__ = [
        'id', 'code', 'belligerent', 'pos', 'rotation_angle', 'delay', 'count',
        'period', 'destination',
    ]

    def __init__(self, id, code, belligerent, pos, rotation_angle, delay,
                 count, period, destination):
        self.id = id
        self.code = code
        self.belligerent = belligerent
        self.pos = pos
        self.rotation_angle = rotation_angle
        self.delay = delay
        self.count = count
        self.period = period
        self.destination = destination

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


class GroundRoutePoint(object):
    __slots__ = ['pos', 'is_checkpoint', 'delay', 'section_length', 'speed', ]

    def __init__(self, pos, is_checkpoint, delay=None, section_length=None,
                 speed=None):
        self.pos = pos
        self.is_checkpoint = is_checkpoint
        self.delay = delay
        self.section_length = section_length
        self.speed = speed

    def __eq__(self, other):
        if not isinstance(other, GroundRoutePoint):
            return NotImplemented
        return (
            self.pos == other.pos
            and self.is_checkpoint == other.is_checkpoint
            and self.delay == other.delay
            and self.section_length == other.section_length
            and self.speed == other.speed
        )

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((
            self.pos, self.is_checkpoint, self.delay, self.section_length,
            self.speed,
        ))


class Building(object):
    __slots__ = ['id', 'belligerent', 'code', 'pos', 'rotation_angle', ]

    def __init__(self, id, belligerent, code, pos, rotation_angle):
        self.id = id
        self.belligerent = belligerent
        self.code = code
        self.pos = pos
        self.rotation_angle = rotation_angle

    def __eq__(self, other):
        if not isinstance(other, Building):
            return NotImplemented
        return (
            self.id == other.id
            and self.code == other.code
            and self.belligerent == other.belligerent
            and self.pos == other.pos
            and self.rotation_angle == other.rotation_angle
        )

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((
            self.id, self.code, self.belligerent, self.pos,
            self.rotation_angle,
        ))


class StaticCamera(object):
    __slots__ = ['belligerent', 'pos', ]

    def __init__(self, belligerent, pos):
        self.belligerent = belligerent
        self.pos = pos

    def __eq__(self, other):
        if not isinstance(other, StaticCamera):
            return NotImplemented
        return self.belligerent == other.belligerent and self.pos == other.pos

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.belligerent, self.pos))


class FrontMarker(object):
    __slots__ = ['id', 'belligerent', 'pos', ]

    def __init__(self, id, belligerent, pos):
        self.id = id
        self.belligerent = belligerent
        self.pos = pos

    def __eq__(self, other):
        if not isinstance(other, FrontMarker):
            return NotImplemented
        return (
            self.id == other.id
            and self.belligerent == other.belligerent
            and self.pos == other.pos
        )

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.id, self.belligerent, self.pos))

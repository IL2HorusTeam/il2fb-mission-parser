# -*- coding: utf-8 -*-


class Base(object):
    __slots__ = ()

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


class Point2D(Base):
    __slots__ = ['x', 'y', ]

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "<Point2D '{0};{1}'>".format(self.x, self.y)


class Point3D(Base):
    __slots__ = ['x', 'y', 'z', ]

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return "<Point3D '{0};{1};{2}'>".format(self.x, self.y, self.z)


class GroundRoutePoint(Base):
    __slots__ = ['pos', 'is_checkpoint', 'delay', 'section_length', 'speed', ]

    def __init__(self, pos, is_checkpoint, delay=None, section_length=None,
                 speed=None):
        self.pos = pos
        self.is_checkpoint = is_checkpoint
        self.delay = delay
        self.section_length = section_length
        self.speed = speed

    def __repr__(self):
        return "<GroundRoutePoint '{0};{1}'>".format(self.pos.x, self.pos.y)


class Building(Base):
    __slots__ = ['id', 'belligerent', 'code', 'pos', 'rotation_angle', ]

    def __init__(self, id, belligerent, code, pos, rotation_angle):
        self.id = id
        self.belligerent = belligerent
        self.code = code
        self.pos = pos
        self.rotation_angle = rotation_angle

    def __repr__(self):
        return "<Building '{0}'>".format(self.id)


class StaticCamera(Base):
    __slots__ = ['belligerent', 'pos', ]

    def __init__(self, belligerent, pos):
        self.belligerent = belligerent
        self.pos = pos

    def __repr__(self):
        return (
            "<StaticCamera '{0};{1};{2}'>"
            .format(self.pos.x, self.pos.y, self.pos.z)
        )


class FrontMarker(Base):
    __slots__ = ['id', 'belligerent', 'pos', ]

    def __init__(self, id, belligerent, pos):
        self.id = id
        self.belligerent = belligerent
        self.pos = pos

    def __repr__(self):
        return "<FrontMarker '{0}'>".format(self.id)


class Rocket(Base):
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

    def __repr__(self):
        return "<Rocket '{0}'>".format(self.id)


class StationaryObject(Base):
    __slots__ = [
        'id', 'belligerent', 'code', 'pos', 'rotation_angle', 'type',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type):
        self.id = id
        self.belligerent = belligerent
        self.code = code
        self.pos = pos
        self.rotation_angle = rotation_angle
        self.type = type

    def __repr__(self):
        return "<StationaryObject '{0}'>".format(self.id)


class StationaryArtillery(StationaryObject):
    __slots__ = StationaryObject.__slots__ + [
        'awakening_time', 'range', 'skill', 'use_spotter',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type,
                 awakening_time, range, skill, use_spotter):
        super(StationaryArtillery, self).__init__(
            id, belligerent, code, pos, rotation_angle, type)
        self.awakening_time = awakening_time
        self.range = range
        self.skill = skill
        self.use_spotter = use_spotter


class StationaryAircraft(StationaryObject):
    __slots__ = StationaryObject.__slots__ + [
        'air_force', 'allows_spawning', 'is_restorable', 'skin',
        'show_markings',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type,
                 air_force, allows_spawning, is_restorable, skin,
                 show_markings):
        super(StationaryAircraft, self).__init__(
            id, belligerent, code, pos, rotation_angle, type)
        self.air_force = air_force
        self.allows_spawning = allows_spawning
        self.is_restorable = is_restorable
        self.skin = skin
        self.show_markings = show_markings


class StationaryShip(StationaryObject):
    __slots__ = StationaryObject.__slots__ + [
        'awakening_time', 'recharge_time', 'skill',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type,
                 awakening_time, recharge_time, skill):
        super(StationaryShip, self).__init__(
            id, belligerent, code, pos, rotation_angle, type)
        self.awakening_time = awakening_time
        self.recharge_time = recharge_time
        self.skill = skill


class FlightRoutePoint(Base):
    __slots__ = ['type', 'pos', 'speed', 'formation', 'radio_silence', ]

    def __init__(self, type, pos, speed, formation, radio_silence):
        self.type = type
        self.pos = pos
        self.speed = speed
        self.formation = formation
        self.radio_silence = radio_silence

    def __repr__(self):
        return (
            "<FlightRoutePoint '{0};{1};{2}'>"
            .format(self.pos.x, self.pos.y, self.pos.z)
        )


class FlightRouteTakeoffPoint(FlightRoutePoint):
    __slots__ = FlightRoutePoint.__slots__ + ['delay', 'spacing', ]

    def __init__(self, type, pos, speed, formation, radio_silence, delay,
                 spacing):
        super(FlightRouteTakeoffPoint, self).__init__(
            type, pos, speed, formation, radio_silence)
        self.delay = delay
        self.spacing = spacing


class FlightRoutePatrolPoint(FlightRoutePoint):
    __slots__ = FlightRoutePoint.__slots__ + [
        'patrol_cycles', 'patrol_timeout',
        'pattern_angle', 'pattern_side_size', 'pattern_altitude_difference',
    ]

    def __init__(self, type, pos, speed, formation, radio_silence,
                 patrol_cycles, patrol_timeout, pattern_angle,
                 pattern_side_size, pattern_altitude_difference):
        super(FlightRoutePatrolPoint, self).__init__(
            type, pos, speed, formation, radio_silence)
        self.patrol_cycles = patrol_cycles
        self.patrol_timeout = patrol_timeout
        self.pattern_angle = pattern_angle
        self.pattern_side_size = pattern_side_size
        self.pattern_altitude_difference = pattern_altitude_difference


class FlightRouteAttackPoint(FlightRoutePoint):
    __slots__ = FlightRoutePoint.__slots__ + [
        'target_id', 'target_route_point',
    ]

    def __init__(self, type, pos, speed, formation, radio_silence, target_id,
                 target_route_point):
        super(FlightRouteAttackPoint, self).__init__(
            type, pos, speed, formation, radio_silence)
        self.target_id = target_id
        self.target_route_point = target_route_point

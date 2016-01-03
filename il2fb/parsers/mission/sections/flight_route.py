# -*- coding: utf-8 -*-

from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.spatial import Point3D
from il2fb.commons.structures import BaseStructure

from ..constants import (
    ROUTE_POINT_EXTRA_PARAMETERS_MARK, ROUTE_POINT_RADIO_SILENCE_ON,
    ROUTE_POINT_RADIO_SILENCE_OFF,
)

from . import CollectingParser


class FlightRoutePoint(BaseStructure):
    __slots__ = ['type', 'pos', 'speed', 'formation', 'radio_silence', ]

    def __init__(self, type, pos, speed, formation, radio_silence):
        self.type = type
        self.pos = pos
        self.speed = speed
        self.formation = formation
        self.radio_silence = radio_silence

    def __repr__(self):
        return ("<{0} '{1};{2};{3}'>"
                .format(self.__class__.__name__,
                        self.pos.x, self.pos.y, self.pos.z))


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


class FlightRouteParser(CollectingParser):
    """
    Parses ``*_Way`` section.
    View :ref:`detailed description <flight-route-section>`.
    """
    input_suffix = "_Way"
    output_prefix = 'flight_route_'

    def check_section_name(self, section_name):
        return section_name.endswith(self.input_suffix)

    def _extract_flight_code(self, section_name):
        return section_name[:-len(self.input_suffix)]

    def init_parser(self, section_name):
        super(FlightRouteParser, self).init_parser(section_name)
        flight_code = self._extract_flight_code(section_name)
        self.output_key = "{}{}".format(self.output_prefix, flight_code)
        self.point = None
        self.point_class = None

    def parse_line(self, line):
        params = line.split()
        type_code, params = params[0], params[1:]
        if type_code == ROUTE_POINT_EXTRA_PARAMETERS_MARK:
            self._parse_options(params)
        else:
            self._finalize_current_point()
            pos, speed, params = params[0:3], params[3], params[4:]
            self.point = {
                'type': RoutePointTypes.get_by_value(type_code),
                'pos': Point3D(*pos),
                'speed': float(speed),
            }
            self._parse_extra(params)

    def _parse_options(self, params):
        try:
            cycles, timeout, angle, side_size, altitude_difference = params
            self.point.update({
                'patrol_cycles': int(cycles),
                'patrol_timeout': int(timeout),
                'pattern_angle': int(angle),
                'pattern_side_size': int(side_size),
                'pattern_altitude_difference': int(altitude_difference),
            })
            self.point_class = FlightRoutePatrolPoint
        except ValueError:
            delay, spacing = params[1:3]
            self.point.update({
                'delay': int(delay),
                'spacing': int(spacing),
            })
            self.point_class = FlightRouteTakeoffPoint

    def _parse_extra(self, params):
        if FlightRouteParser._is_new_game_version(params):
            radio_silence, formation, params = FlightRouteParser._parse_new_version_extra(params)
            if params:
                self._parse_target(params)
        else:
            radio_silence = False
            formation = None

        self.point.update({
            'radio_silence': radio_silence,
            'formation': formation,
        })

    @staticmethod
    def _is_new_game_version(params):
        return (
            ROUTE_POINT_RADIO_SILENCE_ON in params
            or ROUTE_POINT_RADIO_SILENCE_OFF in params
        )

    @staticmethod
    def _parse_new_version_extra(params):
        try:
            index = params.index(ROUTE_POINT_RADIO_SILENCE_ON)
        except ValueError:
            index = params.index(ROUTE_POINT_RADIO_SILENCE_OFF)

        params, radio_silence, extra = params[:index], params[index], params[index+1:]

        radio_silence = radio_silence == ROUTE_POINT_RADIO_SILENCE_ON
        formation = Formations.get_by_value(extra[0]) if extra else None

        return radio_silence, formation, params

    def _parse_target(self, params):
        target_id, target_route_point = params[:2]

        self.point.update({
            'target_id': target_id,
            'target_route_point': int(target_route_point),
        })

        if self.point['type'] is RoutePointTypes.normal:
            self.point['type'] = RoutePointTypes.air_attack

        self.point_class = FlightRouteAttackPoint

    def clean(self):
        self._finalize_current_point()
        return {self.output_key: self.data}

    def _finalize_current_point(self):
        if self.point:
            point_class = getattr(self, 'point_class') or FlightRoutePoint
            self.data.append(point_class(**self.point))
            self.point = None
            self.point_class = None

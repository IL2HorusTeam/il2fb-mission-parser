# -*- coding: utf-8 -*-

from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.organization import AirForces, Regiments
from il2fb.commons.spatial import Point3D
from il2fb.commons.structures import BaseStructure

from ..constants import (
    ROUTE_POINT_EXTRA_PARAMETERS_MARK, ROUTE_POINT_RADIO_SILENCE_ON,
    ROUTE_POINT_RADIO_SILENCE_OFF,
)
from ..converters import to_skill
from . import CollectingParser, ValuesParser


class WingSectionParser(CollectingParser):
    """
    Parses ``Wing`` section.
    View :ref:`detailed description <wing-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Wing"

    def clean(self):
        return {'wings': self.data}


class WingInfoSectionParser(ValuesParser):
    """
    Parses settings for a moving wing group.
    View :ref:`detailed description <wing-info-section>`.
    """

    def check_section_name(self, section_name):
        try:
            self._decompose_section_name(section_name)
        except Exception:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(WingInfoSectionParser, self).init_parser(section_name)
        self.output_key = section_name
        self.wing_info = self._decompose_section_name(section_name)

    def _decompose_section_name(self, section_name):
        prefix = section_name[:-2]
        squadron, wing = section_name[-2:]

        try:
            regiment = None
            air_force = AirForces.get_by_flight_prefix(prefix)
        except ValueError:
            regiment = Regiments.get_by_code_name(prefix)
            air_force = regiment.air_force

        return {
            'id': section_name,
            'air_force': air_force,
            'regiment': regiment,
            'squadron_index': int(squadron),
            'wing_index': int(wing),
        }

    def clean(self):
        count = int(self.data['Planes'])
        code = self.data['Class'].split('.', 1)[1]
        aircrafts = []

        def _add_if_present(target, key, value):
            if value:
                target[key] = value

        for i in range(count):
            aircraft = {
                'index': i,
                'has_markings': self._has_markings(i),
                'skill': self._get_skill(i),
            }
            _add_if_present(
                aircraft, 'aircraft_skin', self._get_skin('skin', i))
            _add_if_present(
                aircraft, 'nose_art', self._get_skin('nose_art', i))
            _add_if_present(
                aircraft, 'pilot_skin', self._get_skin('pilot', i))
            _add_if_present(
                aircraft, 'spawn_object', self._get_spawn_object_id(i))
            aircrafts.append(aircraft)

        self.wing_info.update({
            'ai_only': 'OnlyAI' in self.data,
            'aircrafts': aircrafts,
            'code': code,
            'fuel': int(self.data['Fuel']),
            'with_parachutes': 'Parachute' not in self.data,
            'count': count,
            'weapons': self.data['weapons'],
        })

        return {self.output_key: self.wing_info}

    def _get_skill(self, aircraft_id):
        if 'Skill' in self.data:
            return to_skill(self.data['Skill'])
        else:
            return to_skill(self.data['Skill{:}'.format(aircraft_id)])

    def _has_markings(self, aircraft_id):
        return 'numberOn{:}'.format(aircraft_id) not in self.data

    def _get_skin(self, prefix, aircraft_id):
        return self.data.get('{:}{:}'.format(prefix, aircraft_id))

    def _get_spawn_object_id(self, aircraft_id):
        return self.data.get('spawn{:}'.format(aircraft_id))


class WingRoutePoint(BaseStructure):
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


class WingRouteTakeoffPoint(WingRoutePoint):
    __slots__ = WingRoutePoint.__slots__ + ['delay', 'spacing', ]

    def __init__(self, type, pos, speed, formation, radio_silence, delay,
                 spacing):
        super(WingRouteTakeoffPoint, self).__init__(
            type, pos, speed, formation, radio_silence)
        self.delay = delay
        self.spacing = spacing


class WingRoutePatrolPoint(WingRoutePoint):
    __slots__ = WingRoutePoint.__slots__ + [
        'patrol_cycles', 'patrol_timeout',
        'pattern_angle', 'pattern_side_size', 'pattern_altitude_difference',
    ]

    def __init__(self, type, pos, speed, formation, radio_silence,
                 patrol_cycles, patrol_timeout, pattern_angle,
                 pattern_side_size, pattern_altitude_difference):
        super(WingRoutePatrolPoint, self).__init__(
            type, pos, speed, formation, radio_silence)
        self.patrol_cycles = patrol_cycles
        self.patrol_timeout = patrol_timeout
        self.pattern_angle = pattern_angle
        self.pattern_side_size = pattern_side_size
        self.pattern_altitude_difference = pattern_altitude_difference


class WingRouteAttackPoint(WingRoutePoint):
    __slots__ = WingRoutePoint.__slots__ + [
        'target_id', 'target_route_point',
    ]

    def __init__(self, type, pos, speed, formation, radio_silence, target_id,
                 target_route_point):
        super(WingRouteAttackPoint, self).__init__(
            type, pos, speed, formation, radio_silence)
        self.target_id = target_id
        self.target_route_point = target_route_point


class WingRouteSectionParser(CollectingParser):
    """
    Parses ``*_Way`` section.
    View :ref:`detailed description <wing-route-section>`.
    """
    input_suffix = "_Way"
    output_prefix = 'wing_route_'

    def check_section_name(self, section_name):
        return section_name.endswith(self.input_suffix)

    def _extract_wing_code(self, section_name):
        return section_name[:-len(self.input_suffix)]

    def init_parser(self, section_name):
        super(WingRouteSectionParser, self).init_parser(section_name)
        wing_code = self._extract_wing_code(section_name)
        self.output_key = "{}{}".format(self.output_prefix, wing_code)
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
            self.point_class = WingRoutePatrolPoint
        except ValueError:
            delay, spacing = params[1:3]
            self.point.update({
                'delay': int(delay),
                'spacing': int(spacing),
            })
            self.point_class = WingRouteTakeoffPoint

    def _parse_extra(self, params):
        if WingRouteSectionParser._is_new_game_version(params):
            radio_silence, formation, params = WingRouteSectionParser._parse_new_version_extra(params)
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

        self.point_class = WingRouteAttackPoint

    def clean(self):
        self._finalize_current_point()
        return {self.output_key: self.data}

    def _finalize_current_point(self):
        if self.point:
            point_class = getattr(self, 'point_class') or WingRoutePoint
            self.data.append(point_class(**self.point))
            self.point = None
            self.point_class = None

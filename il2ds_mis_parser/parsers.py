# -*- coding: utf-8 -*-
"""
Parsers of whole missions files and separate sections.
"""
import datetime
import math

from abc import ABCMeta, abstractmethod

from il2ds_mis_parser.constants import *


def to_bool(value):
    """
    Converts a string representation of a number into boolean.

    :param str value: a string representation of a number to convert

    :returns: `False` if `value` is equal to `'0'`, `True` otherwise
    :rtype: :class:`bool`

    **Examples:**

    .. code-block:: python

       >>> to_bool('0')
       False
       >>> to_bool('1')
       True
       >>> to_bool('-1')
       True
    """
    return value != '0'


def to_pos(x, y, z=None):
    """
    Converts a string representation of position coordinates into dictionary.

    :param str x: a string representation of x coordinate
    :param str y: a string representation of y coordinate
    :param z: a string representation of z coordinate
    :type z: str or None

    :returns: a dictionary of float coordinates which can be accessed by their
              names
    :rtype: :class:`dict`

    **Examples:**

    .. code-block:: python

       >>> to_pos('100', '200')
       {'y': 200.0, 'x': 100.0}
       >>> to_pos('100', '200', '300')
       {'y': 200.0, 'x': 100.0, 'z': 300.0}
    """
    pos = {
        'x': float(x),
        'y': float(y),
    }
    if z is not None:
        pos['z'] = float(z)
    return pos


class SectionParser(object):
    """
    Abstract base parser of sections in mission file.
    """

    __metaclass__ = ABCMeta

    running = False
    data = None

    def start(self, section_name):
        """
        Try to start parser. Return 'True' if 'section_name' fits parser or
        'False' otherwise.
        """
        result = self.check_section_name(section_name)
        if result:
            self.running = True
            self.init_parser(section_name)
        return result

    @abstractmethod
    def check_section_name(self, section_name):
        """
        Return 'True' if 'section_name' can be parsed or 'False' otherwise.
        """

    @abstractmethod
    def init_parser(self, section_name):
        """
        Prepare to parse section.
        """

    @abstractmethod
    def parse_line(self, line):
        """
        Parse incoming line.
        """

    def stop(self):
        """
        Stop serction parsing and return processed data.
        """
        if not self.running:
            raise RuntimeError("Cannot stop parser which is not running")

        self.running = False
        return self.process_data()

    def process_data(self):
        """
        Return fully parsed data.
        """
        return self.data


class ValuesParser(SectionParser):

    def init_parser(self, section_name):
        self.data = {}

    def parse_line(self, line):
        code, value = line.split()
        self.data.update({code: value})


class CollectingParser(SectionParser):

    def init_parser(self, section_name):
        self.data = []

    def parse_line(self, line):
        self.data.append(line)


class MainParser(ValuesParser):
    """
    Parses 'MAIN' section.
    """

    def check_section_name(self, section_name):
        return section_name == "MAIN"

    def _to_time(self, value):
        time = float(self.data['TIME'])
        minutes, hours = math.modf(time)
        return datetime.time(int(hours), int(minutes*60))

    def process_data(self):
        return {
            'loader': self.data['MAP'],
            'time': self._to_time(self.data['TIME']),
            'weather_type': WEATHER_TYPES[self.data['CloudType']],
            'clouds_height': float(self.data['CloudHeight']),
            'army_code': ARMIES_NAME[self.data['army']],
            'player_regiment': self.data['playerNum'],
        }


class SeasonParser(ValuesParser):
    """
    Parses 'SEASON' section.
    """

    def check_section_name(self, section_name):
        return section_name == "SEASON"

    def process_data(self):
        date = datetime.date(int(self.data['Year']),
                             int(self.data['Month']),
                             int(self.data['Day']))
        return {'date': date, }


class WeatherParser(ValuesParser):
    """
    Parses 'WEATHER' section.
    """

    def check_section_name(self, section_name):
        return section_name == "WEATHER"

    def process_data(self):
        return {
            'weather': {
                'wind': {
                    'direction': float(self.data['WindDirection']),
                    'speed': float(self.data['WindSpeed']),
                },
                'gust': int(self.data['Gust']),
                'turbulence': int(self.data['Turbulence']),
            },
        }


class MDSParser(ValuesParser):
    """
    Parses 'MDS' section.
    """

    def check_section_name(self, section_name):
        return section_name == "MDS"

    def parse_line(self, line):
        super(MDSParser, self).parse_line(line.replace('MDS_', ''))

    def process_data(self):
        return {
            'radar': {
                'advance_mode': to_bool(self.data['Radar_SetRadarToAdvanceMode']),
                'vectoring': not to_bool(self.data['Radar_DisableVectoring']),
                'ships': {
                    'big': {
                        'max_range': int(self.data['Radar_ShipRadar_MaxRange']),
                        'min_height': int(self.data['Radar_ShipRadar_MinHeight']),
                        'max_height': int(self.data['Radar_ShipRadar_MaxHeight']),
                    },
                    'small': {
                        'max_range': int(self.data['Radar_ShipSmallRadar_MaxRange']),
                        'min_height': int(self.data['Radar_ShipSmallRadar_MinHeight']),
                        'max_height': int(self.data['Radar_ShipSmallRadar_MaxHeight']),
                    },
                },
                'scouts': {
                    'treat_as_radar': to_bool(self.data['Radar_ScoutsAsRadar']),
                    'max_range': int(self.data['Radar_ScoutRadar_MaxRange']),
                },
            },
            'ai': {
                'no_radio_chatter': to_bool(self.data['Misc_DisableAIRadioChatter']),
                'hide_planes_after_landing': to_bool(self.data['Misc_DespawnAIPlanesAfterLanding']),
            },
            'bomb_crater_visibility_muptipliers': {
                'le_100kg': float(self.data['Misc_BombsCat1_CratersVisibilityMultiplier']),
                'le_1000kg': float(self.data['Misc_BombsCat2_CratersVisibilityMultiplier']),
                'gt_1000kg': float(self.data['Misc_BombsCat3_CratersVisibilityMultiplier']),
            },
            'no_players_count_on_home_base': to_bool(self.data['Misc_HidePlayersCountOnHomeBase']),
        }


class RespawnTimeParser(ValuesParser):
    """
    Parses 'RespawnTime' section.
    """

    def check_section_name(self, section_name):
        return section_name == "RespawnTime"

    def process_data(self):
        return {
            'respawn_time': {
                'ship': {
                    'big': int(self.data['Bigship']),
                    'small': int(self.data['Ship']),
                },
                'balloon': int(self.data['Aeroanchored']),
                'artillery': int(self.data['Artillery']),
                'searchlight': int(self.data['Searchlight']),
            },
        }


class ChiefsParser(CollectingParser):
    """
    Parses 'Chiefs' section.
    """

    def check_section_name(self, section_name):
        return section_name == "Chiefs"

    def parse_line(self, line):
        params = line.split()
        (code, type_code, army_code), params = params[0:3], params[3:]
        chief_type, code_name = type_code.split('.')
        chiefs = {
            'code': code,
            'code_name': code_name,
            'type': chief_type.lower(),
            'army_code': ARMIES_NAME[army_code],
        }
        if params:
            timeout, skill, recharge_time = params
            chiefs.update({
                'timeout': int(timeout),
                'skill': SKILLS[skill],
                'recharge_time': float(recharge_time),
            })
        self.data.append(chiefs)

    def process_data(self):
        return {'chiefs': self.data, }


class ChiefRoadParser(CollectingParser):
    """
    Parses 'N_Chief_Road' section.
    """
    suffix = "_Road"

    def check_section_name(self, section_name):
        if not section_name.endswith(self.suffix):
            return False
        try:
            self._extract_object_code(section_name)
        except ValueError:
            return False
        else:
            return True

    def _extract_object_code(self, section_name):
        return section_name.rstrip(self.suffix).lower()

    def init_parser(self, section_name):
        super(ChiefRoadParser, self).init_parser(section_name)
        self.output_key = "{}_road".format(self._extract_object_code(section_name))

    def parse_line(self, line):
        params = line.split()
        pos_x, pos_y, timeout = params[0], params[1], params[3:4]
        chief_road = {
            'pos': to_pos(pos_x, pos_y),
        }
        if timeout:
            chief_road.update({
                'timeout': int(timeout[0]),
            })
        self.data.append(chief_road)

    def process_data(self):
        return {self.output_key: self.data}


class NStationaryParser(CollectingParser):
    """
    Parses 'NStationary' section.
    """
    def init_parser(self, section_name):
        super(NStationaryParser, self).init_parser(section_name)
        self.subparsers = {
            STATIONARY_TYPE_ARTILLERY: self._parse_artillery,
            STATIONARY_TYPE_PLANES: self._parse_planes,
            STATIONARY_TYPE_SHIPS: self._parse_ships,
        }

    def check_section_name(self, section_name):
        return section_name == "NStationary"

    def parse_line(self, line):
        params = line.split()
        code, stationary_object, army_code, pos, rotation_angle, params = params[0], params[1], params[2], \
                                                                   params[3:5], params[5], params[7:]
        static = ({
            'code': code,
            'code_name': self._get_code_name(stationary_object),
            'army_code': ARMIES_NAME[army_code],
            'pos': to_pos(*pos),
            'rotation_angle': float(rotation_angle),
        })
        subparser = self.subparsers.get(self._get_subparser_name(stationary_object))
        if subparser:
            static.update(subparser(params))
        self.data.append(static)

    def _get_subparser_name(self, subparser_name):
        if subparser_name.startswith('ships'):
            return "ships"
        else:
            return subparser_name[subparser_name.index('.')+1:subparser_name.rindex('.')]

    def _get_code_name(self, code):
        return code[code.index('$')+1:]

    def _parse_artillery(self, params):
        """
        Parse additional options category "artillery"
        """
        distance, skill, spotter = params
        return {
            'range': int(distance),
            'skill': SKILLS[skill],
            'is_spotter': spotter,
        }

    def _parse_planes(self, params):
        """
        Parse additional options category "planes"
        """
        (air_force, allows_spawning_restorable), (camouflage, markings) = params[:2], params[3:]
        return {
            'air_force': AIR_FORCES[air_force],
            'allows_spawning': to_bool(allows_spawning_restorable),
            'restorable': allows_spawning_restorable == '2',
            'skin': camouflage,
            'markings': to_bool(markings),
        }

    def _parse_ships(self, params):
        """
        Parse additional options category "ships"
        """
        timeout, skill, overcharge_time = params
        return {
            'timeout': int(timeout),
            'skill': SKILLS[skill],
            'overcharge_time': float(overcharge_time),
        }

    def process_data(self):
        return {'statics': self.data, }


class BuildingsParser(CollectingParser):
    """
    Parses 'Buildings' section.
    """

    def check_section_name(self, section_name):
        return section_name == "Buildings"

    def parse_line(self, line):
        buildings = {}
        code, building_object, army_code, pos_x, pos_y, rotation_angle = line.split()
        building_type, code_name = building_object.split('$')
        buildings.update({
            'code': code,
            'army_code': ARMIES_NAME[army_code],
            'pos': to_pos(pos_x, pos_y),
            'rotation_angle': float(rotation_angle),
        })
        buildings.update(self._decompose_building_object(building_object))
        self.data.append(buildings)

    def _decompose_building_object(self, building_object):
        building_type, code_name = building_object.split('$')
        return {
            'type': building_type,
            'code_name': code_name,
        }

    def process_data(self):
        return {'buildings': self.data, }


class TargetParser(CollectingParser):
    """
    Parses 'Target' section.
    """

    def check_section_name(self, section_name):
        return section_name == "Target"

    def init_parser(self, section_name):
        super(TargetParser, self).init_parser(section_name)
        self.subparsers = {
            TARGET_TYPE_DESTROY: self._parse_destroy_or_cover_or_escort,
            TARGET_TYPE_DESTROY_BRIDGE: self._parse_destroy_or_cover_bridge,
            TARGET_TYPE_DESTROY_AREA: self._parse_destroy_or_cover_area,
            TARGET_TYPE_RECON: self._parse_recon,
            TARGET_TYPE_ESCORT: self._parse_destroy_or_cover_or_escort,
            TARGET_TYPE_COVER: self._parse_destroy_or_cover_or_escort,
            TARGET_TYPE_COVER_AREA: self._parse_destroy_or_cover_area,
            TARGET_TYPE_COVER_BRIDGE: self._parse_destroy_or_cover_bridge,
        }

    def parse_line(self, line):
        params = line.split()
        (type_code, priority, sleep_mode, timeout), params = params[:4], params[4:]
        target = {
            'type': TARGET_TYPES[type_code],
            'priority': TARGET_PRIORITIES[priority],
            'sleep_mode': to_bool(sleep_mode),
            'timeout': int(timeout),
        }
        subparser = self.subparsers.get(type_code)
        target.update(subparser(params))
        self.data.append(target)

    def _to_destruction_level(self, value):
        return int(value) / 10

    def _parse_destroy_or_cover_or_escort(self, params):
        """
        Parse extra parameters for targets with type 'destroy' or 'cover' or
        'escort'.
        """
        (destruction_level, pos_x, pos_y), object_code = params[:3], params[5]
        return {
            'object_code': object_code,
            'destruction_level': self._to_destruction_level(destruction_level),
            'pos': to_pos(pos_x, pos_y),
        }

    def _parse_destroy_or_cover_bridge(self, params):
        """
        Parse extra parameters for targets with type 'destroy bridge' or
        'cover bridge'.
        """
        (pos_x, pos_y), object_code = params[1:3], params[5]
        return {
            'object_code': object_code,
            'pos': to_pos(pos_x, pos_y),
        }

    def _parse_destroy_or_cover_area(self, params):
        """
        Parse extra parameters for targets with type 'destroy area' or
        'cover area'.
        """
        destruction_level, pos_x, pos_y = params[:3]
        return {
            'destruction_level': self._to_destruction_level(destruction_level),
            'pos': to_pos(pos_x, pos_y),
        }

    def _parse_recon(self, params):
        """
        Parse extra parameters for targets with type 'recon.
        """
        (requires_landing, pos_x, pos_y, radius) = params[:4]

        data = {
            'radius': int(radius),
            'requires_landing': requires_landing != '500',
            'pos': to_pos(pos_x, pos_y),
        }

        object_code = params[5:6]
        if object_code:
            (data['object_code'], ) = object_code

        return data

    def process_data(self):
        return {'targets': self.data, }


class BornPlaceParser(CollectingParser):
    """
    Parses 'BornPlace' section.
    """
    def check_section_name(self, section_name):
        return section_name == "BornPlace"

    def parse_line(self, line):
        (army_code, radius, pos_x, pos_y, parachute, air_spawn_height,
         air_spawn_speed, air_spawn_heading, max_allowed_pilots,
         recon_min_height, recon_max_height, recon_range, air_spawn_always,
         enable_aircraft_limits, aircraft_limits_consider_lost,
         disable_spawning, friction_enabled, friction_value,
         aircraft_limits_consider_destroyed_stationary, show_default_icon,
         air_spawn_if_deck_is_full, spawn_in_stationary,
         return_to_start_position) = line.split()

        self.data.append({
            'radius': int(radius),
            'army_code': ARMIES_NAME[army_code],
            'show_default_icon': to_bool(show_default_icon),
            'friction': {
                'enabled': to_bool(friction_enabled),
                'value': float(friction_value),
            },
            'spawning': {
                'enabled': not to_bool(disable_spawning),
                'return_to_start_position': to_bool(return_to_start_position),
                'parachute': to_bool(parachute),
                'max_allowed_pilots': int(max_allowed_pilots),
                'aircraft_limits': {
                    'enabled': to_bool(enable_aircraft_limits),
                    'consider_lost': to_bool(aircraft_limits_consider_lost),
                    'consider_destroyed_stationary': to_bool(aircraft_limits_consider_destroyed_stationary),
                },
                'in_stationary': to_bool(spawn_in_stationary),
                'in_air': {
                    'height': int(air_spawn_height),
                    'speed': int(air_spawn_speed),
                    'heading': int(air_spawn_heading),
                    'conditions': {
                        'always': to_bool(air_spawn_always),
                        'if_deck_is_full': to_bool(air_spawn_if_deck_is_full),
                    },
                },
            },
            'recon': {
                'range': int(recon_range),
                'min_height': int(recon_min_height),
                'max_height': int(recon_max_height),
            },
            'pos': to_pos(pos_x, pos_y),
        })

    def process_data(self):
        return {'homebases': self.data, }


class BornPlaceAircraftsParser(CollectingParser):
    """
    Parses 'BornPlaceN' section.
    """
    prefix = "BornPlace"

    def check_section_name(self, section_name):
        if not section_name.startswith(self.prefix):
            return False
        try:
            self._extract_section_number(section_name)
        except ValueError:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(BornPlaceAircraftsParser, self).init_parser(section_name)
        self.output_key = 'homebase_aircrafts_{0}'.format(
                           self._extract_section_number(section_name))
        self.aircraft = {}

    def _extract_section_number(self, section_name):
        return int(section_name.lstrip(self.prefix))

    def parse_line(self, line):
        chunks = line.split()

        if chunks[0] == '+':
            self.aircraft['loadout'].extend(chunks[1:])
        else:
            if self.aircraft:
                self.data.append(self.aircraft)
            (aircraft_code, limit), loadout = chunks[:2], chunks[2:]
            self.aircraft = {
                'aircraft_code': aircraft_code,
                'limit': self._to_limit(limit),
                'loadout': loadout,
            }

    def process_data(self):
        if self.aircraft:
            self.data.append(self.aircraft)
        return {self.output_key: self.data, }

    def _to_limit(self, value):
        return int(value) if int(value) >= 0 else None


class BornPlaceCountriesParser(CollectingParser):
    """
    Parses 'BornPlaceCountriesN' section.
    """
    prefix = "BornPlaceCountries"

    def check_section_name(self, section_name):
        if not section_name.startswith(self.prefix):
            return False
        try:
            self._extract_section_number(section_name)
        except ValueError:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(BornPlaceCountriesParser, self).init_parser(section_name)
        self.output_key = 'homebase_countries_{0}'.format(
                           self._extract_section_number(section_name))
        self.countries = {}

    def _extract_section_number(self, section_name):
        return int(section_name.lstrip(self.prefix))

    def process_data(self):
        return {self.output_key: self.data, }


class StaticCameraParser(CollectingParser):
    """
    Parses 'StaticCamera' section.
    """

    def check_section_name(self, section_name):
        return section_name == "StaticCamera"

    def parse_line(self, line):
        pos_x, pos_y, pos_z, army_code = line.split()
        self.data.append({
            'army_code': ARMIES_NAME[army_code],
            'pos': to_pos(pos_x, pos_y, pos_z),
        })

    def process_data(self):
        return {'cameras': self.data, }


class BridgeParser(CollectingParser):
    """
    Parses 'Bridge' section.
    """

    def check_section_name(self, section_name):
        return section_name == "Bridge"

    def parse_line(self, line):
        pass

    def process_data(self):
        return {'bridges': self.data, }


class HouseParser(CollectingParser):
    """
    Parses 'House' section.
    """

    def check_section_name(self, section_name):
        return section_name == "House"

    def parse_line(self, line):
        pass

    def process_data(self):
        return {'houses': self.data, }


class FrontMarkerParser(CollectingParser):
    """
    Parses 'FrontMarker' section.
    """

    def check_section_name(self, section_name):
        return section_name == "FrontMarker"

    def parse_line(self, line):
        code, pos_x, pos_y, army_code = line.split()
        self.data.append({
            'code': code,
            'army_code': ARMIES_NAME[army_code],
            'pos': to_pos(pos_x, pos_y),
        })

    def process_data(self):
        return {'markers': self.data, }


class RocketParser(CollectingParser):
    """
    Parses 'Rocket' section.
    """

    def check_section_name(self, section_name):
        return section_name == "Rocket"

    def parse_line(self, line):
        params = line.split()
        (code, code_name, army_code), pos, \
        (rotation_angle, timeout, amount, period), target_pos = params[0:3], params[3:5], params[5:9], params[9:]
        self.data.append({
            'code': code,
            'code_name': code_name,
            'army_code': ARMIES_NAME[army_code],
            'pos': to_pos(*pos),
            'rotation_angle': float(rotation_angle),
            'timeout': float(timeout),
            'amount': int(amount),
            'period': float(period),
            'target_pos': to_pos(*target_pos) if target_pos else None
        })

    def process_data(self):
        return {'rocket': self.data}


class FileParser(object):
    """
    Parses whole mission files.
    """
    def __init__(self):
        self.data = {}
        self.parsers = [
            MainParser(),
            SeasonParser(),
            WeatherParser(),
            MDSParser(),
            RespawnTimeParser(),
            ChiefsParser(),
            NStationaryParser(),
            BuildingsParser(),
            TargetParser(),
            BornPlaceParser(),
            StaticCameraParser(),
            BridgeParser(),
            HouseParser(),
            FrontMarkerParser(),
            RocketParser(),
        ]

    def parse(self, file_path):
        parser = None

        def safely_stop_parser():
            if parser:
                self.data.update(parser.stop())

        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if self.has_section_name(line):
                    safely_stop_parser()
                    section_name = self.get_section_name(line)
                    parser = self.get_parser(section_name)
                elif parser:
                    parser.parse_line(line)
            safely_stop_parser()

        return self.process_data()

    def has_section_name(self, line):
        return line.startswith('[') and line.endswith(']')

    def get_section_name(self, line):
        return line.strip('[]')

    def get_parser(self, section_name):
        for parser in self.parsers:
            if parser.start(section_name):
                return parser
        return None

    def process_data(self):
        # TODO:
        return self.data

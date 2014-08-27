# -*- coding: utf-8 -*-
"""
This module provides a set of parsers which can be used to obtain information
about IL-2 FB missions. Every parser is a one-pass parser. They can be used to
parse a whole mission file or to parse a single given section as well.
"""
import datetime
import math

from abc import ABCMeta, abstractmethod

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.organization import AirForces, Belligerents
from il2fb.commons.targets import TargetTypes, TargetPriorities
from il2fb.commons.weather import Conditions, Gust, Turbulence

from il2fb.parsers.mission.helpers import _
from il2fb.parsers.mission.constants import (
    WAY_POINT_TYPES, WAY_POINT_FORMATIONS,
)


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
    :type z: :class:`str` or ``None``

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


to_belligerent = lambda value: Belligerents.get_by_value(int(value))
to_skill = lambda value: Skills.get_by_value(int(value))
to_unit_type = lambda value: UnitTypes.get_by_value(value.lower())


class SectionParser(object):
    """
    Abstract base parser of a single section in a mission file.

    A common approach to parse a section can be described in the following way:

    #. Pass a section name (e.g. 'MAIN') to :meth:`start` method. If parser can
       process a section with such name, it will return `True` and then you can
       proceed.
    #. Pass section lines one-by-one to :meth:`parse_line`.
    #. When you are done, get your parsed data by calling :meth:`stop`. This
       will tell the parser that no more data will be given and the parsing can
       be finished.

    |
    **Example**:

    .. code-block:: python

       section_name = "Test section"
       lines = ["foo", "bar", "baz", "qux", ]
       parser = SomeParser()

       if parser.start(section_name):
           for line in lines:
              parser.parse_line(line)
           result = parser.stop()

    """

    __metaclass__ = ABCMeta

    #: Tells whether a parser was started.
    running = False

    #: An internal buffer which can be redefined.
    data = None

    def start(self, section_name):
        """
        Try to start a parser. If a section with given name can be parsed, the
        parser will initialize it's internal data structures and set
        :attr:`running` to `True`.

        :param str section_name: a name of section which is going to be parsed

        :returns: `True` if section with a given name can be parsed by parser,
                  `False` otherwise
        :rtype: :class:`bool`
        """
        result = self.check_section_name(section_name)
        if result:
            self.running = True
            self.init_parser(section_name)
        return result

    @abstractmethod
    def check_section_name(self, section_name):
        """
        Check whether a section with a given name can be parsed.

        :param str section_name: a name of section which is going to be parsed

        :returns: `True` if section with a given name can be parsed by parser,
                  `False` otherwise
        :rtype: :class:`bool`
        """

    @abstractmethod
    def init_parser(self, section_name):
        """
        Abstract method which is called by :meth:`start` to initialize
        internal data structures.

        :param str section_name: a name of section which is going to be parsed

        :returns: ``None``
        """

    @abstractmethod
    def parse_line(self, line):
        """
        Abstract method which is called manually to parse a line from mission
        section.

        :param str line: a single line to parse

        :returns: ``None``
        """

    def stop(self):
        """
        Stops parser and returns fully processed data.

        :returns: a data structure returned by :meth:`process_data` method

        :raises RuntimeError: if parser was not started
        """
        if not self.running:
            raise RuntimeError("Cannot stop parser which is not running")

        self.running = False
        return self.process_data()

    def process_data(self):
        """
        Returns fully parsed data. Is called by :meth:`stop` method.

        :returns: a data structure which is specific for every subclass
        """
        return self.data


class ValuesParser(SectionParser):
    """
    This is a base class for parsers which assume that a section, which is
    going to be parsed, consists of key-value pairs with unique keys, one pair
    per line.

    **Section definition example**::

       [some section name]
       key1 value1
       key2 value2
       key3 value3
    """

    def init_parser(self, section_name):
        """
        Implements abstract method. See :meth:`SectionParser.init_parser` for
        semantics.

        Initializes a dictionary to store raw keys and their values.
        """
        self.data = {}

    def parse_line(self, line):
        """
        Implements abstract method. See :meth:`SectionParser.parse_line` for
        semantics.

        Splits line into key-value pair and puts it into internal dictionary.
        """
        key, value = line.split()
        self.data.update({key: value})


class CollectingParser(SectionParser):
    """
    This is a base class for parsers which assume that a section, which is
    going to be parsed, consists of homogeneous lines which describe different
    objects with one set of attributes.

    **Section definition example**::

       [some section name]
       object1_attr1 object1_attr2 object1_attr3 object1_attr4
       object2_attr1 object2_attr2 object2_attr3 object2_attr4
       object3_attr1 object3_attr2 object3_attr3 object3_attr4
    """

    def init_parser(self, section_name):
        """
        Implements abstract method. See :meth:`SectionParser.init_parser` for
        semantics.

        Initializes a list for storing collection of objects.
        """
        self.data = []

    def parse_line(self, line):
        """
        Implements abstract method. See :meth:`SectionParser.parse_line` for
        semantics.

        Just puts entire line to internal buffer. You probably will want to
        redefine this method to do some extra job on each line.
        """
        self.data.append(line)


class MainParser(ValuesParser):
    """
    Parses ``MAIN`` section.
    View :ref:`detailed description <main-section>`.
    """

    def check_section_name(self, section_name):
        """
        Implements abstract method. See
        :meth:`SectionParser.check_section_name` for semantics.
        """
        return section_name == "MAIN"

    def process_data(self):
        """
        Redefines base method. See :meth:`SectionParser.process_data` for
        semantics.
        """
        weather_conditions = int(self.data['CloudType'])
        return {
            'loader': self.data['MAP'],
            'time': {
                'value': self._to_time(self.data['TIME']),
                'is_fixed': 'TIMECONSTANT' in self.data,
            },
            'fixed_loadout': 'WEAPONSCONSTANT' in self.data,
            'weather_conditions': Conditions.get_by_value(weather_conditions),
            'cloud_base': int(float(self.data['CloudHeight'])),
            'player': {
                'belligerent': to_belligerent(self.data['army']),
                'regiment': self.data.get('player'),
                'number': int(self.data['playerNum']),
            },
        }

    def _to_time(self, value):
        time = float(self.data['TIME'])
        minutes, hours = math.modf(time)
        return datetime.time(int(hours), int(minutes * 60))


class SeasonParser(ValuesParser):
    """
    Parses ``SEASON`` section.
    View :ref:`detailed description <season-section>`.
    """

    def check_section_name(self, section_name):
        """
        Implements abstract method. See
        :meth:`SectionParser.check_section_name` for semantics.
        """
        return section_name == "SEASON"

    def process_data(self):
        """
        Redefines base method. See :meth:`SectionParser.process_data` for
        semantics.

        Combines day, time and year into :class:`datetime.date` object.
        """
        date = datetime.date(int(self.data['Year']),
                             int(self.data['Month']),
                             int(self.data['Day']))
        return {'date': date, }


class WeatherParser(ValuesParser):
    """
    Parses ``WEATHER`` section.
    View :ref:`detailed description <weather-section>`.
    """

    def check_section_name(self, section_name):
        """
        Implements abstract method. See
        :meth:`SectionParser.check_section_name` for semantics.
        """
        return section_name == "WEATHER"

    def process_data(self):
        """
        Redefines base method. See :meth:`SectionParser.process_data` for
        semantics.
        """
        gust = int(self.data['Gust'])
        turbulence = int(self.data['Turbulence'])
        return {
            'weather': {
                'wind': {
                    'direction': float(self.data['WindDirection']),
                    'speed': float(self.data['WindSpeed']),
                },
                'gust': Gust.get_by_value(gust),
                'turbulence': Turbulence.get_by_value(turbulence),
            },
        }


class MDSParser(ValuesParser):
    """
    Parses ``MDS`` section.
    View :ref:`detailed description <mds-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "MDS"

    def parse_line(self, line):
        super(MDSParser, self).parse_line(line.replace('MDS_', ''))

    def process_data(self):
        return {
            'radar': {
                'advanced_mode': to_bool(self.data['Radar_SetRadarToAdvanceMode']),
                'refresh_interval': int(self.data['Radar_RefreshInterval']),
                'ships': {
                    'treat_as_radar': to_bool(self.data['Radar_ShipsAsRadar']),
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
                    'max_height': int(self.data['Radar_ScoutRadar_DeltaHeight']),
                    'alpha': int(self.data['Radar_ScoutGroundObjects_Alpha']),
                },
            },
            'ai': {
                'no_radio_chatter': to_bool(self.data['Misc_DisableAIRadioChatter']),
                'hide_aircrafts_after_landing': to_bool(self.data['Misc_DespawnAIPlanesAfterLanding']),
            },
            'homebase': {
                'tower_communications': to_bool(self.data['Radar_EnableTowerCommunications']),
                'hide_unpopulated': to_bool(self.data['Radar_HideUnpopulatedAirstripsFromMinimap']),
                'hide_players_count': to_bool(self.data['Misc_HidePlayersCountOnHomeBase']),
            },
            'crater_visibility_muptipliers': {
                'le_100kg': float(self.data['Misc_BombsCat1_CratersVisibilityMultiplier']),
                'le_1000kg': float(self.data['Misc_BombsCat2_CratersVisibilityMultiplier']),
                'gt_1000kg': float(self.data['Misc_BombsCat3_CratersVisibilityMultiplier']),
            },
            'vectoring': not to_bool(self.data['Radar_DisableVectoring']),
            'only_scounts_complete_recon_targets': to_bool(self.data['Radar_ScoutCompleteRecon']),
        }


class MDSScoutsParser(CollectingParser):
    """
    Parses ``MDS_Scouts`` section.
    View :ref:`detailed description <mds-scouts-section>`.
    """
    prefix = "MDS_Scouts_"

    def check_section_name(self, section_name):
        if not section_name.startswith(self.prefix):
            return False
        suffix = self._extract_section_suffix(section_name)
        return bool(suffix)

    def init_parser(self, section_name):
        super(MDSScoutsParser, self).init_parser(section_name)
        suffix = self._extract_section_suffix(section_name)
        self.output_key = "scout_planes_{:}".format(suffix)

    def _extract_section_suffix(self, section_name):
        return section_name.lstrip(self.prefix).lower()

    def process_data(self):
        return {self.output_key: self.data}


class RespawnTimeParser(ValuesParser):
    """
    Parses ``RespawnTime`` section.
    View :ref:`detailed description <respawn-time-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "RespawnTime"

    def process_data(self):
        return {
            'respawn_time': {
                'ships': {
                    'big': int(self.data['Bigship']),
                    'small': int(self.data['Ship']),
                },
                'balloons': int(self.data['Aeroanchored']),
                'artillery': int(self.data['Artillery']),
                'searchlights': int(self.data['Searchlight']),
            },
        }


class ChiefsParser(CollectingParser):
    """
    Parses ``Chiefs`` section.
    View :ref:`detailed description <chiefs-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Chiefs"

    def parse_line(self, line):
        params = line.split()
        (oid, type_code, belligerent), params = params[0:3], params[3:]

        chief_type, code = type_code.split('.')
        try:
            chief_type = to_unit_type(chief_type)
        except:
            chief_type = None

        chief = {
            'id': oid,
            'code': code,
            'type': chief_type,
            'belligerent': to_belligerent(belligerent),
        }
        if params:
            waiting_time, skill, recharge_time = params
            chief.update({
                'waiting_time': int(waiting_time),
                'skill': to_skill(skill),
                'recharge_time': float(recharge_time),
            })
        self.data.append(chief)

    def process_data(self):
        return {'chiefs': self.data, }


class ChiefRoadParser(CollectingParser):
    """
    Parses ``N_Chief_Road`` section.
    View :ref:`detailed description <chief-road-section>`.
    """
    suffix = "_Chief_Road"

    def check_section_name(self, section_name):
        if not section_name.endswith(self.suffix):
            return False
        try:
            self._extract_object_code(section_name)
        except ValueError:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(ChiefRoadParser, self).init_parser(section_name)
        object_code = self._extract_object_code(section_name)
        self.output_key = "{0}_chief_route".format(object_code)

    def _extract_object_code(self, section_name):
        stop = section_name.index('_')
        return int(section_name[:stop])

    def parse_line(self, line):
        params = line.split()
        pos, params = params[0:2], params[3:]
        way_point = {
            'pos': to_pos(*pos),
        }
        is_check_point = bool(params)
        way_point['is_check_point'] = is_check_point
        if is_check_point:
            way_point['waiting_time'] = int(params[0])
            way_point['section_length'] = int(params[1])
            way_point['speed'] = float(params[2])

        self.data.append(way_point)

    def process_data(self):
        return {self.output_key: self.data}


class NStationaryParser(CollectingParser):
    """
    Parses ``NStationary`` section.
    View :ref:`detailed description <nstationary-section>`.
    """

    def init_parser(self, section_name):
        super(NStationaryParser, self).init_parser(section_name)
        self.subparsers = {
            'artillery': self._parse_artillery,
            'planes': self._parse_planes,
            'ships': self._parse_ships,
        }

    def check_section_name(self, section_name):
        return section_name == "NStationary"

    def parse_line(self, line):
        params = line.split()

        oid, object_name, belligerent = params[0], params[1], params[2]
        pos = params[3:5]
        rotation_angle = params[5]
        params = params[6:]

        type_name = self._get_type_name(object_name)
        try:
            object_type = to_unit_type(type_name)
        except:
            object_type = None

        static = ({
            'belligerent': to_belligerent(belligerent),
            'id': oid,
            'code': self._get_code(object_name),
            'pos': to_pos(*pos),
            'rotation_angle': float(rotation_angle),
            'type': object_type,
        })

        subparser = self.subparsers.get(type_name)
        if subparser:
            static.update(subparser(params))
        self.data.append(static)

    def _get_type_name(self, object_name):
        if object_name.startswith('ships'):
            return "ships"
        else:
            start = object_name.index('.') + 1
            stop = object_name.rindex('.')
            return object_name[start:stop]

    def _get_code(self, code):
        start = code.index('$') + 1
        return code[start:]

    def _parse_artillery(self, params):
        """
        Parse additional options for ``artillery`` type
        """
        awakening_time, range_, skill, is_spotter = params
        return {
            'awakening_time': float(awakening_time),
            'range': int(range_),
            'skill': to_skill(skill),
            'use_spotter': to_bool(is_spotter),
        }

    def _parse_planes(self, params):
        """
        Parse additional options for ``planes`` type
        """
        air_force, allows_spawning_restorable = params[1:3]
        skin, has_markings = params[4:]
        return {
            'air_force': AirForces.get_by_value(air_force),
            'allows_spawning': to_bool(allows_spawning_restorable),
            'restorable': allows_spawning_restorable == '2',
            'skin': skin,
            'show_markings': to_bool(has_markings),
        }

    def _parse_ships(self, params):
        """
        Parse additional options for ``ships`` type
        """
        awakening_time, skill, recharge_time = params[1:]
        return {
            'awakening_time': float(awakening_time),
            'recharge_time': float(recharge_time),
            'skill': to_skill(skill),
        }

    def process_data(self):
        return {'stationary': self.data, }


class BuildingsParser(CollectingParser):
    """
    Parses ``Buildings`` section.
    View :ref:`detailed description <buildings-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Buildings"

    def parse_line(self, line):
        params = line.split()
        oid, building_object, belligerent = params[:3]
        pos_x, pos_y, rotation_angle = params[3:]
        building_type, code = building_object.split('$')
        buildings = {
            'id': oid,
            'belligerent': to_belligerent(belligerent),
            'code': code,
            'pos': to_pos(pos_x, pos_y),
            'rotation_angle': float(rotation_angle),
        }
        self.data.append(buildings)

    def process_data(self):
        return {'buildings': self.data, }


class TargetParser(CollectingParser):
    """
    Parses ``Target`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "Target"

    def parse_line(self, line):
        params = line.split()

        type_code, priority, sleep_mode, timeout = params[:4]
        params = params[4:]

        target_type = TargetTypes.get_by_value(int(type_code))
        target = {
            'type': target_type,
            'priority': TargetPriorities.get_by_value(int(priority)),
            'in_sleep_mode': to_bool(sleep_mode),
            'timeout': int(timeout),
        }

        subparser = TargetParser.subparsers.get(target_type)
        if subparser is not None:
            target.update(subparser(params))

        self.data.append(target)

    @staticmethod
    def to_destruction_level(value):
        return int(value) / 10

    def parse_destroy_or_cover_or_escort(params):
        """
        Parse extra parameters for targets with type 'destroy' or 'cover' or
        'escort'.
        """
        destruction_level = TargetParser.to_destruction_level(params[0])
        pos, waypoint, object_code = params[1:3], params[4], params[5]
        object_pos = params[6:8]
        return {
            'destruction_level': destruction_level,
            'pos': to_pos(*pos),
            'object': {
                'waypoint': int(waypoint),
                'id': object_code,
                'pos': to_pos(*object_pos),
            },
        }

    def parse_destroy_or_cover_bridge(params):
        """
        Parse extra parameters for targets with type 'destroy bridge' or
        'cover bridge'.
        """
        pos, object_code, object_pos = params[1:3], params[5], params[6:8]
        return {
            'pos': to_pos(*pos),
            'object': {
                'id': object_code,
                'pos': to_pos(*object_pos),
            },
        }

    def parse_destroy_or_cover_area(params):
        """
        Parse extra parameters for targets with type 'destroy area' or
        'cover area'.
        """
        destruction_level = TargetParser.to_destruction_level(params[0])
        pos_x, pos_y, radius = params[1:]
        return {
            'destruction_level': destruction_level,
            'pos': to_pos(pos_x, pos_y),
            'radius': int(radius),
        }

    def parse_recon(params):
        """
        Parse extra parameters for targets with 'recon' type.
        """
        requires_landing = params[0] != '500'
        pos, radius, params = params[1:3], params[3], params[4:]
        data = {
            'radius': int(radius),
            'requires_landing': requires_landing,
            'pos': to_pos(*pos),
        }
        if params:
            waypoint, object_code = params[:2]
            object_pos = params[2:]
            data['object'] = {
                'waypoint': int(waypoint),
                'id': object_code,
                'pos': to_pos(*object_pos),
            }
        return data

    subparsers = {
        TargetTypes.destroy: parse_destroy_or_cover_or_escort,
        TargetTypes.destroy_bridge: parse_destroy_or_cover_bridge,
        TargetTypes.destroy_area: parse_destroy_or_cover_area,
        TargetTypes.recon: parse_recon,
        TargetTypes.escort: parse_destroy_or_cover_or_escort,
        TargetTypes.cover: parse_destroy_or_cover_or_escort,
        TargetTypes.cover_area: parse_destroy_or_cover_area,
        TargetTypes.cover_bridge: parse_destroy_or_cover_bridge,
    }

    def process_data(self):
        return {'targets': self.data, }


class BornPlaceParser(CollectingParser):
    """
    Parses ``BornPlace`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "BornPlace"

    def parse_line(self, line):
        (belligerent, radius, pos_x, pos_y, parachute, air_spawn_height,
         air_spawn_speed, air_spawn_heading, max_allowed_pilots,
         recon_min_height, recon_max_height, recon_range, air_spawn_always,
         enable_aircraft_limits, aircraft_limits_consider_lost,
         disable_spawning, friction_enabled, friction_value,
         aircraft_limits_consider_destroyed_stationary, show_default_icon,
         air_spawn_if_deck_is_full, spawn_in_stationary,
         return_to_start_position) = line.split()

        self.data.append({
            'radius': int(radius),
            'belligerent': to_belligerent(belligerent),
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
    Parses ``BornPlaceN`` section.
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
        self.output_key = (
            'homebase_aircrafts_{0}'
            .format(self._extract_section_number(section_name))
        )
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
    Parses ``BornPlaceCountriesN`` section.
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
    Parses ``StaticCamera`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "StaticCamera"

    def parse_line(self, line):
        pos_x, pos_y, pos_z, belligerent = line.split()
        self.data.append({
            'belligerent': to_belligerent(belligerent),
            'pos': to_pos(pos_x, pos_y, pos_z),
        })

    def process_data(self):
        return {'cameras': self.data, }


class BridgeParser(CollectingParser):
    """
    Parses ``Bridge`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "Bridge"

    def parse_line(self, line):
        pass

    def process_data(self):
        return {'bridges': self.data, }


class HouseParser(CollectingParser):
    """
    Parses ``House`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "House"

    def parse_line(self, line):
        pass

    def process_data(self):
        return {'houses': self.data, }


class FrontMarkerParser(CollectingParser):
    """
    Parses ``FrontMarker`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "FrontMarker"

    def parse_line(self, line):
        oid, pos_x, pos_y, belligerent = line.split()
        self.data.append({
            'id': oid,
            'belligerent': to_belligerent(belligerent),
            'pos': to_pos(pos_x, pos_y),
        })

    def process_data(self):
        return {'markers': self.data, }


class RocketParser(CollectingParser):
    """
    Parses ``Rocket`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "Rocket"

    def parse_line(self, line):
        params = line.split()
        oid, code, belligerent = params[0:3]
        pos = params[3:5]
        rotation_angle, timeout, amount, period = params[5:9]
        target_pos = params[9:]
        self.data.append({
            'id': oid,
            'code': code,
            'belligerent': to_belligerent(belligerent),
            'pos': to_pos(*pos),
            'rotation_angle': float(rotation_angle),
            'timeout': float(timeout),
            'amount': int(amount),
            'period': float(period),
            'target_pos': to_pos(*target_pos) if target_pos else None
        })

    def process_data(self):
        return {'rockets': self.data}


class WingParser(CollectingParser):
    """
    Parses ``Wing`` section.
    """

    def check_section_name(self, section_name):
        return section_name == "Wing"

    def process_data(self):
        return {'flights': self.data}


class FlightDetailsParser(ValuesParser):
    """
    Parses settings for a moving flight group.
    """

    def check_section_name(self, section_name):
        return True

    def init_parser(self, section_name):
        super(FlightDetailsParser, self).init_parser(section_name)
        self.output_key = "{0}_details".format(section_name)
        self.flight_details = self._decompose_section_name(section_name)

    def _decompose_section_name(self, section_name):
        return {
            'regiment_code': section_name[:-2],
            'squadron_number': int(section_name[-2])+1,
            'flight_number': int(section_name[-1])+1,
        }

    def _skin_code(self, prefix, number):
        return self.data.get('{0}{1}'.format(prefix, number), _("default"))

    def _spawn_point(self, number):
            return self.data.get('spawn{0}'.format(number))

    def _skill_code(self, number):
        if 'Skill' in self.data:
            return to_skill(self.data['Skill'])
        else:
            return to_skill(self.data['Skill{0}'.format(number)])

    def _has_markings(self, number):
            return 'numberOn{0}'.format(number) not in self.data

    def _flight(self, aircrafts_count):
        self.flight_details['aircrafts'] = []
        for number in range(0, aircrafts_count):
            self.flight_details['aircrafts'].append({
                'number': number,
                'skill': self._skill_code(number),
                'aircraft_skin': self._skin_code('skin', number),
                'pilot_skin': self._skin_code('pilot', number),
                'has_markings': self._has_markings(number),
                'spawn_point': self._spawn_point(number),
            })

    def process_data(self):
        aircrafts_count = int(self.data['Planes'])
        aircraft_code = self.data['Class'][self.data['Class'].index('.')+1:]

        self.flight_details.update({
            'aircrafts_count': aircrafts_count,
            'aircraft_code': aircraft_code,
            'fuel': int(self.data['Fuel']),
            'loadout': self.data['weapons'],
            'parachute_present': 'Parachute' not in self.data,
            'only_ai': 'OnlyAI' in self.data,
        })

        self._flight(aircrafts_count)

        return {self.output_key: self.flight_details}


class FlightWayParser(CollectingParser):
    """
    Parses ``*_Way`` section.
    """
    suffix = "_Way"

    def check_section_name(self, section_name):
        return section_name.endswith(self.suffix)

    def _extract_flight_code(self, section_name):
        return section_name.rstrip(self.suffix)

    def init_parser(self, section_name):
        self.data = []
        self.way_points = {}
        flight_code = self._extract_flight_code(section_name)
        self.output_key = "{0}_way_point".format(flight_code)

    def _parse_trigger(self, chunks):
        amount_params_takeoff = 4
        if len(chunks) == amount_params_takeoff:
            (timeout, distance, ) = chunks[1:3]
            self.way_points.update({
                'triggers': {
                    'timeout': int(timeout),
                    'distance': int(distance),
                },
            })
        else:
            cycles, timer, angle, base_size, altitude_diff = chunks
            self.way_points.update({
                'triggers': {
                    'cycles': int(cycles),
                    'timer': int(timer),
                    'angle': int(angle),
                    'base_size': int(base_size),
                    'altitude_diff': int(altitude_diff),
                },
            })

    def _get_formation_code(self, chunks):
        if chunks:
            (formation_code, ) = chunks
            return WAY_POINT_FORMATIONS.get(formation_code)
        else:
            return "default"

    def _parse_way_point_on_target(self, chunks):
        target_code, target_point, radio_silence = chunks[:3]
        chunks = chunks[3:]
        formation_code = self._get_formation_code(chunks)
        self.way_points.update({
            'target_code': target_code,
            'target_point': int(target_point),
            'radio_silence': radio_silence == "&1",
            'formation_code': formation_code,
        })

    def _parse_way_point_without_target(self, chunks):
        radio_silence, chunks = chunks[0], chunks[1:]
        formation_code = self._get_formation_code(chunks)
        self.way_points.update({
            'radio_silence': radio_silence == "&1",
            'formation_code': formation_code,
        })

    def parse_line(self, line):
        chunks = line.split()
        way_point_type, chunks = chunks[0], chunks[1:]
        if way_point_type == "TRIGGERS":
            self._parse_trigger(chunks)
        else:
            if self.way_points:
                self.data.append(self.way_points)
                self.way_points = {}
            pos, speed, chunks = chunks[0:3], chunks[3], chunks[4:]
            self.way_points.update({
                'way_point_type': WAY_POINT_TYPES[way_point_type],
                'pos': to_pos(*pos),
                'speed': float(speed),
            })
            amount_on_target = 2
            if len(chunks) > amount_on_target:
                self._parse_way_point_on_target(chunks)
            else:
                self._parse_way_point_without_target(chunks)

    def process_data(self):
        if self.way_points:
            self.data.append(self.way_points)
        return {self.output_key: self.data}


class FileParser(object):
    """
    Parses a whole mission file.
    """

    def __init__(self):
        self.data = {}
        self.flight_parser = FlightDetailsParser()
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
            WingParser(),
            MDSScoutsParser(),
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
        flight_codes = self.data.get('flights')
        if flight_codes is not None and section_name in flight_codes:
            self.flight_parser.start(section_name)
            return self.flight_parser
        for parser in self.parsers:
            if parser.start(section_name):
                return parser
        return None

    def process_data(self):
        """
        .. todo:: organize final output
        """
        return self.data

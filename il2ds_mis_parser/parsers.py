# -*- coding: utf-8 -*-
"""
Parsers of whole missions files and separate sections.
"""
import datetime
import math

from abc import ABCMeta, abstractmethod

from il2ds_mis_parser.constants import *


def to_bool(value):
    return value != '0'


def to_pos(x, y, z=None):
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
            'army_code': int(self.data['army']),
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
        code, type_code, army = line.split()
        chief_type, code_name = type_code.split('.')

        self.data.append({
            'code': code,
            'code_name': code_name,
            'type': chief_type.lower(),
            'army_code': int(army),
        })

    def process_data(self):
        return {'chiefs': self.data, }


class NStationaryParser(CollectingParser):
    """
    Parses 'NStationary' section.
    """

    def check_section_name(self, section_name):
        return section_name == "NStationary"

    def parse_line(self, line):
        pass

    def process_data(self):
        return {'statics': self.data, }


class BuildingsParser(CollectingParser):
    """
    Parses 'Buildings' section.
    """

    def check_section_name(self, section_name):
        return section_name == "Buildings"

    def parse_line(self, line):
        pass

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
            'army_code': int(army_code),
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


class StaticCameraParser(CollectingParser):
    """
    Parses 'StaticCamera' section.
    """

    def check_section_name(self, section_name):
        return section_name == "StaticCamera"

    def parse_line(self, line):
        pos_x, pos_y, pos_z, army = line.split()
        self.data.append({
            'army_code': int(army),
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
        code, pos_x, pos_y, army = line.split()
        self.data.append({
            'code': code,
            'army_code': int(army),
            'pos': to_pos(pos_x, pos_y),
        })

    def process_data(self):
        return {'markers': self.data, }


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

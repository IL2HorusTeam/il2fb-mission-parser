# -*- coding: utf-8 -*-
"""
Parser files missions and properties.
"""
import datetime

from il2ds_mis_parser.constants import *


def to_bool(value):
    return value != '0'


class BaseParser(object):

    @property
    def section_name(self):
        raise NotImplementedError

    def parse(self, line):
        pass

    def clean(self):
        pass


class ValueParser(BaseParser):

    def __init__(self):
        self.data = {}

    def parse(self, line):
        code, value = line.split()
        self.data.update({code: value})

    def clean(self):
        return self.data


class MainParser(ValueParser):
    """
    Parses 'MAIN' section.
    """
    section_name = "MAIN"

    def parse(self, line):
        super(MainParser, self).parse(line)

    def clean(self):
        return {
            'map': self.data['MAP'],
            'time': self.data['TIME'],
            'type_clouds': int(self.data['CloudType']),
            'height_clouds': float(self.data['CloudHeight']),
            'army': int(self.data['army']),
            'player_regiment': self.data['playerNum'],
        }


class SeasonParser(ValueParser):
    """
    Parses 'SEASON' section.
    """
    section_name = "SEASON"

    def clean(self):
        return datetime.date(int(self.data['Year']),
                             int(self.data['Month']),
                             int(self.data['Day']))


class WeatherParser(ValueParser):
    """
    Parses 'WEATHER' section.
    """
    section_name = "WEATHER"

    def clean(self):
        return {
            'wind': {
                'direction': float(self.data['WindDirection']),
                'speed': float(self.data['WindSpeed']),
            },
            'gust': int(self.data['Gust']),
            'turbulence': int(self.data['Turbulence']),
        }


class MDSParser(ValueParser):
    """
    Parses 'MDS' section.
    """
    section_name = "MDS"

    def parse(self, line):
        super(MDSParser, self).parse(line.replace('MDS_', ''))

    def clean(self):
        return {
            'radar': {
                'advance_mode': to_bool(self.data['Radar_SetRadarToAdvanceMode']),
                'no_vectoring': to_bool(self.data['Radar_DisableVectoring']),
                'ships': {
                    'normal': {
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
            'bomb_crater_visibility_muptiplier': {
                'cat1': float(self.data['Misc_BombsCat1_CratersVisibilityMultiplier']),
                'cat2': float(self.data['Misc_BombsCat2_CratersVisibilityMultiplier']),
                'cat3': float(self.data['Misc_BombsCat3_CratersVisibilityMultiplier']),
            },
            'no_players_count_on_home_base': to_bool(self.data['Misc_HidePlayersCountOnHomeBase']),
        }


class RespawnTimeParser(ValueParser):
    """
    Parses 'RespawnTime' section.
    """
    section_name = "RespawnTime"

    def clean(self):
        return {
            'big_ships': int(self.data['Bigship']),
            'small_ships': int(self.data['Ship']),
            'balloons': int(self.data['Aeroanchored']),
            'artillery': int(self.data['Artillery']),
            'searchlight': int(self.data['Searchlight']),
        }


class ChiefsParser(BaseParser):
    """
    Parses 'Chiefs' section.
    """
    section_name = "Chiefs"

    def __init__(self):
        self.data = {}

    def parse(self, line):
        chiefs, type_code, army = line.split()
        type_chiefs, code = type_code.split('.')
        self.data.update({
            chiefs: {
                'type': type_chiefs,
                'code': code,
                'army': int(army),
            },
        })

    def clean(self):
        return self.data


class NStationaryParser(BaseParser):
    """
    Parses 'NStationary' section.
    """
    section_name = "NStationary"

    def __init__(self):
        self.data = []

    def parse(self, line):
        self.data.append(line)

    def clean(self):
        return self.data


class BuildingsParser(BaseParser):
    """
    Parses 'Buildings' section.
    """
    section_name = "Buildings"

    def __init__(self):
        self.data = []

    def parse(self, line):
        self.data.append(line)

    def clean(self):
        return self.data


class TargetParser(BaseParser):
    """
    Parses 'Target' section.
    """
    section_name = "Target"

    def __init__(self):
        self.data = []
        self.subparsers = {
            TARGET_TYPE_DESTROY: self.parse_destroy_or_cover,
            TARGET_TYPE_DESTROY_BRIDGE: self.parse_destroy_or_cover_bridge,
            TARGET_TYPE_DESTROY_AREA: self.parse_destroy_or_cover_area,
            TARGET_TYPE_RECON: self.parse_recon,
            TARGET_TYPE_ESCORT: self.parse_escort,
            TARGET_TYPE_COVER: self.parse_destroy_or_cover,
            TARGET_TYPE_COVER_AREA: self.parse_destroy_or_cover_area,
            TARGET_TYPE_COVER_BRIDGE: self.parse_destroy_or_cover_bridge,
        }

    def parse(self, line):
        params = line.split()
        (type_code, priority, sleep_mode, timeout), params = params[:4], params[4:]
        target = {
            'type': TARGET_TYPES[type_code],
            'priority': TARGET_PRIORITIES[priority],
            'sleep_mode': to_bool(sleep_mode),
            'timeout': int(timeout),
        }
        sub_parse = self.subparsers.get(type_code)
        target.update(sub_parse(params))
        self.data.append(target)

    def parse_destroy_or_cover(self, params):
        """
        Parses some parameters for target types "destroy" and "cover".
        """
        data = {}
        (destruction_level, pos_x, pos_y), object_target = params[:3], params[5:6]
        data['destruction_level'] = int(destruction_level)/10
        data.update(self.compose_position(pos_x, pos_y))
        data['object'] = object_target[0]

        return data

    def parse_destroy_or_cover_bridge(self, params):
        """
        Parses some parameters for target types "destroy bridge" and "cover bridge".
        """
        data = {}
        (pos_x, pos_y), object_target = params[1:3], params[5:6]
        data.update(self.compose_position(pos_x, pos_y))
        data['object'] = object_target[0]
        return data

    def parse_destroy_or_cover_area(self, params):
        """
        Parser of some parameters for target types "destroy area" and "cover area".
        """
        data = {}
        (destruction_level, pos_x, pos_y), object_target = params[:3], params[5:6]
        data['destruction_level'] = int(destruction_level)/10
        data.update(self.compose_position(pos_x, pos_y))
        return data

    def parse_recon(self, params):
        """
        Parses some parameters for target types "recon".
        """
        data = {}
        (requires_landing, pos_x, pos_y, radius), object_target = params[:4], params[5:6]
        data['requires_landing'] = to_bool(requires_landing[2])
        data.update(self.compose_position(pos_x, pos_y))
        data['radius'] = int(radius)
        if object_target:
            data['object'] = object_target[0]
        return data

    def parse_escort(self, params):
        """
        Parses some parameters for target types "escort".
        """
        data = {}
        (destruction_level, pos_x, pos_y), object_target = params[:3], params[5:6]
        data['destruction_level'] = int(destruction_level)/10
        data.update(self.compose_position(pos_x, pos_y))
        data['object'] = object_target[0]
        return data

    def compose_position(self, pos_x, pos_y):
        """
        Parses positions target.
        """
        return {
            'pos': {
                'x': int(pos_x),
                'y': int(pos_y),
            }
        }

    def clean(self):
        return self.data


class StaticCameraParser(BaseParser):
    """
    Parses 'StaticCamera' section.
    """
    section_name = "StaticCamera"

    def __init__(self):
        self.data = []

    def parse(self, line):
        pos_x, pos_y, height, army = line.split()
        self.data.append(
            {
                'pos': {
                    'x': int(pos_x),
                    'y': int(pos_y),
                },
                'height': int(height),
                'army': int(army),
            }
        )

    def clean(self):
        return self.data


class BridgeParser(BaseParser):
    """
    Parses 'Bridge' section.
    """
    section_name = "Bridge"


class HouseParser(BaseParser):
    """
    Parses 'House' section.
    """
    section_name = "House"


class FrontMarkerParser(BaseParser):
    """
    Parses 'FrontMarker' section.
    """
    section_name = "FrontMarker"

    def __init__(self):
        self.data = []

    def parse(self, line):
        code, pos_x, pos_y, army = line.split()
        self.data.append(
            {
                'code': code,
                'pos': {
                    'x': float(pos_x),
                    'y': float(pos_y)
                },
                'army': int(army),
            }
        )

    def clean(self):
        return self.data


class FileParser(BaseParser):
    """
    Parses whole mission files.
    """
    def __init__(self):
        self.data = {}
        classes = [
            MainParser,
            SeasonParser,
            WeatherParser,
            MDSParser,
            RespawnTimeParser,
            ChiefsParser,
            NStationaryParser,
            BuildingsParser,
            StaticCameraParser,
            BridgeParser,
            HouseParser,
            FrontMarkerParser,
        ]
        self.parsers = {
            parser_class.section_name: parser_class()
            for parser_class in classes
        }

    def parse(self, file_path):
        parser, section_name = None, None

        def finish_section_if_any():
            if parser:
                self.data[section_name] = parser.clean()

        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    finish_section_if_any()
                    section_name = line.strip('[]')
                    parser = self.parsers.get(section_name)
                elif parser:
                    parser.parse(line)
            finish_section_if_any()

        return self.clean()

    def clean(self):
        # TODO:
        return self.data

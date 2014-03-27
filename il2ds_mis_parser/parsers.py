# -*- coding: utf-8 -*-
"""
Parser files missions and properties.
"""
import datetime

from il2ds_mis_parser.constants import TARGET_PRIORITY

def to_boolean(value):
    return int(value) > 0


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
                'advance_mode': to_boolean(self.data['Radar_SetRadarToAdvanceMode']),
                'no_vectoring': to_boolean(self.data['Radar_DisableVectoring']),
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
                    'treat_as_radar': to_boolean(self.data['Radar_ScoutsAsRadar']),
                    'max_range': int(self.data['Radar_ScoutRadar_MaxRange']),
                },
            },
            'ai': {
                'no_radio_chatter': to_boolean(self.data['Misc_DisableAIRadioChatter']),
                'hide_planes_after_landing': to_boolean(self.data['Misc_DespawnAIPlanesAfterLanding']),
            },
            'bomb_crater_visibility_muptiplier': {
                'cat1': float(self.data['Misc_BombsCat1_CratersVisibilityMultiplier']),
                'cat2': float(self.data['Misc_BombsCat2_CratersVisibilityMultiplier']),
                'cat3': float(self.data['Misc_BombsCat3_CratersVisibilityMultiplier']),
            },
            'no_players_count_on_home_base': to_boolean(self.data['Misc_HidePlayersCountOnHomeBase']),
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
    Parses 'TARGET' section.
    """
    section_name = "Target"

    def __init__(self):
        self.data = []

    def parse(self, line):
        self.data.append(line)

    def clean(self):
        targets = {}
        for line in self.data:
            line = line.split()
            if len(line) > 8:
                if line[0] in ('0', '5'):
                    if not targets.has_key('destroy'):
                        targets.update({'destroy': []})
                    targets['destroy'].append(
                        {
                            'priority': TARGET_PRIORITY[line[1]],
                            'idle': to_boolean(line[2]),
                            'timeout': int(line[3]),
                            'destruction_level': int(line[4])/10,
                            'pos': {
                                'x': int(line[5]),
                                'y': int(line[6]),
                            },
                            'object': line[9],
                        }
                    )
                if line[0] == '3':
                    if not targets.has_key('recon'):
                        targets.update({'recon': []})
                    targets['recon'].append(
                        {
                            'priority': TARGET_PRIORITY[line[1]],
                            'idle': to_boolean(line[2]),
                            'timeout': int(line[3]),
                            'requires_landing': to_boolean(line[4][2]),
                            'pos': {
                                'x': int(line[5]),
                                'y': int(line[6]),
                            },
                            'radius': int(line[7]),
                            'object': line[9],
                        }
                    )
            else:
                if line[0] == '3':
                    if not targets.has_key('recon'):
                        targets.update({'recon': []})
                    targets['recon'].append(
                        {
                            'priority': TARGET_PRIORITY[line[1]],
                            'idle': to_boolean(line[2]),
                            'timeout': int(line[3]),
                            'requires_landing': to_boolean(line[4][2]),
                            'pos': {
                                'x': int(line[5]),
                                'y': int(line[6]),
                            },
                            'radius': int(line[7]),
                            'object': None,
                        }
                    )
        return targets


class StaticCameraParser(BaseParser):
    """
    Parses 'StaticCamera' section.
    """
    section_name = "StaticCamera"

    def __init__(self):
        self.data = {}

    def parse(self, line):
        pos_x, pos_y, height, army = line.split()
        self.data.update(
            {
                'pos_x': int(pos_x),
                'pos_y': int(pos_y),
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

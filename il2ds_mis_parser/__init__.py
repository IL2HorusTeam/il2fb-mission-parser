# -*- coding: utf-8 -*-
"""
Parser files missions and properties.
"""
from il2ds_mis_parser.constants import *
from il2ds_mis_parser.helpers import _, covert_str


class MainParser(object):
    """
    Parser configuration sections 'MAIN'
    """
    section_name = MAIN

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        code, value = line.split()
        self.settings.update({code: covert_str(value)})

    def clean(self):
        return self.settings


class SeasonParser(object):
    """
    Parser configuration sections 'SEASON'
    """
    section_name = SEASON

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        code, value = line.split()
        self.settings.update({code: covert_str(value)})

    def clean(self):
        return self.settings


class WeatherParser(object):
    """
    Parser configuration sections 'WEATHER'
    """
    section_name = WEATHER

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        code, value = line.split()
        self.settings.update({code: covert_str(value)})

    def clean(self):
        return self.settings


class MdsParser(object):
    """
    Parser configuration sections 'MDS'
    """
    section_name = MDS

    def __init__(self):
        self.settings = {
            'Radar': {},
            'Misc': {},
        }

    def parser(self, line, i=None):
        if line.startswith('MDS_Radar'):
            line = line[10::]
            code, value = line.split()
            self.settings['Radar'].update({code: covert_str(value)})
        elif line.startswith('MDS_Misc'):
            line = line[9::]
            code, value = line.split()
            self.settings['Misc'].update({code: covert_str(value)})

    def clean(self):
        return self.settings


class RespawnTimeParser(object):
    """
    Parser configuration sections 'RespawnTime'
    """
    section_name = RESPAWN_TIME

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        code, value = line.split()
        self.settings.update({code: covert_str(value)})

    def clean(self):
        return self.settings


class ChiefsParser(object):
    """
    Parser configuration sections 'Chiefs'
    """
    section_name = CHIEFS

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        chiefs, type_code, army = line.split()
        type_chiefs, code = type_code.split('.')
        self.settings.update(
            {
                chiefs: {
                    'type': type_chiefs,
                    'code': code,
                    'army': covert_str(army)
                }
            }
        )

    def clean(self):
        return self.settings


class NStationaryParser(object):
    """
    Parser configuration sections 'NStationary'
    """
    section_name = N_STATIONARY


class BuildingsParser(object):
    """
    Parser configuration sections 'Buildings'
    """
    section_name = BUILDINGS

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        buildings_code, type_code, army, pos_x, pos_y, height = line.split()
        type_buildings, code = type_code.split('$')
        self.settings.update(
            {
                buildings_code: {
                    'type': type_buildings,
                    'code': code,
                    'army': covert_str(army),
                    'pos_x': covert_str(pos_x),
                    'pos_y': covert_str(pos_y),
                    'height': covert_str(height)
                }
            }
        )

    def clean(self):
        return self.settings


class TargetParser(object):
    """
    Parser configuration sections 'Buildings'
    """
    section_name = TARGET

    def __init__(self):
        self.settings = {}
        self.key = 0

    def parser(self, line, i=None):
        army_defender, army_striker, p3, p4, percent_damage, pos_x, pos_y, radius = line.split()
        self.settings.update(
            {
                'target%s' % i: {
                    'army_defender': covert_str(army_defender),
                    'army_striker': covert_str(army_striker),
                    'p3': covert_str(p3),
                    'p4': covert_str(p4),
                    'percent_damage': covert_str(percent_damage),
                    'pos_x': covert_str(pos_x),
                    'pos_y': covert_str(pos_y),
                    'radius': covert_str(radius)
                }
            }
        )

    def clean(self):
        return self.settings


class StaticCameraParser(object):
    """
    Parser configuration sections 'StaticCamera'
    """
    section_name = STATIC_CAMERA


class BridgeParser(object):
    """
    Parser configuration sections 'Bridge'
    """
    section_name = BRIDGE


class HouseParser(object):
    """
    Parser configuration sections 'House'
    """
    section_name = HOUSE


class FrontMarkerParser(object):
    """
    Parser configuration sections 'FrontMarker'
    """
    section_name = FRONT_MARKER

    def __init__(self):
        self.settings = {}

    def parser(self, line, i=None):
        code, pos_x, pos_y, army = line.split()
        self.settings.update(
            {
                code: {
                    'pos_x': covert_str(pos_x),
                    'pos_y': covert_str(pos_y),
                    'army': covert_str(army),
                }
            }
        )

    def clean(self):
        return self.settings


class ParserRoot(object):
    """
    Base class for parsing file missions
    """
    def __init__(self):
        self.parsers = {
            MainParser.section_name: MainParser(),
            SeasonParser.section_name: SeasonParser(),
            WeatherParser.section_name: WeatherParser(),
            MdsParser.section_name: MdsParser(),
            RespawnTimeParser.section_name: RespawnTimeParser(),
            ChiefsParser.section_name: ChiefsParser(),
            NStationaryParser.section_name: NStationaryParser(),
            BuildingsParser.section_name: BuildingsParser(),
            TargetParser.section_name: TargetParser(),
            StaticCameraParser.section_name: StaticCameraParser(),
            BridgeParser.section_name: BridgeParser(),
            HouseParser.section_name: HouseParser(),
            FrontMarkerParser.section_name: FrontMarkerParser(),
        }

    def parser(self, file_path):
        settings = {}
        parser_line = None
        try:
            with open(file_path) as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if line.startswith('['):
                        section_name = line.strip('[]')
                        settings.update({section_name: {}})
                        parser_line = self.parsers[section_name]
                    else:
                        line = line.strip()
                        parser_line.parser(line, i)
                        settings[section_name].update(parser_line.clean())

            return settings
        except EOFError:
            raise (_("File not found"))
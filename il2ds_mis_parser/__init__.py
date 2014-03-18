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

    def parser(self, line):
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

    def parser(self, line):
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

    def parser(self, line):
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

    def parser(self, line):
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

    def parser(self, line):
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

    def parser(self, line):
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
                for line in f:
                    line = line.strip()
                    if line.startswith('['):
                        section_name = line.strip('[]')
                        settings.update({section_name: {}})
                        parser_line = self.parsers[section_name]
                    else:
                        line = line.strip()
                        parser_line.parser(line)
                        settings[section_name].update(parser_line.clean())

            return settings
        except EOFError:
            raise (_("File not found"))
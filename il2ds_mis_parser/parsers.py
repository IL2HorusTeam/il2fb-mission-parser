# -*- coding: utf-8 -*-
"""
Parser files missions and properties.
"""
import datetime


class MainParser(object):
    """
    Parser configuration sections 'MAIN'
    """
    section_name = "MAIN"

    def __init__(self):
        self.settings = {}

    def parse(self, line):
        code, value = line.split()
        self.settings.update({code: value})

    def clean(self):
        return self.settings


class SeasonParser(object):
    """
    Parser configuration sections 'SEASON'
    """
    section_name = "SEASON"

    def __init__(self):
        self.settings = {}

    def parse(self, line):
        code, value = line.split()
        self.settings.update({code: int(value)})

    def clean(self):
        return self.settings


class WeatherParser(object):
    """
    Parser configuration sections 'WEATHER'
    """
    section_name = "WEATHER"

    def __init__(self):
        self.settings = {}

    def parse(self, line):
        code, value = line.split()
        self.settings.update({code: value})

    def clean(self):
        return self.settings


class MdsParser(object):
    """
    Parser configuration sections 'MDS'
    """
    section_name = "MDS"

    def __init__(self):
        self.settings = {
            'Radar': {},
            'Misc': {},
        }

    def parse(self, line):
        if line.startswith('MDS_Radar'):
            line = line[10::]
            code, value = line.split()
            self.settings['Radar'].update({code: value})
        elif line.startswith('MDS_Misc'):
            line = line[9::]
            code, value = line.split()
            self.settings['Misc'].update({code: value})

    def clean(self):
        return self.settings


class RespawnTimeParser(object):
    """
    Parser configuration sections 'RespawnTime'
    """
    section_name = "RespawnTime"

    def __init__(self):
        self.settings = {}

    def parse(self, line):
        code, value = line.split()
        self.settings.update({code: value})

    def clean(self):
        return self.settings


class ChiefsParser(object):
    """
    Parser configuration sections 'Chiefs'
    """
    section_name = "Chiefs"

    def __init__(self):
        self.settings = {}

    def parse(self, line):
        chiefs, type_code, army = line.split()
        type_chiefs, code = type_code.split('.')
        self.settings.update(
            {
                chiefs: {
                    'type': type_chiefs,
                    'code': code,
                    'army': int(army)
                }
            }
        )

    def clean(self):
        return self.settings


class NStationaryParser(object):
    """
    Parser configuration sections 'NStationary'
    """
    section_name = "NStationary"


class BuildingsParser(object):
    """
    Parser configuration sections 'Buildings'
    """
    section_name = "Buildings"


class StaticCameraParser(object):
    """
    Parser configuration sections 'StaticCamera'
    """
    section_name = "StaticCamera"


class BridgeParser(object):
    """
    Parser configuration sections 'Bridge'
    """
    section_name = "Bridge"


class HouseParser(object):
    """
    Parser configuration sections 'House'
    """
    section_name = "House"


class FrontMarkerParser(object):
    """
    Parser configuration sections 'FrontMarker'
    """
    section_name = "FrontMarker"


class RootParser(object):
    """
    Base class for parsing file missions
    """
    def __init__(self):
        classes = [
            MainParser,
            SeasonParser,
            WeatherParser,
            MdsParser,
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
        settings = {}
        parser = None
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    if parser:
                        settings[section_name].update(parser.clean())
                    section_name = line.strip('[]')
                    settings.update({section_name: {}})
                    parser = self.parsers[section_name]

                else:
                    line = line.strip()
                    parser.parse(line)

            # The last section processing
            settings[section_name].update(parser.clean())

        return settings
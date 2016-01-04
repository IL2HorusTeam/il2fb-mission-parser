# -*- coding: utf-8 -*-
"""
Memory & time consumption tests for parsers.
"""
if 'profile' not in locals():
    try:
        from memory_profiler import profile
    except ImportError:
        import __builtin__
        try:
            profile = __builtin__.profile
        except AttributeError:
            profile = lambda x: x


from il2fb.parsers.mission.sections.chiefs import ChiefRoadSectionParser
from il2fb.parsers.mission.sections.nstationary import NStationarySectionParser
from il2fb.parsers.mission.sections.buildings import BuildingsSectionParser
from il2fb.parsers.mission.sections.target import TargetSectionParser
from il2fb.parsers.mission.sections.born_place import BornPlaceSectionParser
from il2fb.parsers.mission.sections.static_camera import StaticCameraSectionParser
from il2fb.parsers.mission.sections.front_marker import FrontMarkerSectionParser
from il2fb.parsers.mission.sections.rocket import RocketSectionParser
from il2fb.parsers.mission.sections.wing import FlightRouteSectionParser

from generators import (
    generate_cheif_road_lines,
    generate_nstationary_lines, generate_buildings_lines,
    generate_target_lines, generate_born_place_lines,
    generate_static_camera_lines, generate_front_marker_lines,
    generate_rocket_lines, generate_flight_route_lines,
)


class ParserWrapper(object):

    def __init__(self, parser_class, section_name, lines_generator):
        self.parser_class = parser_class
        self.section_name = section_name
        self.lines_generator = lines_generator

    def __enter__(self):
        self.parser = self.parser_class()
        self.parser.start(self.section_name)
        return self

    def __exit__(self, exception_type, exception, traceback):
        self.parser.stop()

    @property
    def lines(self):
        return self.lines_generator()

    def parse_line(self, line):
        return self.parser.parse_line(line)


@profile
def profile_chief_road_parser():
    with ParserWrapper(ChiefRoadSectionParser, '0_Chief_Road', generate_cheif_road_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_nstationary_parser():
    with ParserWrapper(NStationarySectionParser, 'NStationary', generate_nstationary_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_buildings_parser():
    with ParserWrapper(BuildingsSectionParser, 'Buildings', generate_buildings_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_target_parser():
    with ParserWrapper(TargetSectionParser, 'Target', generate_target_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_born_place_parser():
    with ParserWrapper(BornPlaceSectionParser, 'BornPlace', generate_born_place_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_static_camera_parser():
    with ParserWrapper(StaticCameraSectionParser, 'StaticCamera', generate_static_camera_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_front_marker_parser():
    with ParserWrapper(FrontMarkerSectionParser, 'FrontMarker', generate_front_marker_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_rocket_parser():
    with ParserWrapper(RocketSectionParser, 'Rocket', generate_rocket_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_flight_route_parser():
    with ParserWrapper(FlightRouteSectionParser, '3GvIAP01_Way', generate_flight_route_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


if __name__ == '__main__':
    profile_chief_road_parser()
    profile_nstationary_parser()
    profile_buildings_parser()
    profile_target_parser()
    profile_born_place_parser()
    profile_static_camera_parser()
    profile_front_marker_parser()
    profile_rocket_parser()
    profile_flight_route_parser()

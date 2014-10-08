# -*- coding: utf-8 -*-
"""
Memory & time consumption tests for parsers.
"""
from il2fb.parsers.mission.parsers import (
    MDSScoutsParser, ChiefsParser, ChiefRoadParser, NStationaryParser,
    BuildingsParser, TargetParser, BornPlaceParser, StaticCameraParser,
    FrontMarkerParser, RocketParser, FlightRouteParser,
)

from generators import (
    generate_cheifs_lines, generate_cheif_road_lines,
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

    def __exit__(self, type, value, traceback):
        self.parser.stop()

    @property
    def lines(self):
        return self.lines_generator()

    def parse_line(self, line):
        return self.parser.parse_line(line)


@profile
def profile_chiefs_parser():
    with ParserWrapper(ChiefsParser, 'Chiefs', generate_cheifs_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_chief_road_parser():
    with ParserWrapper(ChiefRoadParser, '0_Chief_Road', generate_cheif_road_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_nstationary_parser():
    with ParserWrapper(NStationaryParser, 'NStationary', generate_nstationary_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_buildings_parser():
    with ParserWrapper(BuildingsParser, 'Buildings', generate_buildings_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_target_parser():
    with ParserWrapper(TargetParser, 'Target', generate_target_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_born_place_parser():
    with ParserWrapper(BornPlaceParser, 'BornPlace', generate_born_place_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_static_camera_parser():
    with ParserWrapper(StaticCameraParser, 'StaticCamera', generate_static_camera_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_front_marker_parser():
    with ParserWrapper(FrontMarkerParser, 'FrontMarker', generate_front_marker_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_rocket_parser():
    with ParserWrapper(RocketParser, 'Rocket', generate_rocket_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


@profile
def profile_flight_route_parser():
    with ParserWrapper(FlightRouteParser, '3GvIAP01_Way', generate_flight_route_lines) as pw:
        for line in pw.lines:
            pw.parse_line(line)


if __name__ == '__main__':
    profile_chiefs_parser()
    profile_chief_road_parser()
    profile_nstationary_parser()
    profile_buildings_parser()
    profile_target_parser()
    profile_born_place_parser()
    profile_static_camera_parser()
    profile_front_marker_parser()
    profile_rocket_parser()
    profile_flight_route_parser()

# -*- coding: utf-8 -*-

import six
import sys

from .exceptions import MissionParsingError
from .sections.main import MainSectionParser
from .sections.season import SeasonSectionParser
from .sections.weather import WeatherSectionParser
from .sections.respawn_time import RespawnTimeSectionParser
from .sections.mds import MDSSectionParser
from .sections.mds_scouts import MDSScoutsSectionParser
from .sections.chiefs import ChiefsSectionParser
from .sections.chief_road import ChiefRoadSectionParser
from .sections.nstationary import NStationarySectionParser
from .sections.buildings import BuildingsSectionParser
from .sections.target import TargetSectionParser
from .sections.born_place import BornPlaceSectionParser
from .sections.born_place_aircrafts import BornPlaceAircraftsSectionParser
from .sections.born_place_air_forces import BornPlaceAirForcesSectionParser
from .sections.static_camera import StaticCameraSectionParser
from .sections.front_marker import FrontMarkerSectionParser
from .sections.rocket import RocketSectionParser
from .sections.wing import WingSectionParser
from .sections.flight_info import FlightInfoSectionParser
from .sections.flight_route import FlightRouteSectionParser
from .utils import move_if_present, set_if_present, strip_comments


class MissionParser(object):
    """
    Parses a whole mission file.
    View :ref:`detailed description <file-parser>`.
    """

    def __init__(self):
        self.parsers = [
            MainSectionParser(),
            SeasonSectionParser(),
            WeatherSectionParser(),
            RespawnTimeSectionParser(),
            MDSSectionParser(),
            MDSScoutsSectionParser(),
            ChiefsSectionParser(),
            ChiefRoadSectionParser(),
            NStationarySectionParser(),
            BuildingsSectionParser(),
            TargetSectionParser(),
            BornPlaceSectionParser(),
            BornPlaceAircraftsSectionParser(),
            BornPlaceAirForcesSectionParser(),
            StaticCameraSectionParser(),
            FrontMarkerSectionParser(),
            RocketSectionParser(),
            WingSectionParser(),
            FlightRouteSectionParser(),
        ]
        self.flight_info_parser = FlightInfoSectionParser()

    def parse(self, mission):
        if isinstance(mission, six.string_types):
            with open(mission, 'r') as f:
                return self.parse_stream(f)
        else:
            return self.parse_stream(mission)

    def parse_stream(self, sequence):
        self._current_parser = None
        self.data = {}

        for i, line in enumerate(sequence):
            line = strip_comments(line)
            if self.is_section_name(line):
                self._finalize_current_parser()
                section_name = self.get_section_name(line)
                self._current_parser = self._get_parser(section_name)
            elif self._current_parser:
                self._try_to_parse_line(i, line)

        self._finalize_current_parser()
        return self._clean()

    @staticmethod
    def is_section_name(line):
        return line.startswith('[') and line.endswith(']')

    @staticmethod
    def get_section_name(line):
        return line.strip('[]')

    def _get_parser(self, section_name):
        parser = self.flight_info_parser
        flights = self.data.get('flights')

        if flights is not None and parser.start(section_name):
            return parser

        for parser in self.parsers:
            if parser.start(section_name):
                return parser

        return None

    def _finalize_current_parser(self):
        if not self._current_parser:
            return
        try:
            data = self._current_parser.stop()
        except Exception:
            error_type, original_msg, traceback = sys.exc_info()
            msg = (
                "{0} during finalization of \"{1}\": {2}"
                .format(error_type.__name__,
                        self._current_parser.__class__.__name__,
                        original_msg))
            self._raise_error(msg, traceback)
        else:
            self.data.update(data)
        finally:
            self._current_parser = None

    def _try_to_parse_line(self, line_number, line):
        try:
            self._current_parser.parse_line(line)
        except Exception:
            error_type, original_msg, traceback = sys.exc_info()
            msg = (
                "{0} in line #{1} (\"{2}\"): {3}"
                .format(error_type.__name__, line_number, line, original_msg))
            self._raise_error(msg, traceback)

    @staticmethod
    def _raise_error(message, traceback):
        error = MissionParsingError(message)
        six.reraise(MissionParsingError, error, traceback)

    def _clean(self):
        result = {}

        move_if_present(result, self.data, 'location_loader')
        move_if_present(result, self.data, 'player')
        move_if_present(result, self.data, 'targets')

        set_if_present(result, 'conditions', self._get_conditions())
        set_if_present(result, 'objects', self._get_objects())

        return result

    def _get_conditions(self):
        result = {}

        set_if_present(result, 'time_info', self._get_time_info())
        set_if_present(result, 'meteorology', self._get_meteorology())
        set_if_present(result, 'scouting', self._get_scouting())

        move_if_present(result, self.data, 'respawn_time')

        if 'conditions' in self.data:
            conditions = self.data['conditions']

            move_if_present(result, conditions, 'radar')
            move_if_present(result, conditions, 'communication')
            move_if_present(result, conditions, 'home_bases')
            move_if_present(result, conditions, 'crater_visibility_muptipliers')

        return result

    def _get_time_info(self):
        result = {}

        move_if_present(result, self.data, 'date')
        if 'time' in self.data:
            result.update({
                'time': self.data['time']['value'],
                'is_fixed': self.data['time']['is_fixed'],
            })

        return result

    def _get_meteorology(self):
        result = {}

        move_if_present(result, self.data, 'weather', 'weather_conditions')
        move_if_present(result, self.data, 'cloud_base')

        if 'weather' in self.data:
            result.update(self.data.pop('weather'))

        return result

    def _get_scouting(self):
        result = {}

        try:
            conditions = self.data['conditions'].pop('scouting')
            result.update(conditions)
        except KeyError:
            pass

        keys = filter(
            lambda x: x.startswith(MDSScoutsSectionParser.output_prefix),
            self.data.keys()
        )
        scouts = {
            self.data[key]['belligerent']: self.data[key]['aircrafts']
            for key in keys
        }
        set_if_present(result, 'scouts', scouts)

        return result

    def _get_objects(self):
        result = {}

        set_if_present(result, 'moving_units', self._get_moving_units())
        set_if_present(result, 'flights', self._get_flights())
        set_if_present(result, 'home_bases', self._get_home_bases())

        move_if_present(result, self.data, 'stationary')
        move_if_present(result, self.data, 'buildings')
        move_if_present(result, self.data, 'cameras')
        move_if_present(result, self.data, 'markers')
        move_if_present(result, self.data, 'rockets')

        return result

    def _get_moving_units(self):
        units = self.data.pop('moving_units', [])
        for unit in units:
            key = "{}{}".format(ChiefRoadSectionParser.output_prefix, unit['id'])
            unit['route'] = self.data.pop(key, [])
        return units

    def _get_flights(self):
        keys = self.data.pop('flights', [])
        flights = [self.data.pop(key) for key in keys if key in self.data]
        for flight in flights:
            key = "{}{}".format(FlightRouteSectionParser.output_prefix, flight['id'])
            flight['route'] = self.data.pop(key, [])
        return flights

    def _get_home_bases(self):
        home_bases = self.data.pop('home_bases', [])
        for i, home_base in enumerate(home_bases):
            key = "{}{}".format(BornPlaceAircraftsSectionParser.output_prefix, i)
            home_base['spawning']['aircraft_limitations']['allowed_aircrafts'] = self.data.pop(key, [])

            key = "{}{}".format(BornPlaceAirForcesSectionParser.output_prefix, i)
            home_base['spawning']['allowed_air_forces'] = self.data.pop(key, [])
        return home_bases

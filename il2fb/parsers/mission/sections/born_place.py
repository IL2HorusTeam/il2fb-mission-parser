# coding: utf-8

from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.constants import WEAPONS_CONTINUATION_MARK
from il2fb.parsers.mission.converters import to_bool
from il2fb.parsers.mission.converters import to_belligerent
from il2fb.parsers.mission.converters import to_air_force
from il2fb.parsers.mission.sections.base import CollectingParser


class BornPlaceSectionParser(CollectingParser):
    """
    Parses ``BornPlace`` section.
    View :ref:`detailed description <bornplace-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "BornPlace"

    def parse_line(self, line):
        (
            belligerent, the_range, pos_x, pos_y, has_parachutes,
            air_spawn_height, air_spawn_speed, air_spawn_heading, max_pilots,
            radar_min_height, radar_max_height, radar_range, air_spawn_always,
            enable_aircraft_limits, aircraft_limits_consider_lost,
            disable_spawning, friction_enabled, friction_value,
            aircraft_limits_consider_stationary, show_default_icon,
            air_spawn_if_deck_is_full, spawn_in_stationary,
            return_to_start_position
        ) = line.split()

        self.data.append({
            'range': int(the_range),
            'belligerent': to_belligerent(belligerent),
            'show_default_icon': to_bool(show_default_icon),
            'friction': {
                'enabled': to_bool(friction_enabled),
                'value': float(friction_value),
            },
            'spawning': {
                'enabled': not to_bool(disable_spawning),
                'with_parachutes': to_bool(has_parachutes),
                'max_pilots': int(max_pilots),
                'in_stationary': {
                    'enabled': to_bool(spawn_in_stationary),
                    'return_to_start_position': to_bool(return_to_start_position),
                },
                'in_air': {
                    'height': int(air_spawn_height),
                    'speed': int(air_spawn_speed),
                    'heading': int(air_spawn_heading),
                    'conditions': {
                        'always': to_bool(air_spawn_always),
                        'if_deck_is_full': to_bool(air_spawn_if_deck_is_full),
                    },
                },
                'aircraft_limitations': {
                    'enabled': to_bool(enable_aircraft_limits),
                    'consider_lost': to_bool(aircraft_limits_consider_lost),
                    'consider_stationary': to_bool(aircraft_limits_consider_stationary),
                },
            },
            'radar': {
                'range': int(radar_range),
                'min_height': int(radar_min_height),
                'max_height': int(radar_max_height),
            },
            'pos': Point2D(pos_x, pos_y),
        })

    def clean(self):
        return {'home_bases': self.data, }


class BornPlaceAirForcesSectionParser(CollectingParser):
    """
    Parses ``BornPlaceCountriesN`` section.
    View :ref:`detailed description <bornplace-air-forces-section>`.
    """
    input_prefix = 'BornPlaceCountries'
    output_prefix = 'home_base_air_forces_'

    def check_section_name(self, section_name):
        if not section_name.startswith(self.input_prefix):
            return False
        try:
            self._extract_section_number(section_name)
        except ValueError:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(BornPlaceAirForcesSectionParser, self).init_parser(section_name)
        self.output_key = (
            "{0}{1}".format(self.output_prefix,
                            self._extract_section_number(section_name)))
        self.countries = {}

    def _extract_section_number(self, section_name):
        start = len(self.input_prefix)
        return int(section_name[start:])

    def parse_line(self, line):
        air_force = to_air_force(line.strip())
        self.data.append(air_force)

    def clean(self):
        return {self.output_key: self.data, }


class BornPlaceAircraftsSectionParser(CollectingParser):
    """
    Parses ``BornPlaceN`` section.
    View :ref:`detailed description <bornplace-aircrafts-section>`.
    """
    input_prefix = 'BornPlace'
    output_prefix = 'home_base_aircrafts_'

    def check_section_name(self, section_name):
        if not section_name.startswith(self.input_prefix):
            return False
        try:
            self._extract_section_number(section_name)
        except ValueError:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(BornPlaceAircraftsSectionParser, self).init_parser(section_name)
        self.output_key = (
            "{}{}".format(self.output_prefix,
                          self._extract_section_number(section_name)))
        self.aircraft = None

    def _extract_section_number(self, section_name):
        start = len(self.input_prefix)
        return int(section_name[start:])

    def parse_line(self, line):
        parts = line.split()

        if parts[0] == WEAPONS_CONTINUATION_MARK:
            self.aircraft['weapon_limitations'].extend(parts[1:])
        else:
            if self.aircraft:
                # Finalize previous aircraft
                self.data.append(self.aircraft)
            self.aircraft = self._parse_new_item(parts)

    @classmethod
    def _parse_new_item(cls, parts):
        code = parts.pop(0)
        limit = cls._extract_limit(parts)
        return {
            'code': code,
            'limit': limit,
            'weapon_limitations': parts,
        }

    @staticmethod
    def _extract_limit(parts):
        if parts:
            limit = int(parts.pop(0))
            limit = limit if limit >= 0 else None
        else:
            limit = None
        return limit

    def clean(self):
        if self.aircraft:
            aircraft, self.aircraft = self.aircraft, None
            self.data.append(aircraft)

        return {self.output_key: self.data, }

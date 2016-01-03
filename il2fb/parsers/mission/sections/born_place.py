# -*- coding: utf-8 -*-

from il2fb.commons.spatial import Point2D

from ..converters import to_bool, to_belligerent
from . import CollectingParser


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

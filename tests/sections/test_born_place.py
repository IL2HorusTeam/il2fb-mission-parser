# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.born_place import BornPlaceSectionParser

from .mixins import SectionParserTestCaseMixin


class BornPlaceSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``BornPlace`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "1 3000 121601 74883 1 1000 200 0 0 0 5000 50 0 1 1 0 0 3.8 1 0 0 0 0",
        ]
        expected = {
            'home_bases': [
                {
                    'range': 3000,
                    'belligerent': Belligerents.red,
                    'show_default_icon': False,
                    'friction': {
                        'enabled': False,
                        'value': 3.8,
                    },
                    'spawning': {
                        'enabled': True,
                        'with_parachutes': True,
                        'max_pilots': 0,
                        'in_stationary': {
                            'enabled': False,
                            'return_to_start_position': False,
                        },
                        'in_air': {
                            'height': 1000,
                            'speed': 200,
                            'heading': 0,
                            'conditions': {
                                'always': False,
                                'if_deck_is_full': False,
                            },
                        },
                        'aircraft_limitations': {
                            'enabled': True,
                            'consider_lost': True,
                            'consider_stationary': True,
                        },
                    },
                    'radar': {
                        'range': 50,
                        'min_height': 0,
                        'max_height': 5000,
                    },
                    'pos': Point2D(121601.0, 74883.0),
                },
            ]
        }
        self.assertParser(BornPlaceSectionParser, 'BornPlace', lines, expected)

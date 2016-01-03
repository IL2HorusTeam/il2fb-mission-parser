# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import AirForces, Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.born_place import (
    BornPlaceSectionParser, BornPlaceAirForcesSectionParser,
    BornPlaceAircraftsSectionParser,
)

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


class BornPlaceAirForcesSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``BornPlaceCountriesN`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "de",
            "ru",
            "nn",
        ]
        expected = {
            'home_base_air_forces_1': [
                AirForces.luftwaffe,
                AirForces.vvs_rkka,
                AirForces.none,
            ],
        }
        self.assertParser(BornPlaceAirForcesSectionParser, 'BornPlaceCountries1',
                          lines, expected)

    def test_invalid_section_name(self):
        parser = BornPlaceAirForcesSectionParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('BornPlaceCountriesX'))


class BornPlaceAircraftsSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``BornPlaceN`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "Bf-109F-4 -1 1sc250 4sc50",
            "Bf-109G-6_Late 0",
            "Ju-88A-4 10 28xSC50 28xSC50_2xSC250 28xSC50_4xSC250",
            "+ 2xSC1800 2xSC2000",
            "CantZ1007bis",
        ]
        expected = {
            'home_base_aircrafts_1': [
                {
                    'code': 'Bf-109F-4',
                    'limit': None,
                    'weapon_limitations': [
                        '1sc250',
                        '4sc50',
                    ],
                },
                {
                    'code': 'Bf-109G-6_Late',
                    'limit': 0,
                    'weapon_limitations': [],
                },
                {
                    'code': 'Ju-88A-4',
                    'limit': 10,
                    'weapon_limitations': [
                        '28xSC50',
                        '28xSC50_2xSC250',
                        '28xSC50_4xSC250',
                        '2xSC1800',
                        '2xSC2000',
                    ],
                },
                {
                    'code': 'CantZ1007bis',
                    'limit': None,
                    'weapon_limitations': [],
                },
            ],
        }
        self.assertParser(BornPlaceAircraftsSectionParser, 'BornPlace1', lines, expected)

    def test_invalid_section_name(self):
        parser = BornPlaceAircraftsSectionParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('BornPlaceX'))

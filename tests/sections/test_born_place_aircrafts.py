# -*- coding: utf-8 -*-

import unittest

from il2fb.parsers.mission.sections.born_place_aircrafts import BornPlaceAircraftsParser

from .mixins import SectionParserTestCaseMixin


class BornPlaceAircraftsParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
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
        self.assertParser(BornPlaceAircraftsParser, 'BornPlace1', lines, expected)

    def test_invalid_section_name(self):
        parser = BornPlaceAircraftsParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('BornPlaceX'))

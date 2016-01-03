# -*- coding: utf-8 -*-

import unittest

from il2fb.parsers.mission.sections.respawn_time import RespawnTimeSectionParser

from .mixins import SectionParserTestCaseMixin


class RespawnTimeSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``RespawnTime`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "Bigship 1000000",
            "Ship 1000000",
            "Aeroanchored 1000000",
            "Artillery 1000000",
            "Searchlight 1000000",
        ]
        expected = {
            'respawn_time': {
                'ships': {
                    'big': 1000000,
                    'small': 1000000,
                },
                'balloons': 1000000,
                'artillery': 1000000,
                'searchlights': 1000000,
            },
        }
        self.assertParser(RespawnTimeSectionParser, 'RespawnTime', lines, expected)

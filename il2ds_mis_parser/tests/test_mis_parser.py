# -*- coding: utf-8 -*-
"""
 Testing the application il2ds-mis-parser
"""
import unittest
from datetime import date

from il2ds_mis_parser.parsers import MainParser, SeasonParser


class MissionParserTestCase(unittest.TestCase):

    def test_parse_main(self):
        """
        The test parse a section MAIN with parameters
        """
        lines = [
            "MAP Moscow/sload.ini",
            "TIME 11.75",
            "CloudType 1",
            "CloudHeight 1500.0",
            "army 1",
            "playerNum 0",
        ]

        expected = {
            'MAP': 'Moscow/sload.ini',
            'army': '1',
            'playerNum': '0',
            'CloudHeight': '1500.0',
            'CloudType': '1',
            'TIME': '11.75'
        }

        parser = MainParser()
        for line in lines:
            parser.parse(line)
        self.assertEqual(expected, parser.clean())

    def test_parse_season(self):
        """
        Receipt date of the mission of section SEASON
        """
        lines = [
            "Year 1942",
            "Month 8",
            "Day 25",
        ]

        expected = date(1942, 8, 25)

        parser = SeasonParser()
        for line in lines:
            parser.parse(line)
        self.assertEqual(expected, parser.clean())
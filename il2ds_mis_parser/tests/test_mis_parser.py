# -*- coding: utf-8 -*-
"""
 Testing the application il2ds-mis-parser
"""
import unittest
from datetime import date

from il2ds_mis_parser.parsers import (MainParser, SeasonParser, RespawnTimeParser,
                                      WeatherParser,  MdsParser)


class MissionParserTestCase(unittest.TestCase):

    def _test_parse(self, parser, lines, expected):
        """
        """
        for line in lines:
            parser.parse(line)
        self.assertEqual(expected, parser.clean())

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

        self._test_parse(MainParser(), lines, expected)

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

        self._test_parse(SeasonParser(), lines, expected)

    def test_parse_weather(self):
        """
        The test parse a section WEATHER with parameters
        """
        lines = [
            "WindDirection 120.0",
            "WindSpeed 3.0",
            "Gust 0",
            "Turbulence 0",
        ]

        expected = {
            "WindDirection": "120.0",
            "WindSpeed": "3.0",
            "Gust": "0",
            "Turbulence": "0"
        }

        self._test_parse(WeatherParser(), lines, expected)

    def test_parse_respawn_time(self):
        """
        The test parse a section RespawnTime with parameters
        """
        lines = [
            "Bigship 1000000",
            "Ship 1000000",
            "Aeroanchored 1000000",
            "Artillery 1000000",
            "Searchlight 1000000",
        ]

        expected = {
            "Bigship": 1000000,
            "Ship": 1000000,
            "Aeroanchored": 1000000,
            "Artillery": 1000000,
            "Searchlight": 1000000
        }

        self._test_parse(RespawnTimeParser(), lines, expected)

    def test_parse_mds(self):
        """

        """
        lines = [
            "MDS_Radar_SetRadarToAdvanceMode 0",
            "MDS_Radar_DisableVectoring 1",
            "MDS_Radar_ShipRadar_MaxRange 100",
            "MDS_Radar_ShipRadar_MinHeight 100",
            "MDS_Radar_ShipRadar_MaxHeight 5000",
            "MDS_Radar_ShipSmallRadar_MaxRange 25",
            "MDS_Radar_ShipSmallRadar_MinHeight 0",
            "MDS_Radar_ShipSmallRadar_MaxHeight 2000",
            "MDS_Radar_ScoutsAsRadar 0",
            "MDS_Radar_ScoutRadar_MaxRange 2",
            "MDS_Misc_DisableAIRadioChatter 1",
            "MDS_Misc_DespawnAIPlanesAfterLanding 1",
            "MDS_Misc_HidePlayersCountOnHomeBase 0",
            "MDS_Misc_BombsCat1_CratersVisibilityMultiplier 1.0",
            "MDS_Misc_BombsCat2_CratersVisibilityMultiplier 1.0",
            "MDS_Misc_BombsCat3_CratersVisibilityMultiplier 1.0",
        ]

        expected = {
            "Radar": {
                "SetRadarToAdvanceMode": '0',
                "DisableVectoring": '1',
                "ShipRadar": {
                    "MaxRange": '100',
                    "MinHeight": '100',
                    "MaxHeight": '5000'
                },
                "ShipSmallRadar": {
                    "MaxRange": '25',
                    "MinHeight": '0',
                    "MaxHeight": '2000'
                },
                "ScoutsAsRadar": '0',
                "ScoutRadar": {
                    "MaxRange": '2'
                },
            },
            "Misc": {
                "DisableAIRadioChatter": '1',
                "DespawnAIPlanesAfterLanding": '1',
                "HidePlayersCountOnHomeBase": '0',
                "BombsCat1": {
                    "CratersVisibilityMultiplier": '1.0'
                },
                "BombsCat2": {
                    "CratersVisibilityMultiplier": '1.0'
                },
                "BombsCat3": {
                    "CratersVisibilityMultiplier": '1.0'
                },
            }
        }

        self._test_parse(MdsParser(), lines, expected)

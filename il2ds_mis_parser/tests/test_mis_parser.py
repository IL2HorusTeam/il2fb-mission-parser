# -*- coding: utf-8 -*-
"""
Mission parser tests.
"""
import unittest
from datetime import date

from il2ds_mis_parser.parsers import (MainParser, SeasonParser,
    RespawnTimeParser, WeatherParser, MDSParser, )


class MissionParserTestCase(unittest.TestCase):

    def _test_parser(self, parser, lines, expected):
        for line in lines:
            parser.parse(line)
        self.assertEqual(expected, parser.clean())

    def test_main_parser(self):
        """
        Test 'MAIN' section parser.
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
            'map': 'Moscow/sload.ini',
            'army': 1,
            'regiment_player': '0',
            'height_clouds': 1500.0,
            'type_clouds': 1,
            'time': '11.75',
        }
        self._test_parser(MainParser(), lines, expected)

    def test_season_parser(self):
        """
        Test 'SEASON' section parser.
        """
        lines = [
            "Year 1942",
            "Month 8",
            "Day 25",
        ]
        expected = date(1942, 8, 25)
        self._test_parser(SeasonParser(), lines, expected)

    def test_weather_parser(self):
        """
        Test 'WEATHER' section parser.
        """
        lines = [
            "WindDirection 120.0",
            "WindSpeed 3.0",
            "Gust 0",
            "Turbulence 0",
        ]
        expected = {
            'wind': {
                'direction': 120.0,
                'speed': 3.0,
            },
            'gust': 0,
            'turbulence': 0,
        }
        self._test_parser(WeatherParser(), lines, expected)

    def test_respawn_time_parser(self):
        """
        Test 'RespawnTime' section parser.
        """
        lines = [
            "Bigship 1000000",
            "Ship 1000000",
            "Aeroanchored 1000000",
            "Artillery 1000000",
            "Searchlight 1000000",
        ]
        expected = {
            'big_ship': 1000000,
            'small_ships': 1000000,
            'balloons': 1000000,
            'artillery': 1000000,
            'floodlights': 1000000,
        }
        self._test_parser(RespawnTimeParser(), lines, expected)

    def test_parse_mds(self):
        """
        Test 'MDS' section parser.
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
            'radar': {
                'advance_mode': False,
                'no_vectoring': True,
                'ships': {
                    'normal': {
                        'max_range': 100,
                        'min_height': 100,
                        'max_height': 5000,
                    },
                    'small': {
                        'max_range': 25,
                        'min_height': 0,
                        'max_height': 2000,
                    },
                },
                'scouts': {
                    'treat_as_radar': False,
                    'max_range': 2,
                },
            },
            'ai': {
                'no_radio_chatter': True,
                'hide_planes_after_landing': True,
            },
            'bomb_crater_visibility_muptiplier': {
                'cat1': 1.0,
                'cat2': 1.0,
                'cat3': 1.0,
            },
            'no_players_count_on_home_base': False,
        }
        self._test_parser(MDSParser(), lines, expected)

# -*- coding: utf-8 -*-
"""
Mission parser tests.
"""
import unittest
from datetime import date

from il2ds_mis_parser.parsers import (MainParser, SeasonParser,
    RespawnTimeParser, WeatherParser, MDSParser, NStationaryParser,
    BuildingsParser, StaticCameraParser, TargetParser, FrontMarkerParser)


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
            'player_regiment': '0',
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
            'big_ships': 1000000,
            'small_ships': 1000000,
            'balloons': 1000000,
            'artillery': 1000000,
            'searchlight': 1000000,
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

    def test_parse_stationary(self):
        """
        Test 'NStationary' section parser.
        """
        lines = [
            "959_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1",
            "49_Static vehicles.stationary.Stationary$OpelBlitz6700A_fuel 2 43726.71 58239.31 540.00 0.0",
            "171_Static vehicles.stationary.Stationary$OpelBlitz6700A_fuel 2 45107.15 58463.06 600.00 0.0",
        ]

        expected = [
            "959_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1",
            "49_Static vehicles.stationary.Stationary$OpelBlitz6700A_fuel 2 43726.71 58239.31 540.00 0.0",
            "171_Static vehicles.stationary.Stationary$OpelBlitz6700A_fuel 2 45107.15 58463.06 600.00 0.0",
        ]

        self._test_parser(NStationaryParser(), lines, expected)

    def test_parse_buildings(self):
        """
        Test 'Buildings' section parser.
        """
        lines = [
            "0_bld House$Tent_Pyramid_US 1 43471.34 57962.08 630.00",
            "12_bld House$46FTankDE 1 43722.70 58106.67 555.00",
            "38_bld House$FurnitureTreeBroad1 1 43725.10 58081.35 475.0",
        ]

        expected = [
            "0_bld House$Tent_Pyramid_US 1 43471.34 57962.08 630.00",
            "12_bld House$46FTankDE 1 43722.70 58106.67 555.00",
            "38_bld House$FurnitureTreeBroad1 1 43725.10 58081.35 475.0",
        ]

        self._test_parser(BuildingsParser(), lines, expected)

    def test_parse_static_camera(self):
        """
        Test 'StaticCamera' section parser.
        """
        lines = [
            "38426 65212 35 2",
        ]

        expected = {
            'pos': {
                'x': 38426,
                'y': 65212,
            },
            'height': 35,
            'army': 2,
        }

        self._test_parser(StaticCameraParser(), lines, expected)

    def test_parse_target(self):
        """
        Test 'Target' section parser.
        """
        lines = [
            "0 0 0 0 500 90939 91871 0",
            "3 1 1 30 500 90681 91687 500",
            "3 2 1 30 500 90681 91687 500 0 0_Chief 91100 91500",
        ]

        expected = [
            {
                'type': "destroy",
                'priority': "main",
                'sleep_mode': False,
                'timeout': 0,
                'destruction_level': 50,
                'pos': {
                    'x': 90939,
                    'y': 91871,
                },
            },
            {
                'type': "recon",
                'priority': "additional",
                'sleep_mode': True,
                'timeout': 30,
                'requires_landing': False,
                'pos': {
                    'x': 90681,
                    'y': 91687,
                },
                'radius': 500,
            },
            {
                'type': "recon",
                'priority': "hidden",
                'sleep_mode': True,
                'timeout': 30,
                'requires_landing': False,
                'pos': {
                    'x': 90681,
                    'y': 91687,
                },
                'radius': 500,
                'object': "0_Chief",
            },
        ]

        self._test_parser(TargetParser(), lines, expected)

    def test_parse_front_marker(self):
        """
        Test 'FrontMarker' section parser.
        """
        lines = [
            "FrontMarker0 7636.65 94683.02 1",
        ]

        expected = [
            {
                'code': "FrontMarker0",
                'pos': {
                    'x': 7636.65,
                    'y': 94683.02,
                },
                'army': 1,
            }
        ]

        self._test_parser(FrontMarkerParser(), lines, expected)
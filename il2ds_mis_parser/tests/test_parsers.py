# -*- coding: utf-8 -*-
"""
Mission parser tests.
"""
import datetime
import unittest

from il2ds_mis_parser.parsers import (
    MainParser, SeasonParser, RespawnTimeParser, WeatherParser, MDSParser,
    NStationaryParser, BuildingsParser, StaticCameraParser, TargetParser,
    FrontMarkerParser, BornPlaceParser, ChiefsParser,
)


class MissionParserTestCase(unittest.TestCase):

    maxDiff = 5000

    def _test_parser(self, parser_class, section_name, lines, expected):
        parser = parser_class()
        self.assertTrue(parser.start(section_name))
        for line in lines:
            parser.parse_line(line)
        self.assertEqual(expected, parser.stop())

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
            'loader': 'Moscow/sload.ini',
            'army_code': 1,
            'player_regiment': '0',
            'clouds': {
                'height': 1500,
                'type': 1,
            },
            'time': datetime.time(11, 45),
        }
        self._test_parser(MainParser, 'MAIN', lines, expected)

    def test_season_parser(self):
        """
        Test 'SEASON' section parser.
        """
        lines = [
            "Year 1942",
            "Month 8",
            "Day 25",
        ]
        expected = {
            'date': datetime.date(1942, 8, 25),
        }
        self._test_parser(SeasonParser, 'SEASON', lines, expected)

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
            'weather': {
                'wind': {
                    'direction': 120.0,
                    'speed': 3.0,
                },
                'gust': 0,
                'turbulence': 0,
            },
        }
        self._test_parser(WeatherParser, 'WEATHER', lines, expected)

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
            'respawn_time': {
                'ship': {
                    'big': 1000000,
                    'small': 1000000,
                },
                'balloon': 1000000,
                'artillery': 1000000,
                'searchlight': 1000000,
            },
        }
        self._test_parser(RespawnTimeParser, 'RespawnTime', lines, expected)

    def test_mds_parser(self):
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
                'vectoring': False,
                'ships': {
                    'big': {
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
            'bomb_crater_visibility_muptipliers': {
                'le_100kg': 1.0,
                'le_1000kg': 1.0,
                'gt_1000kg': 1.0,
            },
            'no_players_count_on_home_base': False,
        }
        self._test_parser(MDSParser, 'MDS', lines, expected)

    def test_stationary_parser(self):
        """
        Test 'NStationary' section parser.
        """
        lines = [
            "959_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1",
            "49_Static vehicles.stationary.Stationary$OpelBlitz6700A_fuel 2 43726.71 58239.31 540.00 0.0",
            "171_Static vehicles.stationary.Stationary$OpelBlitz6700A_fuel 2 45107.15 58463.06 600.00 0.0",
        ]
        expected = {
            'statics': [],
        }
        self._test_parser(NStationaryParser, 'NStationary', lines, expected)

    def test_buildings_parser(self):
        """
        Test 'Buildings' section parser.
        """
        lines = [
            "0_bld House$Tent_Pyramid_US 1 43471.34 57962.08 630.00",
            "12_bld House$46FTankDE 1 43722.70 58106.67 555.00",
            "38_bld House$FurnitureTreeBroad1 1 43725.10 58081.35 475.0",
        ]
        expected = {
            'buildings': [],
        }
        self._test_parser(BuildingsParser, 'Buildings', lines, expected)

    def test_static_camera_parser(self):
        """
        Test 'StaticCamera' section parser.
        """
        lines = [
            "38426 65212 35 2",
        ]
        expected = {
            'cameras': [
                {
                    'army_code': 2,
                    'pos': {
                        'x': 38426,
                        'y': 65212,
                        'z': 35,
                    },
                },
            ],
        }
        self._test_parser(StaticCameraParser, 'StaticCamera', lines, expected)

    def test_target_parser(self):
        """
        Test 'Target' section parser.
        """
        lines = [
            "0 0 0 0 500 90939 91871 0 0 10_Chief 91100 91500",
            "3 1 1 30 500 90681 91687 500",
            "3 2 1 30 500 90681 91687 500 0 0_Chief 91100 91500",
        ]
        expected = {
            'targets': [
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
                    'object_code': "10_Chief",
                },
                {
                    'type': "recon",
                    'priority': "extra",
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
                    'object_code': "0_Chief",
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_born_place_parser(self):
        """
        Test 'BornPlace' section parser.
        """
        lines = [
            "1 3000 121601 74883 1 1000 200 0 0 0 5000 50 0 1 1 0 0 3.8 1 0 0 0 0",
        ]
        expected = {
            'homebases': [
                {
                    'radius': 3000,
                    'army_code': 1,
                    'show_default_icon': False,
                    'friction': {
                        'enabled': False,
                        'value': 3.8,
                    },
                    'spawning': {
                        'enabled': True,
                        'return_to_start_position': False,
                        'parachute': True,
                        'max_allowed_pilots': 0,
                        'aircraft_limits': {
                            'enabled': True,
                            'consider_lost': True,
                            'consider_destroyed_stationary': True,
                        },
                        'in_stationary': False,
                        'in_air': {
                            'height': 1000,
                            'speed': 200,
                            'heading': 0,
                            'conditions': {
                                'always': False,
                                'if_deck_is_full': False,
                            },
                        },
                    },
                    'recon': {
                        'range': 50,
                        'min_height': 0,
                        'max_height': 5000,
                    },
                    'pos': {
                        'x': 121601,
                        'y': 74883,
                    },
                },
            ]
        }
        self._test_parser(BornPlaceParser, 'BornPlace', lines, expected)

    def test_front_marker_parser(self):
        """
        Test 'FrontMarker' section parser.
        """
        lines = [
            "FrontMarker0 7636.65 94683.02 1",
        ]
        expected = {
            'markers': [
                {
                    'code': "FrontMarker0",
                    'pos': {
                        'x': 7636.65,
                        'y': 94683.02,
                    },
                    'army_code': 1,
                },
            ],
        }
        self._test_parser(FrontMarkerParser, 'FrontMarker', lines, expected)

    def test_chiefs_parser(self):
        lines = [
            "0_Chief Vehicles.US_Supply_Cpy 1",
            "1_Chief Trains.Germany_CargoTrain/AA 2",
        ]
        expected = {
            'chiefs': [
                {
                    'code': "0_Chief",
                    'code_name': "US_Supply_Cpy",
                    'type': "vehicles",
                    'army_code': 1,
                },
                {
                    'code': "1_Chief",
                    'code_name': "Germany_CargoTrain/AA",
                    'type': "trains",
                    'army_code': 2,
                },
            ],
        }
        self._test_parser(ChiefsParser, 'Chiefs', lines, expected)

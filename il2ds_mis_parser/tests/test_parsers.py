# -*- coding: utf-8 -*-
"""
Mission parser tests.
"""
import datetime
import unittest

from il2ds_mis_parser.parsers import (to_bool, to_pos, SectionParser,
    MainParser, SeasonParser, RespawnTimeParser, WeatherParser, MDSParser,
    NStationaryParser, BuildingsParser, StaticCameraParser, TargetParser,
    FrontMarkerParser, BornPlaceParser, ChiefsParser, BornPlaceAircraftsParser,
    BornPlaceCountriesParser, RocketParser, ChiefRoadParser, WingParser,
    MDSScoutsParser, FlightDetailsParser,)


class CommonsTestCase(unittest.TestCase):

    def test_to_bool(self):
        self.assertFalse(to_bool('0'))
        self.assertTrue(to_bool('1'))
        self.assertTrue(to_bool('-1'))

    def test_to_pos(self):
        self.assertEqual(to_pos('100', '200'), {'x': 100, 'y': 200, })
        self.assertEqual(
            to_pos('100', '200', '300'), {'x': 100, 'y': 200, 'z': 300, })


class SectionParserTestCase(unittest.TestCase):

    class FooParser(SectionParser):

        def check_section_name(self, section_name):
            return True

        def init_parser(self, section_name):
            pass

        def parse_line(self, line):
            pass

    def setUp(self):
        self.parser = SectionParserTestCase.FooParser()

    def test_process_data(self):
        self.parser.start("foo")
        result = self.parser.stop()
        self.assertIsNone(result)

    def test_stop_with_failure(self):
        self.assertRaises(RuntimeError, self.parser.stop)


class ParserTestCaseMixin(object):

    maxDiff = 5000

    def _test_parser(self, parser_class, section_name, lines, expected):
        parser = parser_class()
        self.assertTrue(parser.start(section_name))
        for line in lines:
            parser.parse_line(line)
        self.assertEqual(expected, parser.stop())


class MissionParserTestCase(unittest.TestCase, ParserTestCaseMixin):

    def test_main_parser(self):
        """
        Test 'MAIN' section parser.
        """
        lines = [
            "MAP Moscow/sload.ini",
            "TIME 11.75",
            "TIMECONSTANT 1",
            "WEAPONSCONSTANT 1",
            "CloudType 1",
            "CloudHeight 1500.0",
            "player fiLLv24fi00",
            "army 1",
            "playerNum 0",
        ]
        expected = {
            'loader': 'Moscow/sload.ini',
            'time': {
                'value': datetime.time(11, 45),
                'is_fixed': True,
            },
            'fixed_loadout': True,
            'weather_type': 'clear',
            'clouds_height': 1500,
            'player': {
                'army': 'red',
                'regiment': "fiLLv24fi00",
                'number': 0,
            },
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
                'gust': 'none',
                'turbulence': 'none',
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

    def test_mds_scouts_parser(self):
        lines = [
            "B-25H-1NA",
            "B-25J-1NA",
            "BeaufighterMk21",
        ]

        expected = {
            'scout_plane_red': [
                "B-25H-1NA",
                "B-25J-1NA",
                "BeaufighterMk21",
            ]
        }
        self._test_parser(MDSScoutsParser, 'MDS_Scouts_Red', lines, expected)


    def test_stationary_parser(self):
        """
        Test 'NStationary' section parser.
        """
        lines = [
            "959_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1",
            "0_Static vehicles.planes.Plane$I_16TYPE24 2 134146.89 88005.43 336.92 0.0 de 2 1.0 I-16type24_G1_RoW3.bmp 1",
            "1_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4",
        ]
        expected = {
            'statics': [
                {
                    'army': 'blue',
                    'code': '959_Static',
                    'code_name': 'SdKfz251',
                    'is_spotter': True,
                    'pos': {
                        'x': 31333.62,
                        'y': 90757.91,
                    },
                    'rotation_angle': 600.29,
                    'range': 0,
                    'skill': 'rookie',
                },
                {
                    'air_force': 'luftwaffe',
                    'allows_spawning': True,
                    'army': 'blue',
                    'skin': 'I-16type24_G1_RoW3.bmp',
                    'code': '0_Static',
                    'code_name': 'I_16TYPE24',
                    'markings': True,
                    'pos': {
                        'x': 134146.89,
                        'y': 88005.43,
                    },
                    'rotation_angle': 336.92,
                    'restorable': True,
                },
                {
                    'army': 'red',
                    'code': '1_Static',
                    'code_name': 'G5',
                    'recharge_time': 1.4,
                    'pos': {
                        'x': 83759.05,
                        'y': 115021.15,
                    },
                    'rotation_angle': 360.00,
                    'skill': 'ace',
                    'timeout': 60
                },
            ],
        }
        self._test_parser(NStationaryParser, 'NStationary', lines, expected)

    def test_buildings_parser(self):
        """
        Test 'Buildings' section parser.
        """
        lines = [
            "0_bld House$Tent_Pyramid_US 1 43471.34 57962.08 630.00",
        ]
        expected = {
            'buildings': [
                {
                    'code': '0_bld',
                    'type': 'House',
                    'code_name': 'Tent_Pyramid_US',
                    'army': 'red',
                    'pos': {
                        'y': 57962.08,
                        'x': 43471.34,
                    },
                    'rotation_angle': 630.00
                }
            ],
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
                    'army': "blue",
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
                    'army': "red",
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

    def test_born_place_aircraft_parser(self):
        """
        Test 'BornPlaceN' section parser.
        """
        lines = [
            "Bf-109F-4 -1 1sc250 4sc50",
            "Ju-88A-4 10 28xSC50 28xSC50_2xSC250 28xSC50_4xSC250",
            "+ 2xSC1800 2xSC2000",
        ]
        expected = {
            'homebase_aircrafts_9999': [
                {
                    'aircraft_code': 'Bf-109F-4',
                    'limit': None,
                    'loadout': [
                        '1sc250',
                        '4sc50',
                    ],
                },
                {
                    'aircraft_code': 'Ju-88A-4',
                    'limit': 10,
                    'loadout': [
                        '28xSC50',
                        '28xSC50_2xSC250',
                        '28xSC50_4xSC250',
                        '2xSC1800',
                        '2xSC2000',
                    ],
                },
            ],
        }
        self._test_parser(BornPlaceAircraftsParser, 'BornPlace9999',
                          lines, expected)

    def test_born_place_countries_parser(self):
        """
        Test 'BornPlaceCountriesN' section parser.
        """
        lines = [
            "de",
            "ru",
        ]
        expected = {
            'homebase_countries_9999': [
                "de",
                "ru",
            ],
        }
        self._test_parser(BornPlaceCountriesParser, 'BornPlaceCountries9999',
                          lines, expected)

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
                    'army': "red",
                },
            ],
        }
        self._test_parser(FrontMarkerParser, 'FrontMarker', lines, expected)

    def test_chiefs_parser(self):
        lines = [
            "0_Chief Vehicles.US_Supply_Cpy 1",
            "1_Chief Trains.Germany_CargoTrain/AA 2",
            "2_Chief Ships.G5 1 60 1 1.0",
        ]
        expected = {
            'chiefs': [
                {
                    'code': "0_Chief",
                    'code_name': "US_Supply_Cpy",
                    'type': "vehicles",
                    'army': "red",
                },
                {
                    'code': "1_Chief",
                    'code_name': "Germany_CargoTrain/AA",
                    'type': "trains",
                    'army': "blue",
                },
                {
                    'code': "2_Chief",
                    'code_name': "G5",
                    'type': "ships",
                    'army': "red",
                    'timeout': 60,
                    'skill': "rookie",
                    'recharge_time': 1.0,
                },
            ],
        }
        self._test_parser(ChiefsParser, 'Chiefs', lines, expected)

    def test_chiefs_road_parser(self):
        lines = [
            "21380.02 41700.34 120.00 10 0 3.055555582046509",
            "21500.00 41700.00 20.00",
            "50299.58 35699.85 120.00 10 33 2.6388890743255615",
        ]
        expected = {
            '0_chief_road': [
                {
                    'pos': {
                    'x': 21380.02,
                    'y': 41700.34,
                    },
                    'timeout': 10,
                },
                {
                    'pos': {
                    'x': 21500.00,
                    'y': 41700.00,
                    },
                },
                {
                    'pos': {
                    'x': 50299.58,
                    'y': 35699.85,
                    },
                    'timeout': 10,
                },
            ]
        }
        self._test_parser(ChiefRoadParser, '0_Chief_Road', lines, expected)

    def test_rocket_parser(self):
        lines = [
            "0_Rocket Fi103_V1_ramp 2 84141.38 114216.82 360.00 60.0 10 80.0 83433.91 115445.49",
            "1_Rocket Fi103_V1_ramp 2 84141.38 114216.82 360.00 60.0 10 80.0",
        ]
        expected = {
            'rockets': [
                {
                    'code': "0_Rocket",
                    'code_name': "Fi103_V1_ramp",
                    'army': "blue",
                    'pos': {
                        'x': 84141.38,
                        'y': 114216.82,
                    },
                    'rotation_angle': 360.00,
                    'timeout': 60.0,
                    'amount': 10,
                    'period': 80.0,
                    'target_pos': {
                        'x': 83433.91,
                        'y': 115445.49,
                    },
                },
                {
                    'code': "1_Rocket",
                    'code_name': "Fi103_V1_ramp",
                    'army': "blue",
                    'pos': {
                        'x': 84141.38,
                        'y': 114216.82,
                    },
                    'rotation_angle': 360.00,
                    'timeout': 60.0,
                    'amount': 10,
                    'period': 80.0,
                    'target_pos': None,
                },
            ],
        }
        self._test_parser(RocketParser, 'Rocket', lines, expected)

    def test_wing_parser(self):
        lines = [
            "1GvIAP12",
            "1GvIAP13",
        ]
        expected = {
            'flights': [
                "1GvIAP12",
                "1GvIAP13",
            ],
        }
        self._test_parser(WingParser, 'Wing', lines, expected)


class FlightDetailsParserTestCase(unittest.TestCase, ParserTestCaseMixin):

    maxDiff = 5000

    def test_flight_details_parser(self):
        lines = [
            "Planes 2",
            "Skill0 1",
            "Class air.A_20C",
            "Fuel 100",
            "weapons default",
            "Skill0 1",
            "Skill1 2",
            "skin0 Funky.bmp",
            "numberOn1 0",
            "spawn0 0_Static",
        ]

        expected = {
            '3GvIAP00_details': {
                'regiment_code': "3GvIAP",
                'squadron_number': 1,
                'flight_number': 1,
                'aircrafts_count': 2,
                'aircraft_code': "A_20C",
                'fuel': 100,
                'loadout': "default",
                'parachute_present': True,
                'only_ai': False,
                'aircrafts': [
                    {
                        'number': 1,
                        'skill': "rookie",
                        'aircraft_skin': "Funky.bmp",
                        'pilot_skin': "default",
                        'has_markings': True,
                        'spawn_point': "0_Static",
                    },
                    {
                        'number': 2,
                        'skill': "veteran",
                        'aircraft_skin': "default",
                        'pilot_skin': "default",
                        'has_markings': False,
                        'spawn_point': None,
                    },
                ],
            },
        }
        self._test_parser(FlightDetailsParser, '3GvIAP00', lines, expected)

    def test_flight_details_solo_parser(self):
        lines = [
            "Planes 1",
            "Skill 1",
            "Class air.A_20C",
            "Fuel 100",
            "weapons default",
            "skin0 Funky.bmp",
            "numberOn0 0",
            "spawn0 0_Static",
        ]

        expected = {
            '3GvIAP01_details': {
                'regiment_code': "3GvIAP",
                'squadron_number': 1,
                'flight_number': 2,
                'aircrafts_count': 1,
                'aircraft_code': "A_20C",
                'fuel': 100,
                'loadout': "default",
                'parachute_present': True,
                'only_ai': False,
                'aircrafts': [
                    {
                        'number': 1,
                        'skill': "rookie",
                        'aircraft_skin': "Funky.bmp",
                        'pilot_skin': "default",
                        'has_markings': False,
                        'spawn_point': "0_Static",
                    },
                ],
            },
        }
        self._test_parser(FlightDetailsParser, '3GvIAP01', lines, expected)

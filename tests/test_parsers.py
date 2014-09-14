# -*- coding: utf-8 -*-
"""
Mission parser tests.
"""
import datetime
import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.organization import AirForces, Belligerents, Regiments
from il2fb.commons.targets import TargetTypes, TargetPriorities
from il2fb.commons.weather import Conditions, Gust, Turbulence

from il2fb.parsers.mission.parsers import (
    to_bool, to_pos, to_belligerent, to_skill, to_unit_type, SectionParser,
    MainParser, SeasonParser, RespawnTimeParser, WeatherParser, MDSParser,
    NStationaryParser, BuildingsParser, StaticCameraParser, TargetParser,
    FrontMarkerParser, BornPlaceParser, ChiefsParser, BornPlaceAircraftsParser,
    BornPlaceAirForcesParser, RocketParser, ChiefRoadParser, WingParser,
    MDSScoutsParser, FlightInfoParser, FlightRouteParser,
)


class CommonsTestCase(unittest.TestCase):

    def test_to_bool(self):
        self.assertFalse(to_bool('0'))
        self.assertTrue(to_bool('1'))
        self.assertTrue(to_bool('-1'))

    def test_to_pos(self):
        self.assertEqual(
            to_pos('100', '200'), {'x': 100, 'y': 200, }
        )
        self.assertEqual(
            to_pos('100', '200', '300'), {'x': 100, 'y': 200, 'z': 300, }
        )

    def test_to_belligerent(self):
        self.assertEqual(to_belligerent('0'), Belligerents.none)
        self.assertEqual(to_belligerent('1'), Belligerents.red)
        self.assertEqual(to_belligerent('2'), Belligerents.blue)

    def test_to_skill(self):
        self.assertEqual(to_skill('3'), Skills.ace)

    def test_to_unit_type(self):
        self.assertEqual(to_unit_type('planes'), UnitTypes.airplane)


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

    maxDiff = None

    def _test_parser(self, parser_class, section_name, lines, expected):
        parser = parser_class()
        self.assertTrue(parser.start(section_name))
        for line in lines:
            parser.parse_line(line)
        self.assertEqual(expected, parser.stop())


class MissionParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    def test_main_parser(self):
        """
        Test ``MAIN`` section parser.
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
            'weather_conditions': Conditions.good,
            'cloud_base': 1500,
            'player': {
                'belligerent': Belligerents.red,
                'regiment': "fiLLv24fi00",
                'number': 0,
            },
        }
        self._test_parser(MainParser, 'MAIN', lines, expected)

    def test_season_parser(self):
        """
        Test ``SEASON`` section parser.
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
        Test ``WEATHER`` section parser.
        """
        lines = [
            "WindDirection 120.0",
            "WindSpeed 3.0",
            "Gust 0",
            "Turbulence 4",
        ]
        expected = {
            'weather': {
                'wind': {
                    'direction': 120.0,
                    'speed': 3.0,
                },
                'gust': Gust.none,
                'turbulence': Turbulence.very_strong,
            },
        }
        self._test_parser(WeatherParser, 'WEATHER', lines, expected)

    def test_mds_parser(self):
        """
        Test ``MDS`` section parser.
        """
        lines = [
            "MDS_Radar_SetRadarToAdvanceMode 1",
            "MDS_Radar_RefreshInterval 0",
            "MDS_Radar_DisableVectoring 0",
            "MDS_Radar_EnableTowerCommunications 1",
            "MDS_Radar_ShipsAsRadar 0",
            "MDS_Radar_ShipRadar_MaxRange 100",
            "MDS_Radar_ShipRadar_MinHeight 100",
            "MDS_Radar_ShipRadar_MaxHeight 5000",
            "MDS_Radar_ShipSmallRadar_MaxRange 25",
            "MDS_Radar_ShipSmallRadar_MinHeight 0",
            "MDS_Radar_ShipSmallRadar_MaxHeight 2000",
            "MDS_Radar_ScoutsAsRadar 0",
            "MDS_Radar_ScoutRadar_MaxRange 2",
            "MDS_Radar_ScoutRadar_DeltaHeight 1500",
            "MDS_Radar_ScoutGroundObjects_Alpha 5",
            "MDS_Radar_ScoutCompleteRecon 0",
            "MDS_Misc_DisableAIRadioChatter 0",
            "MDS_Misc_DespawnAIPlanesAfterLanding 1",
            "MDS_Radar_HideUnpopulatedAirstripsFromMinimap 0",
            "MDS_Misc_HidePlayersCountOnHomeBase 0",
            "MDS_Misc_BombsCat1_CratersVisibilityMultiplier 1.0",
            "MDS_Misc_BombsCat2_CratersVisibilityMultiplier 1.0",
            "MDS_Misc_BombsCat3_CratersVisibilityMultiplier 1.0",
        ]
        expected = {
            'radar': {
                'advanced_mode': True,
                'refresh_interval': 0,
                'ships': {
                    'treat_as_radar': False,
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
                    'max_height': 1500,
                    'alpha': 5,
                },
            },
            'ai': {
                'no_radio_chatter': False,
                'hide_aircrafts_after_landing': True,
            },
            'homebase': {
                'tower_communications': True,
                'hide_unpopulated': False,
                'hide_players_count': False,
            },
            'crater_visibility_muptipliers': {
                'le_100kg': 1.0,
                'le_1000kg': 1.0,
                'gt_1000kg': 1.0,
            },
            'vectoring': True,
            'only_scounts_complete_recon_targets': False,
        }
        self._test_parser(MDSParser, 'MDS', lines, expected)

    def test_respawn_time_parser(self):
        """
        Test ``RespawnTime`` section parser.
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
                'ships': {
                    'big': 1000000,
                    'small': 1000000,
                },
                'balloons': 1000000,
                'artillery': 1000000,
                'searchlights': 1000000,
            },
        }
        self._test_parser(RespawnTimeParser, 'RespawnTime', lines, expected)

    def test_chiefs_parser(self):
        lines = [
            "0_Chief Armor.1-BT7 2",
            "1_Chief Vehicles.GAZ67 1",
            "2_Chief Trains.USSR_FuelTrain/AA 1",
            "3_Chief Ships.G5 1 60 3 2.0",
        ]
        expected = {
            'chiefs': [
                {
                    'id': "0_Chief",
                    'code': "1-BT7",
                    'type': UnitTypes.armor,
                    'belligerent': Belligerents.blue,
                },
                {
                    'id': "1_Chief",
                    'code': "GAZ67",
                    'type': UnitTypes.vehicle,
                    'belligerent': Belligerents.red,
                },
                {
                    'id': "2_Chief",
                    'code': "USSR_FuelTrain/AA",
                    'type': UnitTypes.train,
                    'belligerent': Belligerents.red,
                },
                {
                    'id': "3_Chief",
                    'code': "G5",
                    'type': UnitTypes.ship,
                    'belligerent': Belligerents.red,
                    'waiting_time': 60,
                    'skill': Skills.ace,
                    'recharge_time': 2.0,
                },
            ],
        }
        self._test_parser(ChiefsParser, 'Chiefs', lines, expected)

    def test_stationary_parser(self):
        """
        Test ``NStationary`` section parser.
        """
        lines = [
            "0_Static vehicles.aeronautics.Aeronautics$BarrageBalloon_2400m 1 151781.85 89055.58 360.00 0.0",
            "1_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1",
            "2_Static vehicles.lights.Searchlight$SL_ManualBlue 1 151740.45 88673.74 360.00 0.0",
            "3_Static vehicles.planes.Plane$I_16TYPE24 2 134146.89 88005.43 336.92 0.0 de 2 1.0 I-16type24_G1_RoW3.bmp 1",
            "4_Static vehicles.radios.Beacon$RadioBeacon 2 151679.84 88805.39 360.00 0.0",
            "5_Static vehicles.stationary.Campfire$CampfireAirfield 0 151428.38 88817.52 360.00 0.0",
            "6_Static vehicles.stationary.Smoke$Smoke20 0 151404.61 89009.57 360.00 0.00",
            "7_Static vehicles.stationary.Siren$SirenCity 1 151984.28 88577.12 360.00 0.0",
            "8_Static vehicles.stationary.Stationary$Wagon1 1 152292.72 89662.80 360.00 0.0",
            "9_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4",
        ]
        expected = {
            'stationary': [
                {
                    'belligerent': Belligerents.red,
                    'id': '0_Static',
                    'code': 'BarrageBalloon_2400m',
                    'pos': {
                        'x': 151781.85,
                        'y': 89055.58,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.balloon,
                },
                {
                    'belligerent': Belligerents.blue,
                    'id': '1_Static',
                    'code': 'SdKfz251',
                    'use_spotter': True,
                    'pos': {
                        'x': 31333.62,
                        'y': 90757.91,
                    },
                    'rotation_angle': 600.29,
                    'range': 0,
                    'skill': Skills.average,
                    'type': UnitTypes.artillery,
                    'awakening_time': 0.0,
                },
                {
                    'belligerent': Belligerents.red,
                    'id': '2_Static',
                    'code': 'SL_ManualBlue',
                    'pos': {
                        'x': 151740.45,
                        'y': 88673.74,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.light,
                },
                {
                    'air_force': AirForces.luftwaffe,
                    'allows_spawning': True,
                    'belligerent': Belligerents.blue,
                    'id': '3_Static',
                    'code': 'I_16TYPE24',
                    'show_markings': True,
                    'pos': {
                        'x': 134146.89,
                        'y': 88005.43,
                    },
                    'rotation_angle': 336.92,
                    'restorable': True,
                    'skin': 'I-16type24_G1_RoW3.bmp',
                    'type': UnitTypes.airplane,
                },
                {
                    'belligerent': Belligerents.blue,
                    'id': '4_Static',
                    'code': 'RadioBeacon',
                    'pos': {
                        'x': 151679.84,
                        'y': 88805.39,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.radio,
                },
                {
                    'belligerent': Belligerents.none,
                    'id': '5_Static',
                    'code': 'CampfireAirfield',
                    'pos': {
                        'x': 151428.38,
                        'y': 88817.52,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.stationary,
                },
                {
                    'belligerent': Belligerents.none,
                    'id': '6_Static',
                    'code': 'Smoke20',
                    'pos': {
                        'x': 151404.61,
                        'y': 89009.57,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.stationary,
                },
                {
                    'belligerent': Belligerents.red,
                    'id': '7_Static',
                    'code': 'SirenCity',
                    'pos': {
                        'x': 151984.28,
                        'y': 88577.12,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.stationary,
                },
                {
                    'belligerent': Belligerents.red,
                    'id': '8_Static',
                    'code': 'Wagon1',
                    'pos': {
                        'x': 152292.72,
                        'y': 89662.80,
                    },
                    'rotation_angle': 360.00,
                    'type': UnitTypes.stationary,
                },
                {
                    'belligerent': Belligerents.red,
                    'id': '9_Static',
                    'code': 'G5',
                    'recharge_time': 1.4,
                    'pos': {
                        'x': 83759.05,
                        'y': 115021.15,
                    },
                    'rotation_angle': 360.00,
                    'skill': Skills.ace,
                    'type': UnitTypes.ship,
                    'awakening_time': 60.0,
                },
            ],
        }
        self._test_parser(NStationaryParser, 'NStationary', lines, expected)

    def test_buildings_parser(self):
        """
        Test ``Buildings`` section parser.
        """
        lines = [
            "0_bld House$Tent_Pyramid_US 1 43471.34 57962.08 630.00",
        ]
        expected = {
            'buildings': [
                {
                    'belligerent': Belligerents.red,
                    'id': '0_bld',
                    'code': 'Tent_Pyramid_US',
                    'pos': {
                        'y': 57962.08,
                        'x': 43471.34,
                    },
                    'rotation_angle': 630.00,
                },
            ],
        }
        self._test_parser(BuildingsParser, 'Buildings', lines, expected)

    def test_born_place_parser(self):
        """
        Test ``BornPlace`` section parser.
        """
        lines = [
            "1 3000 121601 74883 1 1000 200 0 0 0 5000 50 0 1 1 0 0 3.8 1 0 0 0 0",
        ]
        expected = {
            'homebases': [
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
                        'has_parachutes': True,
                        'max_pilots': 0,
                        'aircraft_limits': {
                            'enabled': True,
                            'consider_lost': True,
                            'consider_stationary': True,
                        },
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
                    },
                    'radar': {
                        'range': 50,
                        'min_height': 0,
                        'max_height': 5000,
                    },
                    'pos': {
                        'x': 121601.0,
                        'y': 74883.0,
                    },
                },
            ]
        }
        self._test_parser(BornPlaceParser, 'BornPlace', lines, expected)

    def test_static_camera_parser(self):
        """
        Test ``StaticCamera`` section parser.
        """
        lines = [
            "38426 65212 35 2",
        ]
        expected = {
            'cameras': [
                {
                    'belligerent': Belligerents.blue,
                    'pos': {
                        'x': 38426.0,
                        'y': 65212.0,
                        'z': 35.0,
                    },
                },
            ],
        }
        self._test_parser(StaticCameraParser, 'StaticCamera', lines, expected)

    def test_front_marker_parser(self):
        """
        Test ``FrontMarker`` section parser.
        """
        lines = [
            "FrontMarker0 7636.65 94683.02 1",
        ]
        expected = {
            'markers': [
                {
                    'belligerent': Belligerents.red,
                    'id': "FrontMarker0",
                    'pos': {
                        'x': 7636.65,
                        'y': 94683.02,
                    },
                },
            ],
        }
        self._test_parser(FrontMarkerParser, 'FrontMarker', lines, expected)

    def test_rocket_parser(self):
        lines = [
            "0_Rocket Fi103_V1_ramp 2 84141.38 114216.82 360.00 60.0 10 80.0 83433.91 115445.49",
            "1_Rocket Fi103_V1_ramp 2 84141.38 114216.82 360.00 60.0 10 80.0",
        ]
        expected = {
            'rockets': [
                {
                    'belligerent': Belligerents.blue,
                    'id': "0_Rocket",
                    'code': "Fi103_V1_ramp",
                    'pos': {
                        'x': 84141.38,
                        'y': 114216.82,
                    },
                    'rotation_angle': 360.00,
                    'waiting_time': 60.0,
                    'count': 10,
                    'period': 80.0,
                    'destination': {
                        'x': 83433.91,
                        'y': 115445.49,
                    },
                },
                {
                    'belligerent': Belligerents.blue,
                    'id': "1_Rocket",
                    'code': "Fi103_V1_ramp",
                    'pos': {
                        'x': 84141.38,
                        'y': 114216.82,
                    },
                    'rotation_angle': 360.00,
                    'waiting_time': 60.0,
                    'count': 10,
                    'period': 80.0,
                    'destination': None,
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

    def test_flight_route_parser(self):
        lines = [
            "TAKEOFF 193373.53 99288.17 0 0 &0",
            "TRIGGERS 0 10 20 0",
            "NORMFLY_401 98616.72 78629.31 500.00 300.00 &0 F2",
            "TRIGGERS 1 1 25 5 500",
            "NORMFLY 63028.34 42772.13 500.00 300.00 r0100 1 &0",
            "GATTACK 99737.30 79106.06 500.00 300.00 0_Chief 0 &0",
            "GATTACK 74338.61 29746.57 500.00 300.00 4_Static 0 &0",
            "GATTACK 82387.92 51163.75 500.00 300.00 0_Rocket 0 &0",
            "LANDING_104 185304.27 54570.12 0 0 &1",
        ]
        expected = {
            '3GvIAP01_route': [
                {
                    'type': RoutePointTypes.takeoff_normal,
                    'pos': {
                        'x': 193373.53,
                        'y': 99288.17,
                        'z': 0.0,
                    },
                    'speed': 0.0,
                    'formation': None,
                    'radio_silence': False,
                    'options': {
                        'delay': 10,
                        'spacing': 20,
                    }
                },
                {
                    'type': RoutePointTypes.patrol_triangle,
                    'pos': {
                        'x': 98616.72,
                        'y': 78629.31,
                        'z': 500.00,
                    },
                    'speed': 300.00,
                    'formation': Formations.echelon_right,
                    'radio_silence': False,
                    'options': {
                        'cycles': 1,
                        'timeout': 1,
                    },
                    'pattern': {
                        'angle': 25,
                        'side_size': 5,
                        'altitude_difference': 500,
                    },
                },
                {
                    'type': RoutePointTypes.air_attack,
                    'pos': {
                        'x': 63028.34,
                        'y': 42772.13,
                        'z': 500.00,
                    },
                    'speed': 300.00,
                    'formation': None,
                    'target': {
                        'id': "r0100",
                        'route_point': 1,
                    },
                    'radio_silence': False,
                },
                {
                    'type': RoutePointTypes.ground_attack,
                    'pos': {
                        'x': 99737.30,
                        'y': 79106.06,
                        'z': 500.00,
                    },
                    'speed': 300.00,
                    'target': {
                        'id': "0_Chief",
                        'route_point': 0,
                    },
                    'formation': None,
                    'radio_silence': False,
                },
                {
                    'type': RoutePointTypes.ground_attack,
                    'pos': {
                        'x': 74338.61,
                        'y': 29746.57,
                        'z': 500.00,
                    },
                    'speed': 300.00,
                    'target': {
                        'id': "4_Static",
                        'route_point': 0,
                    },
                    'formation': None,
                    'radio_silence': False,
                },
                {
                    'type': RoutePointTypes.ground_attack,
                    'pos': {
                        'x': 82387.92,
                        'y': 51163.75,
                        'z': 500.00,
                    },
                    'speed': 300.00,
                    'target': {
                        'id': "0_Rocket",
                        'route_point': 0,
                    },
                    'formation': None,
                    'radio_silence': False,
                },
                {
                    'type': RoutePointTypes.landing_straight,
                    'pos': {
                        'x': 185304.27,
                        'y': 54570.12,
                        'z': 0.00,
                    },
                    'speed': 0.00,
                    'formation': None,
                    'radio_silence': True,
                },
            ]
        }
        self._test_parser(FlightRouteParser, '3GvIAP01_Way', lines, expected)


class MDSScoutsParserTestCase(ParserTestCaseMixin, unittest.TestCase):
    """
    Test ``MDS_Scouts`` section parser.
    """
    def test_valid_data(self):
        lines = [
            "B-25H-1NA",
            "B-25J-1NA",
            "BeaufighterMk21",
        ]
        expected = {
            'scout_planes_red': [
                "B-25H-1NA",
                "B-25J-1NA",
                "BeaufighterMk21",
            ],
        }
        self._test_parser(MDSScoutsParser, 'MDS_Scouts_Red', lines, expected)

    def test_invalid_section_name(self):
        parser = MDSScoutsParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('MDS_Scouts_'))


class ChiefRoadParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        lines = [
            "21380.02 41700.34 120.00 10 2 3.055555582046509",
            "21500.00 41700.00 120.00",
            "50299.58 35699.85 120.00 0 3 2.6388890743255615",
            "60284.10 59142.93 120.00",
            "84682.13 98423.69 120.00",
        ]
        expected = {
            '0_chief_route': [
                {
                    'is_check_point': True,
                    'pos': {
                        'x': 21380.02,
                        'y': 41700.34,
                    },
                    'section_length': 2,
                    'speed': 3.055555582046509,
                    'waiting_time': 10,
                },
                {
                    'is_check_point': False,
                    'pos': {
                        'x': 21500.00,
                        'y': 41700.00,
                    },
                },
                {
                    'is_check_point': True,
                    'pos': {
                        'x': 50299.58,
                        'y': 35699.85,
                    },
                    'section_length': 3,
                    'speed': 2.6388890743255615,
                    'waiting_time': 0,
                },
                {
                    'is_check_point': False,
                    'pos': {
                        'x': 60284.10,
                        'y': 59142.93,
                    },
                },
                {
                    'is_check_point': False,
                    'pos': {
                        'x': 84682.13,
                        'y': 98423.69,
                    },
                },
            ],
        }
        self._test_parser(ChiefRoadParser, '0_Chief_Road', lines, expected)

    def test_invalid_section_name(self):
        parser = ChiefRoadParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('X_Chief_Road'))


class TargetsParserTestCase(ParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Target`` section parser.
    """

    def test_target_destroy(self):
        """
        Test ``destroy`` target type parser.
        """
        lines = [
            "0 0 0 0 500 90939 91871 0 1 10_Chief 91100 91500",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.destroy,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': False,
                    'waiting_time': 0,
                    'destruction_level': 50,
                    'pos': {
                        'x': 90939.0,
                        'y': 91871.0,
                    },
                    'object': {
                        'waypoint': 1,
                        'id': '10_Chief',
                        'pos': {
                            'x': 91100.0,
                            'y': 91500.0,
                        },
                    },
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_destroy_area(self):
        """
        Test 'destroy area' target type parser.
        """
        lines = [
            "1 1 1 60 750 133960 87552 1350",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.destroy_area,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'waiting_time': 60,
                    'destruction_level': 75,
                    'pos': {
                        'x': 133960.0,
                        'y': 87552.0,
                    },
                    'radius': 1350,
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_destroy_bridge(self):
        """
        Test 'destroy bridge' target type parser.
        """
        lines = [
            "2 2 1 30 500 135786 84596 0 0  Bridge84 135764 84636",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.destroy_bridge,
                    'priority': TargetPriorities.hidden,
                    'in_sleep_mode': True,
                    'waiting_time': 30,
                    'pos': {
                        'x': 135786.0,
                        'y': 84596.0,
                    },
                    'object': {
                        'id': 'Bridge84',
                        'pos': {
                            'x': 135764.0,
                            'y': 84636.0,
                        },
                    },
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_recon(self):
        """
        Test ``recon`` target type parser.
        """
        lines = [
            "3 1 1 50 500 133978 87574 1150",
            "3 0 1 40 501 134459 85239 300 0 1_Chief 134360 85346",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.recon,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'waiting_time': 50,
                    'requires_landing': False,
                    'pos': {
                        'x': 133978.0,
                        'y': 87574.0,
                    },
                    'radius': 1150,
                },
                {
                    'type': TargetTypes.recon,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': True,
                    'waiting_time': 40,
                    'requires_landing': True,
                    'pos': {
                        'x': 134459.0,
                        'y': 85239.0,
                    },
                    'radius': 300,
                    'object': {
                        'waypoint': 0,
                        'id': '1_Chief',
                        'pos': {
                            'x': 134360.0,
                            'y': 85346.0,
                        },
                    },
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_escort(self):
        """
        Test ``escort`` target type parser.
        """
        lines = [
            "4 0 1 10 750 134183 85468 0 1 r0100 133993 85287",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.escort,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': True,
                    'waiting_time': 10,
                    'destruction_level': 75,
                    'pos': {
                        'x': 134183.0,
                        'y': 85468.0,
                    },
                    'object': {
                        'waypoint': 1,
                        'id': 'r0100',
                        'pos': {
                            'x': 133993.0,
                            'y': 85287.0,
                        },
                    },
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_cover(self):
        """
        Test ``cover`` target type parser.
        """
        lines = [
            "5 1 1 20 250 132865 87291 0 1 1_Chief 132866 86905",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.cover,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'waiting_time': 20,
                    'destruction_level': 25,
                    'pos': {
                        'x': 132865.0,
                        'y': 87291.0,
                    },
                    'object': {
                        'waypoint': 1,
                        'id': '1_Chief',
                        'pos': {
                            'x': 132866.0,
                            'y': 86905.0,
                        },
                    },
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_cover_area(self):
        """
        Test 'cover area' target type parser.
        """
        lines = [
            "6 1 1 30 500 134064 88188 1350",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.cover_area,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'waiting_time': 30,
                    'destruction_level': 50,
                    'pos': {
                        'x': 134064.0,
                        'y': 88188.0,
                    },
                    'radius': 1350,
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)

    def test_target_cover_bridge(self):
        """
        Test 'cover bridge' target type parser.
        """
        lines = [
            "7 2 1 30 500 135896 84536 0 0  Bridge84 135764 84636",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.cover_bridge,
                    'priority': TargetPriorities.hidden,
                    'in_sleep_mode': True,
                    'waiting_time': 30,
                    'pos': {
                        'x': 135896.0,
                        'y': 84536.0,
                    },
                    'object': {
                        'id': 'Bridge84',
                        'pos': {
                            'x': 135764.0,
                            'y': 84636.0,
                        },
                    },
                },
            ],
        }
        self._test_parser(TargetParser, 'Target', lines, expected)


class BornPlaceAircraftsParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        """
        Test ``BornPlaceN`` section parser.
        """
        lines = [
            "Bf-109F-4 -1 1sc250 4sc50",
            "Bf-109G-6_Late 0",
            "Ju-88A-4 10 28xSC50 28xSC50_2xSC250 28xSC50_4xSC250",
            "+ 2xSC1800 2xSC2000",
        ]
        expected = {
            'homebase_aircrafts_1': [
                {
                    'code': 'Bf-109F-4',
                    'limit': None,
                    'weapon_limits': [
                        '1sc250',
                        '4sc50',
                    ],
                },
                {
                    'code': 'Bf-109G-6_Late',
                    'limit': 0,
                    'weapon_limits': [],
                },
                {
                    'code': 'Ju-88A-4',
                    'limit': 10,
                    'weapon_limits': [
                        '28xSC50',
                        '28xSC50_2xSC250',
                        '28xSC50_4xSC250',
                        '2xSC1800',
                        '2xSC2000',
                    ],
                },
            ],
        }
        self._test_parser(BornPlaceAircraftsParser, 'BornPlace1',
                          lines, expected)

    def test_invalid_section_name(self):
        parser = BornPlaceAircraftsParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('BornPlaceX'))


class BornPlaceAirForcesParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        """
        Test ``BornPlaceCountriesN`` section parser.
        """
        lines = [
            "de",
            "ru",
        ]
        expected = {
            'homebase_air_forces_1': [
                AirForces.luftwaffe,
                AirForces.vvs_rkka,
            ],
        }
        self._test_parser(BornPlaceAirForcesParser, 'BornPlaceCountries1',
                          lines, expected)

    def test_invalid_section_name(self):
        parser = BornPlaceAirForcesParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('BornPlaceCountriesX'))


class FlightInfoParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    def test_check_section_name(self):
        parser = FlightInfoParser()
        self.assertTrue(parser.check_section_name('r0100'))
        self.assertTrue(parser.check_section_name('3GvIAP00'))

    def test_multiple_aircrafts(self):
        lines = [
            "Planes 2",
            "Skill0 1",
            "Class air.A_20C",
            "Fuel 100",
            "weapons default",
            "Skill0 2",
            "Skill1 3",
            "Skill2 1",
            "Skill3 1",
            "skin0 Funky.bmp",
            "numberOn1 0",
            "spawn0 0_Static",
        ]
        expected = {
            '3GvIAP00_info': {
                'ai_only': False,
                'air_force': AirForces.vvs_rkka,
                'code': "A_20C",
                'count': 2,
                'flight': 1,
                'fuel': 100,
                'with_parachutes': True,
                'regiment': Regiments.get_by_code_name('3GvIAP'),
                'squadron': 1,
                'weapons': "default",
                'aircrafts': [
                    {
                        'id': 0,
                        'skill': Skills.veteran,
                        'aircraft_skin': "Funky.bmp",
                        'has_markings': True,
                        'spawn_object': '0_Static',
                    },
                    {
                        'id': 1,
                        'skill': Skills.ace,
                        'has_markings': False,
                    },
                ],
            },
        }
        self._test_parser(FlightInfoParser, '3GvIAP00', lines, expected)

    def test_single_aircraft(self):
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
            '3GvIAP01_info': {
                'ai_only': False,
                'air_force': AirForces.vvs_rkka,
                'code': "A_20C",
                'count': 1,
                'flight': 2,
                'fuel': 100,
                'with_parachutes': True,
                'regiment': Regiments.get_by_code_name('3GvIAP'),
                'squadron': 1,
                'weapons': "default",
                'aircrafts': [
                    {
                        'id': 0,
                        'skill': Skills.average,
                        'aircraft_skin': "Funky.bmp",
                        'has_markings': False,
                        'spawn_object': '0_Static',
                    },
                ],
            },
        }
        self._test_parser(FlightInfoParser, '3GvIAP01', lines, expected)

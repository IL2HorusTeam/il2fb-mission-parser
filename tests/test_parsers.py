# -*- coding: utf-8 -*-
"""
Functional tests for parsers.
"""

import datetime
import itertools
import tempfile
import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.organization import AirForces, Belligerents, Regiments
from il2fb.commons.targets import TargetTypes, TargetPriorities
from il2fb.commons.weather import Conditions, Gust, Turbulence

from il2fb.parsers.mission.constants import COMMENT_MARKERS
from il2fb.parsers.mission.exceptions import MissionParsingError
from il2fb.parsers.mission.parsers import (
    to_bool, to_belligerent, to_skill, to_unit_type, clean_line, SectionParser,
    MainParser, SeasonParser, RespawnTimeParser, WeatherParser, MDSParser,
    NStationaryParser, BuildingsParser, StaticCameraParser, TargetParser,
    FrontMarkerParser, BornPlaceParser, ChiefsParser, BornPlaceAircraftsParser,
    BornPlaceAirForcesParser, RocketParser, ChiefRoadParser, WingParser,
    MDSScoutsParser, FlightInfoParser, FlightRouteParser, FileParser,
)
from il2fb.parsers.mission.structures import (
    Point2D, Point3D, GroundRoutePoint, Building, StaticCamera, FrontMarker,
    Rocket, StationaryObject, StationaryArtillery, StationaryAircraft,
    StationaryShip, FlightRoutePoint, FlightRouteTakeoffPoint,
    FlightRoutePatrolPoint, FlightRouteAttackPoint,
)


class CommonsTestCase(unittest.TestCase):

    def test_to_bool(self):
        self.assertFalse(to_bool('0'))
        self.assertTrue(to_bool('1'))
        self.assertTrue(to_bool('-1'))

    def test_to_belligerent(self):
        self.assertEqual(to_belligerent('0'), Belligerents.none)
        self.assertEqual(to_belligerent('1'), Belligerents.red)
        self.assertEqual(to_belligerent('2'), Belligerents.blue)

    def test_to_skill(self):
        self.assertEqual(to_skill('3'), Skills.ace)

    def test_to_unit_type(self):
        self.assertEqual(to_unit_type('planes'), UnitTypes.aircraft)

    def test_clean_line(self):
        line = "  123   \n"
        self.assertEqual(clean_line(line), "123")

        line = "  {:} \n".format(''.join(COMMENT_MARKERS))
        self.assertEqual(clean_line(line), "")

        for marker in COMMENT_MARKERS:
            line = "  123 {:} 456 ".format(marker)
            self.assertEqual(clean_line(line), "123")

        for combination in itertools.permutations(COMMENT_MARKERS):
            line = "  123 {:} 456 ".format(''.join(combination))
            self.assertEqual(clean_line(line), "123")


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

    def test_clean(self):
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
        result = parser.stop()
        self.assertEqual(result, expected)


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
            'location_loader': 'Moscow/sload.ini',
            'time': {
                'value': datetime.time(11, 45),
                'is_fixed': True,
            },
            'weather_conditions': Conditions.good,
            'cloud_base': 1500,
            'player': {
                'belligerent': Belligerents.red,
                'flight_id': "fiLLv24fi00",
                'aircraft_index': 0,
                'fixed_weapons': True,
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
            'conditions': {
                'radar': {
                    'advanced_mode': True,
                    'refresh_interval': 0,
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
                        'max_range': 2,
                        'max_height': 1500,
                        'alpha': 5,
                    },
                },
                'scouting': {
                    'scouts_affect_radar': False,
                    'ships_affect_radar': False,
                    'only_scouts_complete_targets': False,
                },
                'home_bases': {
                    'hide_unpopulated': False,
                    'hide_players_count': False,
                    'hide_ai_aircrafts_after_landing': True,
                },
                'communication': {
                    'vectoring': True,
                    'tower_communication': True,
                    'ai_radio_silence': False,
                },
                'crater_visibility_muptipliers': {
                    'le_100kg': 1.0,
                    'le_1000kg': 1.0,
                    'gt_1000kg': 1.0,
                },
            }
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
            "4_Chief SomethingUnknown.XXX 1",
            "5_Chief Ships.Niobe 2",
        ]
        expected = {
            'moving_units': [
                {
                    'id': '0_Chief',
                    'code': '1-BT7',
                    'type': UnitTypes.armor,
                    'belligerent': Belligerents.blue,
                },
                {
                    'id': '1_Chief',
                    'code': 'GAZ67',
                    'type': UnitTypes.vehicle,
                    'belligerent': Belligerents.red,
                },
                {
                    'id': '2_Chief',
                    'code': 'USSR_FuelTrain/AA',
                    'type': UnitTypes.train,
                    'belligerent': Belligerents.red,
                },
                {
                    'id': '3_Chief',
                    'code': 'G5',
                    'type': UnitTypes.ship,
                    'belligerent': Belligerents.red,
                    'hibernation': 60,
                    'skill': Skills.ace,
                    'recharge_time': 2.0,
                },
                {
                    'id': '4_Chief',
                    'code': 'XXX',
                    'type': 'SomethingUnknown',
                    'belligerent': Belligerents.red,
                },
                {
                    'id': '5_Chief',
                    'code': 'Niobe',
                    'type': UnitTypes.ship,
                    'belligerent': Belligerents.blue,
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
            "57_Static vehicles.artillery.Artillery$Flak18_37mm 2 153849.64 163928.12 360.00 0.0 0",
            "58_Static vehicles.artillery.Artillery$Flak18_88mm 2 87591.03 115255.62 690.00 0.0",

            "2_Static vehicles.lights.Searchlight$SL_ManualBlue 1 151740.45 88673.74 360.00 0.0",

            "3_Static vehicles.planes.Plane$I_16TYPE24 1 134146.89 88005.43 336.92 0.0 null 2 1.0 I-16type24_G1_RoW3.bmp 1",
            "458_Static vehicles.planes.Plane$FW_190A4FR 2 33201.34 73105.78 265.00 0.0 de 1 1.0 null 0",
            "459_Static vehicles.planes.Plane$A_20C 0 30663.31 24632.09 360.00 0.0 nn 1 1.0 null 0",
            "19_Static vehicles.planes.Plane$JU_87D3 2 153811.08 164330.47 360.00 0.0 null 1",

            "4_Static vehicles.radios.Beacon$RadioBeacon 2 151679.84 88805.39 360.00 0.0",
            "5_Static vehicles.stationary.Campfire$CampfireAirfield 0 151428.38 88817.52 360.00 0.0",
            "6_Static vehicles.stationary.Smoke$Smoke20 0 151404.61 89009.57 360.00 0.00",
            "7_Static vehicles.stationary.Siren$SirenCity 1 151984.28 88577.12 360.00 0.0",
            "8_Static vehicles.stationary.Stationary$Wagon1 1 152292.72 89662.80 360.00 0.0",
            "9_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4",

            "10_Static FAKE.SomethingUnknown.FAKE$XXX 1 152292.72 89662.80 360.00 0.0",
        ]
        expected = {
            'stationary': [
                StationaryObject(
                    id='0_Static',
                    belligerent=Belligerents.red,
                    code='BarrageBalloon_2400m',
                    pos=Point2D(151781.85, 89055.58),
                    rotation_angle=360.00,
                    type=UnitTypes.balloon,
                ),
                StationaryArtillery(
                    id='1_Static',
                    belligerent=Belligerents.blue,
                    code='SdKfz251',
                    pos=Point2D(31333.62, 90757.91),
                    rotation_angle=600.29,
                    type=UnitTypes.artillery,
                    awakening_time=0.0,
                    range=0,
                    skill=Skills.average,
                    use_spotter=True,
                ),
                StationaryArtillery(
                    id='57_Static',
                    belligerent=Belligerents.blue,
                    code='Flak18_37mm',
                    pos=Point2D(153849.64, 163928.12),
                    rotation_angle=360.0,
                    type=UnitTypes.artillery,
                    awakening_time=0.0,
                    range=0,
                    skill=None,
                    use_spotter=False,
                ),
                StationaryArtillery(
                    id='58_Static',
                    belligerent=Belligerents.blue,
                    code='Flak18_88mm',
                    pos=Point2D(87591.03, 115255.62),
                    rotation_angle=690.00,
                    type=UnitTypes.artillery,
                    awakening_time=0.0,
                    range=0,
                    skill=None,
                    use_spotter=False,
                ),
                StationaryObject(
                    id='2_Static',
                    code='SL_ManualBlue',
                    belligerent=Belligerents.red,
                    pos=Point2D(151740.45, 88673.74),
                    rotation_angle=360.00,
                    type=UnitTypes.light,
                ),
                StationaryAircraft(
                    id='3_Static',
                    code='I_16TYPE24',
                    belligerent=Belligerents.red,
                    pos=Point2D(134146.89, 88005.43),
                    rotation_angle=336.92,
                    type=UnitTypes.aircraft,
                    air_force=AirForces.vvs_rkka,
                    allows_spawning=True,
                    show_markings=True,
                    is_restorable=True,
                    skin="I-16type24_G1_RoW3.bmp",
                ),
                StationaryAircraft(
                    air_force=AirForces.luftwaffe,
                    allows_spawning=True,
                    belligerent=Belligerents.blue,
                    id='458_Static',
                    code='FW_190A4FR',
                    show_markings=False,
                    pos=Point2D(33201.34, 73105.78),
                    rotation_angle=265.0,
                    is_restorable=False,
                    skin=None,
                    type=UnitTypes.aircraft,
                ),
                StationaryAircraft(
                    air_force=AirForces.none,
                    allows_spawning=True,
                    belligerent=Belligerents.none,
                    id='459_Static',
                    code='A_20C',
                    show_markings=False,
                    pos=Point2D(30663.31, 24632.09),
                    rotation_angle=360.0,
                    is_restorable=False,
                    skin=None,
                    type=UnitTypes.aircraft,
                ),
                StationaryAircraft(
                    air_force=None,
                    allows_spawning=False,
                    belligerent=Belligerents.blue,
                    id='19_Static',
                    code='JU_87D3',
                    show_markings=True,
                    pos=Point2D(153811.08, 164330.47),
                    rotation_angle=360.0,
                    is_restorable=False,
                    skin=None,
                    type=UnitTypes.aircraft,
                ),
                StationaryObject(
                    belligerent=Belligerents.blue,
                    id='4_Static',
                    code='RadioBeacon',
                    pos=Point2D(151679.84, 88805.39),
                    rotation_angle=360.00,
                    type=UnitTypes.radio,
                ),
                StationaryObject(
                    belligerent=Belligerents.none,
                    id='5_Static',
                    code='CampfireAirfield',
                    pos=Point2D(151428.38, 88817.52),
                    rotation_angle=360.00,
                    type=UnitTypes.stationary,
                ),
                StationaryObject(
                    belligerent=Belligerents.none,
                    id='6_Static',
                    code='Smoke20',
                    pos=Point2D(151404.61, 89009.57),
                    rotation_angle=360.00,
                    type=UnitTypes.stationary,
                ),
                StationaryObject(
                    belligerent=Belligerents.red,
                    id='7_Static',
                    code='SirenCity',
                    pos=Point2D(151984.28, 88577.12),
                    rotation_angle=360.00,
                    type=UnitTypes.stationary,
                ),
                StationaryObject(
                    belligerent=Belligerents.red,
                    id='8_Static',
                    code='Wagon1',
                    pos=Point2D(152292.72, 89662.80),
                    rotation_angle=360.00,
                    type=UnitTypes.stationary,
                ),
                StationaryShip(
                    belligerent=Belligerents.red,
                    id='9_Static',
                    code='G5',
                    recharge_time=1.4,
                    pos=Point2D(83759.05, 115021.15),
                    rotation_angle=360.00,
                    skill=Skills.ace,
                    type=UnitTypes.ship,
                    awakening_time=60.0,
                ),
                StationaryObject(
                    belligerent=Belligerents.red,
                    id='10_Static',
                    code='XXX',
                    pos=Point2D(152292.72, 89662.80),
                    rotation_angle=360.00,
                    type='SomethingUnknown',
                ),
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
                Building(
                    id='0_bld',
                    belligerent=Belligerents.red,
                    code='Tent_Pyramid_US',
                    pos=Point2D(43471.34, 57962.08),
                    rotation_angle=630.00,
                ),
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
                StaticCamera(
                    belligerent=Belligerents.blue,
                    pos=Point3D(38426.0, 65212.0, 35.0),
                ),
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
                FrontMarker(
                    id='FrontMarker0',
                    belligerent=Belligerents.red,
                    pos=Point2D(7636.65, 94683.02),
                ),
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
                Rocket(
                    id='0_Rocket',
                    code='Fi103_V1_ramp',
                    belligerent=Belligerents.blue,
                    pos=Point2D(84141.38, 114216.82),
                    rotation_angle=360.00,
                    delay=60.0,
                    count=10,
                    period=80.0,
                    destination=Point2D(83433.91, 115445.49),
                ),
                Rocket(
                    id='1_Rocket',
                    code='Fi103_V1_ramp',
                    belligerent=Belligerents.blue,
                    pos=Point2D(84141.38, 114216.82),
                    rotation_angle=360.00,
                    delay=60.0,
                    count=10,
                    period=80.0,
                    destination=None,
                ),
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

            "NORMFLY 102105.11 129548.84 250.00 300.00",
            "NORMFLY_401 98616.72 78629.31 500.00 300.00 &0 F2",
            "TRIGGERS 1 1 25 5 500",

            "NORMFLY 63028.34 42772.13 500.00 300.00 r0100 1 &0",
            "GATTACK 99737.30 79106.06 500.00 300.00 0_Chief 0 &0",
            "GATTACK 74338.61 29746.57 500.00 300.00 4_Static 0 &0",
            "GATTACK 82387.92 51163.75 500.00 300.00 0_Rocket 0 &0",
            "GATTACK 98720.93 108662.92 250.00 300.00 0_Chief 6",

            "LANDING_104 185304.27 54570.12 0 0 &1",
        ]
        expected = {
            'flight_route_3GvIAP01': [
                FlightRouteTakeoffPoint(
                    type=RoutePointTypes.takeoff_normal,
                    pos=Point3D(193373.53, 99288.17, 0.0),
                    speed=0.0,
                    formation=None,
                    radio_silence=False,
                    delay=10,
                    spacing=20,
                ),
                FlightRoutePoint(
                    type=RoutePointTypes.normal,
                    pos=Point3D(102105.11, 129548.84, 250.00),
                    speed=300.00,
                    radio_silence=False,
                    formation=None,
                ),
                FlightRoutePatrolPoint(
                    type=RoutePointTypes.patrol_triangle,
                    pos=Point3D(98616.72, 78629.31, 500.00),
                    speed=300.00,
                    formation=Formations.echelon_right,
                    radio_silence=False,
                    patrol_cycles=1,
                    patrol_timeout=1,
                    pattern_angle=25,
                    pattern_side_size=5,
                    pattern_altitude_difference=500,
                ),
                FlightRouteAttackPoint(
                    type=RoutePointTypes.air_attack,
                    pos=Point3D(63028.34, 42772.13, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='r0100',
                    target_route_point=1,
                ),
                FlightRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(99737.30, 79106.06, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='0_Chief',
                    target_route_point=0,
                ),
                FlightRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(74338.61, 29746.57, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='4_Static',
                    target_route_point=0,
                ),
                FlightRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(82387.92, 51163.75, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='0_Rocket',
                    target_route_point=0,
                ),
                FlightRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(98720.93, 108662.92, 250.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='0_Chief',
                    target_route_point=6,
                ),
                FlightRoutePoint(
                    type=RoutePointTypes.landing_straight,
                    pos=Point3D(185304.27, 54570.12, 0.00),
                    speed=0.00,
                    formation=None,
                    radio_silence=True,
                ),
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
            'scouts_red': {
                'belligerent': Belligerents.red,
                'aircrafts': [
                    "B-25H-1NA",
                    "B-25J-1NA",
                    "BeaufighterMk21",
                ],
            },
        }
        self._test_parser(MDSScoutsParser, 'MDS_Scouts_Red', lines, expected)

    def test_invalid_section_name(self):
        parser = MDSScoutsParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('MDS_Scouts_'))


class ChiefRoadParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        lines = [
            "21380.02 41700.34 120.00 10 3 3.055555582046509",
            "21500.00 41700.00 120.00",
            "50299.58 35699.85 120.00 0 3 2.6388890743255615",
            "60284.10 59142.93 120.00",
            "84682.13 98423.69 120.00",
        ]
        expected = {
            'route_0_Chief': [
                GroundRoutePoint(
                    pos=Point2D(21380.02, 41700.34),
                    is_checkpoint=True,
                    delay=10,
                    section_length=3,
                    speed=3.055555582046509,
                ),
                GroundRoutePoint(
                    pos=Point2D(21500.00, 41700.00),
                    is_checkpoint=False,
                ),
                GroundRoutePoint(
                    pos=Point2D(50299.58, 35699.85),
                    is_checkpoint=True,
                    delay=0,
                    section_length=3,
                    speed=2.6388890743255615,
                ),
                GroundRoutePoint(
                    pos=Point2D(60284.10, 59142.93),
                    is_checkpoint=False,
                ),
                GroundRoutePoint(
                    pos=Point2D(84682.13, 98423.69),
                    is_checkpoint=False,
                ),
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
                    'delay': 0,
                    'destruction_level': 50,
                    'pos': Point2D(90939.0, 91871.0),
                    'object': {
                        'waypoint': 1,
                        'id': '10_Chief',
                        'pos': Point2D(91100.0, 91500.0),
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
                    'delay': 60,
                    'destruction_level': 75,
                    'pos': Point2D(133960.0, 87552.0),
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
                    'delay': 30,
                    'pos': Point2D(135786.0, 84596.0),
                    'object': {
                        'id': 'Bridge84',
                        'pos': Point2D(135764.0, 84636.0),
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
                    'delay': 50,
                    'requires_landing': False,
                    'pos': Point2D(133978.0, 87574.0),
                    'radius': 1150,
                },
                {
                    'type': TargetTypes.recon,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': True,
                    'delay': 40,
                    'requires_landing': True,
                    'pos': Point2D(134459.0, 85239.0),
                    'radius': 300,
                    'object': {
                        'waypoint': 0,
                        'id': '1_Chief',
                        'pos': Point2D(134360.0, 85346.0),
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
                    'delay': 10,
                    'destruction_level': 75,
                    'pos': Point2D(134183.0, 85468.0),
                    'object': {
                        'waypoint': 1,
                        'id': 'r0100',
                        'pos': Point2D(133993.0, 85287.0),
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
                    'delay': 20,
                    'destruction_level': 25,
                    'pos': Point2D(132865.0, 87291.0),
                    'object': {
                        'waypoint': 1,
                        'id': '1_Chief',
                        'pos': Point2D(132866.0, 86905.0),
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
                    'delay': 30,
                    'destruction_level': 50,
                    'pos': Point2D(134064.0, 88188.0),
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
                    'delay': 30,
                    'pos': Point2D(135896.0, 84536.0),
                    'object': {
                        'id': 'Bridge84',
                        'pos': Point2D(135764.0, 84636.0),
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
            "nn",
        ]
        expected = {
            'home_base_air_forces_1': [
                AirForces.luftwaffe,
                AirForces.vvs_rkka,
                AirForces.none,
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
            '3GvIAP00': {
                'id': '3GvIAP00',
                'squadron_index': 0,
                'flight_index': 0,
                'air_force': AirForces.vvs_rkka,
                'regiment': Regiments.get_by_code_name('3GvIAP'),
                'code': "A_20C",
                'count': 2,
                'fuel': 100,
                'weapons': "default",
                'ai_only': False,
                'with_parachutes': True,
                'aircrafts': [
                    {
                        'index': 0,
                        'skill': Skills.veteran,
                        'aircraft_skin': "Funky.bmp",
                        'has_markings': True,
                        'spawn_object': '0_Static',
                    },
                    {
                        'index': 1,
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
            '3GvIAP01': {
                'id': '3GvIAP01',
                'squadron_index': 0,
                'flight_index': 1,
                'air_force': AirForces.vvs_rkka,
                'regiment': Regiments.get_by_code_name('3GvIAP'),
                'code': "A_20C",
                'count': 1,
                'fuel': 100,
                'weapons': "default",
                'with_parachutes': True,
                'ai_only': False,
                'aircrafts': [
                    {
                        'index': 0,
                        'skill': Skills.average,
                        'aircraft_skin': "Funky.bmp",
                        'has_markings': False,
                        'spawn_object': '0_Static',
                    },
                ],
            },
        }
        self._test_parser(FlightInfoParser, '3GvIAP01', lines, expected)

    def test_invalid_section_name(self):
        p = FlightInfoParser()
        self.assertFalse(p.check_section_name("Something unknown"))


class FileParserTestCase(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.parser = FileParser()

    def test_parse(self):
        mission = tempfile.NamedTemporaryFile()
        try:
            self.assertEqual(self.parser.parse([]), {})
            self.assertEqual(self.parser.parse(mission), {})
            self.assertEqual(self.parser.parse(mission.name), {})
        finally:
            mission.close()

    def test_parse_line_with_error(self):
        lines = [
            "[MAIN]",
            "  foo",
        ]
        with self.assertRaises(MissionParsingError) as cm:
            self.parser.parse_sequence(lines)
        self.assertEqual(
            cm.exception.args[0],
            "ValueError in line #1 (\"foo\"): need more than 1 value to unpack"
        )

    def test_parser_finalization_with_error(self):
        lines = [
            "[MAIN]",
            "  foo bar",
        ]
        with self.assertRaises(MissionParsingError) as cm:
            self.parser.parse_sequence(lines)
        self.assertEqual(
            cm.exception.args[0],
            "KeyError during finalization of \"MainParser\": \'CloudType\'"
        )

    def test_get_flight_info_parser(self):
        lines = [
            "[Wing]",
            "  r0100",
            "[r0100]",
            "  Planes 1",
            "  Skill 1",
            "  Class air.A_20C",
            "  Fuel 100",
            "  weapons default",
        ]
        result = self.parser.parse_sequence(lines)
        self.assertEquals(
            result,
            {
                'objects': {
                    'flights': [
                        {
                            'id': 'r0100',
                            'squadron_index': 0,
                            'flight_index': 0,
                            'air_force': AirForces.vvs_rkka,
                            'regiment': None,
                            'code': 'A_20C',
                            'fuel': 100,
                            'weapons': 'default',
                            'ai_only': False,
                            'with_parachutes': True,
                            'count': 1,
                            'aircrafts': [
                                {
                                    'index': 0,
                                    'skill': Skills.average,
                                    'has_markings': True
                                },
                            ],
                            'route': [],
                        }
                    ],
                },
            }
        )

    def test_unknown_section(self):
        lines = [
            "[SomethingUnknown]",
            "  XXX",
            "  YYY",
            "  ZZZ",
        ]
        result = self.parser.parse_sequence(lines)
        self.assertEquals(result, {})

    def test_get_conditions(self):
        lines = [
            "[MAIN]",
            "  MAP Moscow/sload.ini",
            "  TIME 11.75",
            "  TIMECONSTANT 1",
            "  WEAPONSCONSTANT 1",
            "  CloudType 1",
            "  CloudHeight 1500.0",
            "  player fiLLv24fi00",
            "  army 1",
            "  playerNum 0",
            "[SEASON]",
            "  Year 1942",
            "  Month 8",
            "  Day 25",
            "[WEATHER]",
            "  WindDirection 120.0",
            "  WindSpeed 3.0",
            "  Gust 0",
            "  Turbulence 4",
            "[MDS]",
            "  MDS_Radar_SetRadarToAdvanceMode 1",
            "  MDS_Radar_RefreshInterval 0",
            "  MDS_Radar_DisableVectoring 0",
            "  MDS_Radar_EnableTowerCommunications 1",
            "  MDS_Radar_ShipsAsRadar 0",
            "  MDS_Radar_ShipRadar_MaxRange 100",
            "  MDS_Radar_ShipRadar_MinHeight 100",
            "  MDS_Radar_ShipRadar_MaxHeight 5000",
            "  MDS_Radar_ShipSmallRadar_MaxRange 25",
            "  MDS_Radar_ShipSmallRadar_MinHeight 0",
            "  MDS_Radar_ShipSmallRadar_MaxHeight 2000",
            "  MDS_Radar_ScoutsAsRadar 0",
            "  MDS_Radar_ScoutRadar_MaxRange 2",
            "  MDS_Radar_ScoutRadar_DeltaHeight 1500",
            "  MDS_Radar_ScoutGroundObjects_Alpha 5",
            "  MDS_Radar_ScoutCompleteRecon 0",
            "  MDS_Misc_DisableAIRadioChatter 0",
            "  MDS_Misc_DespawnAIPlanesAfterLanding 1",
            "  MDS_Radar_HideUnpopulatedAirstripsFromMinimap 0",
            "  MDS_Misc_HidePlayersCountOnHomeBase 0",
            "  MDS_Misc_BombsCat1_CratersVisibilityMultiplier 1.0",
            "  MDS_Misc_BombsCat2_CratersVisibilityMultiplier 1.0",
            "  MDS_Misc_BombsCat3_CratersVisibilityMultiplier 1.0",
        ]
        result = self.parser.parse_sequence(lines)
        self.assertEqual(
            result,
            {
                'location_loader': 'Moscow/sload.ini',
                'player': {
                    'belligerent': Belligerents.red,
                    'flight_id': 'fiLLv24fi00',
                    'aircraft_index': 0,
                    'fixed_weapons': True,
                },
                'conditions': {
                    'time_info': {
                        'date': datetime.date(1942, 8, 25),
                        'time': datetime.time(11, 45),
                        'is_fixed': True,
                    },
                    'communication': {
                        'ai_radio_silence': False,
                        'tower_communication': True,
                        'vectoring': True,
                    },
                    'crater_visibility_muptipliers': {
                        'gt_1000kg': 1.0,
                        'le_1000kg': 1.0,
                        'le_100kg': 1.0,
                    },
                    'home_bases': {
                        'hide_ai_aircrafts_after_landing': True,
                        'hide_players_count': False,
                        'hide_unpopulated': False,
                    },
                    'meteorology': {
                        'cloud_base': 1500,
                        'gust': Gust.none,
                        'turbulence': Turbulence.very_strong,
                        'weather': Conditions.good,
                        'wind': {
                            'direction': 120.0,
                            'speed': 3.0,
                        },
                    },
                    'radar': {
                        'advanced_mode': True,
                        'refresh_interval': 0,
                        'scouts': {
                            'alpha': 5,
                            'max_height': 1500,
                            'max_range': 2,
                        },
                        'ships': {
                            'big': {
                                'max_height': 5000,
                                'max_range': 100,
                                'min_height': 100,
                            },
                            'small': {
                                'max_height': 2000,
                                'max_range': 25,
                                'min_height': 0,
                            },
                        },
                    },
                    'scouting': {
                        'only_scouts_complete_targets': False,
                        'scouts_affect_radar': False,
                        'ships_affect_radar': False,
                    },
                },
            }
        )

    def test_get_scouting(self):
        lines = [
            "[MDS]",
            "  MDS_Radar_SetRadarToAdvanceMode 1",
            "  MDS_Radar_RefreshInterval 0",
            "  MDS_Radar_DisableVectoring 0",
            "  MDS_Radar_EnableTowerCommunications 1",
            "  MDS_Radar_ShipsAsRadar 0",
            "  MDS_Radar_ShipRadar_MaxRange 100",
            "  MDS_Radar_ShipRadar_MinHeight 100",
            "  MDS_Radar_ShipRadar_MaxHeight 5000",
            "  MDS_Radar_ShipSmallRadar_MaxRange 25",
            "  MDS_Radar_ShipSmallRadar_MinHeight 0",
            "  MDS_Radar_ShipSmallRadar_MaxHeight 2000",
            "  MDS_Radar_ScoutsAsRadar 0",
            "  MDS_Radar_ScoutRadar_MaxRange 2",
            "  MDS_Radar_ScoutRadar_DeltaHeight 1500",
            "  MDS_Radar_ScoutGroundObjects_Alpha 5",
            "  MDS_Radar_ScoutCompleteRecon 0",
            "  MDS_Misc_DisableAIRadioChatter 0",
            "  MDS_Misc_DespawnAIPlanesAfterLanding 1",
            "  MDS_Radar_HideUnpopulatedAirstripsFromMinimap 0",
            "  MDS_Misc_HidePlayersCountOnHomeBase 0",
            "  MDS_Misc_BombsCat1_CratersVisibilityMultiplier 1.0",
            "  MDS_Misc_BombsCat2_CratersVisibilityMultiplier 1.0",
            "  MDS_Misc_BombsCat3_CratersVisibilityMultiplier 1.0",
            "[MDS_Scouts_Red]",
            "  B-25H-1NA",
            "  B-25J-1NA",
            "[MDS_Scouts_Blue]",
            "  Bf-109F-4",
            "  Ju-88A-4",
        ]
        result = self.parser.parse_sequence(lines)
        self.assertEqual(
            result['conditions']['scouting'],
            {
                'only_scouts_complete_targets': False,
                'scouts_affect_radar': False,
                'ships_affect_radar': False,
                'scouts': {
                    Belligerents.red: [
                        'B-25H-1NA',
                        'B-25J-1NA'
                    ],
                    Belligerents.blue: [
                        'Bf-109F-4',
                        'Ju-88A-4'
                    ],
                },
            }
        )

    def test_get_moving_units(self):
        lines = [
            "[Chiefs]",
            "  0_Chief Armor.1-BT7 2",
            "[0_Chief_Road]",
            "  21380.02 41700.34 120.00 10 3 3.055555582046509",
            "  21500.00 41700.00 120.00",
            "  50299.58 35699.85 120.00 0 3 2.6388890743255615",
            "  60284.10 59142.93 120.00",
            "  84682.13 98423.69 120.00",
        ]
        result = self.parser.parse_sequence(lines)
        self.assertEqual(
            result,
            {
                'objects': {
                    'moving_units': [
                        {
                            'id': '0_Chief',
                            'code': '1-BT7',
                            'type': UnitTypes.armor,
                            'belligerent': Belligerents.blue,
                            'route': [
                                GroundRoutePoint(
                                    pos=Point2D(21380.02, 41700.34),
                                    is_checkpoint=True,
                                    delay=10,
                                    section_length=3,
                                    speed=3.055555582046509,
                                ),
                                GroundRoutePoint(
                                    pos=Point2D(21500.00, 41700.00),
                                    is_checkpoint=False,
                                ),
                                GroundRoutePoint(
                                    pos=Point2D(50299.58, 35699.85),
                                    is_checkpoint=True,
                                    delay=0,
                                    section_length=3,
                                    speed=2.6388890743255615,
                                ),
                                GroundRoutePoint(
                                    pos=Point2D(60284.10, 59142.93),
                                    is_checkpoint=False,
                                ),
                                GroundRoutePoint(
                                    pos=Point2D(84682.13, 98423.69),
                                    is_checkpoint=False,
                                ),
                            ],
                        },
                    ],
                },
            }
        )

    def test_get_home_bases(self):
        lines = [
            "[BornPlace]",
            "  1 3000 121601 74883 1 1000 200 0 0 0 5000 50 0 1 1 0 0 3.8 1 0 0 0 0",
            "[BornPlace0]",
            "  Bf-109F-4 -1 1sc250 4sc50",
            "  Bf-109G-6_Late 0",
            "  Ju-88A-4 10 28xSC50 28xSC50_2xSC250 28xSC50_4xSC250",
            "  + 2xSC1800 2xSC2000",
            "[BornPlaceCountries0]",
            "  de",
            "  ru",
        ]
        result = self.parser.parse_sequence(lines)
        self.assertEqual(
            result,
            {
                'objects': {
                    'home_bases': [
                        {
                            'belligerent': Belligerents.red,
                            'pos': Point2D(121601.0, 74883.0),
                            'range': 3000,
                            'friction': {
                                'enabled': False,
                                'value': 3.8,
                            },
                            'radar': {
                                'max_height': 5000,
                                'min_height': 0,
                                'range': 50,
                            },
                            'show_default_icon': False,
                            'spawning': {
                                'enabled': True,
                                'in_air': {
                                    'conditions': {
                                        'always': False,
                                        'if_deck_is_full': False,
                                    },
                                    'heading': 0,
                                    'height': 1000,
                                    'speed': 200,
                                },
                                'in_stationary': {
                                    'enabled': False,
                                    'return_to_start_position': False,
                                },
                                'max_pilots': 0,
                                'with_parachutes': True,
                                'aircraft_limitations': {
                                    'allowed_aircrafts': [
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
                                            'weapon_limitations': []
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
                                            ]
                                        },
                                    ],
                                    'consider_lost': True,
                                    'consider_stationary': True,
                                    'enabled': True,
                                },
                                'allowed_air_forces': [
                                    AirForces.luftwaffe,
                                    AirForces.vvs_rkka,
                                ],
                            },
                        },
                    ],
                },
            }
        )

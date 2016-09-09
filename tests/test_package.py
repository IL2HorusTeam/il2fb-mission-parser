# -*- coding: utf-8 -*-

import datetime
import os
import tempfile
import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.organization import AirForces, Belligerents
from il2fb.commons.spatial import Point2D
from il2fb.commons.weather import Conditions, Gust, Turbulence

from il2fb.parsers.mission import MissionParser
from il2fb.parsers.mission.exceptions import MissionParsingError
from il2fb.parsers.mission.sections.chiefs import GroundRoutePoint

from .mixins import ParserTestCaseMixin


class MissionParserTestCase(ParserTestCaseMixin, unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.parser = MissionParser()

    def test_parse_empty_data(self):
        self.assertEqual(self.parser.parse([]), {})

    def test_parse_empty_file(self):
        mission = tempfile.NamedTemporaryFile()
        try:
            self.assertEqual(self.parser.parse(mission), {})
        finally:
            mission.close()

    def test_parse_empty_file_by_file_name(self):
        fd, path = tempfile.mkstemp()
        try:
            self.assertEqual(self.parser.parse(path), {})
        finally:
            os.close(fd)

    def test_parse_line_with_error(self):
        lines = [
            "[MAIN]",
            "  foo",
        ]
        self.assertRaisesWithMessage(
            MissionParsingError,
            "ValueError in line #1 (\"foo\"): need more than 1 value to unpack",
            self.parser.parse_stream, lines)

    def test_parser_finalization_with_error(self):
        lines = [
            "[MAIN]",
            "  foo bar",
        ]
        self.assertRaisesWithMessage(
            MissionParsingError,
            "KeyError during finalization of \"MainSectionParser\": \'CloudType\'",
            self.parser.parse_stream, lines)

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
        result = self.parser.parse_stream(lines)
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
        result = self.parser.parse_stream(lines)
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
            "  Turbulence 6",
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
        result = self.parser.parse_stream(lines)
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
        result = self.parser.parse_stream(lines)
        result = result['conditions']['scouting']

        self.assertEqual(result['only_scouts_complete_targets'], False)
        self.assertEqual(result['scouts_affect_radar'], False)
        self.assertEqual(result['ships_affect_radar'], False)

        self.assertEqual(result['scouts'], [
            {
                'belligerent': Belligerents.blue,
                'aircrafts': [
                    'Bf-109F-4',
                    'Ju-88A-4',
                ],
            },
            {
                'belligerent': Belligerents.red,
                'aircrafts': [
                    'B-25H-1NA',
                    'B-25J-1NA',
                ],
            },
        ])

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
        result = self.parser.parse_stream(lines)
        expected = {
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
        self.assertEqual(
            result['objects']['moving_units'][0]['route'][0],
            expected['objects']['moving_units'][0]['route'][0],
        )
        self.assertEqual(result, expected)

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
        result = self.parser.parse_stream(lines)
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

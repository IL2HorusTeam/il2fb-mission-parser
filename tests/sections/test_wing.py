# -*- coding: utf-8 -*-

import unittest

from il2fb.commons import Skills
from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.organization import AirForces, Regiments
from il2fb.commons.spatial import Point3D

from il2fb.parsers.mission.sections.wing import (
    WingSectionParser, WingInfoSectionParser, WingRouteSectionParser,
    WingRoutePoint, WingRouteTakeoffPoint, WingRouteAttackPoint,
    WingRoutePatrolPoint,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class WingSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Wing`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "1GvIAP12",
            "1GvIAP13",
        ]
        expected = {
            'wings': [
                "1GvIAP12",
                "1GvIAP13",
            ],
        }
        self.assertParser(WingSectionParser, 'Wing', lines, expected)


class WingInfoSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

    def test_check_section_name(self):
        parser = WingInfoSectionParser()
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
                'wing_index': 0,
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
        self.assertParser(WingInfoSectionParser, '3GvIAP00', lines, expected)

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
                'wing_index': 1,
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
        self.assertParser(WingInfoSectionParser, '3GvIAP01', lines, expected)

    def test_invalid_section_name(self):
        p = WingInfoSectionParser()
        self.assertFalse(p.check_section_name("Something unknown"))


class WingRoutePointTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            type=RoutePointTypes.landing_straight,
            pos=Point3D(185304.27, 54570.12, 0.00),
            speed=0.00,
            formation=None,
            radio_silence=True,
        )
        self.assertStructure(WingRoutePoint, **data)

        instance = WingRoutePoint(**data)
        self.assertEqual(
            repr(instance),
            "<WingRoutePoint '185304.27;54570.12;0.0'>")


class WingRouteTakeoffPointTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            type=RoutePointTypes.takeoff_normal,
            pos=Point3D(193373.53, 99288.17, 0.0),
            speed=0.0,
            formation=None,
            radio_silence=False,
            delay=10,
            spacing=20,
        )
        self.assertStructure(WingRouteTakeoffPoint, **data)

        instance = WingRouteTakeoffPoint(**data)
        self.assertEqual(
            repr(instance),
            "<WingRouteTakeoffPoint '193373.53;99288.17;0.0'>")


class WingRoutePatrolPointTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
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
        )
        self.assertStructure(WingRoutePatrolPoint, **data)

        instance = WingRoutePatrolPoint(**data)
        self.assertEqual(
            repr(instance),
            "<WingRoutePatrolPoint '98616.72;78629.31;500.0'>")


class WingRouteAttackPointTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            type=RoutePointTypes.air_attack,
            pos=Point3D(63028.34, 42772.13, 500.00),
            speed=300.00,
            formation=None,
            radio_silence=False,
            target_id='r0100',
            target_route_point=1,
        )
        self.assertStructure(WingRouteAttackPoint, **data)

        instance = WingRouteAttackPoint(**data)
        self.assertEqual(
            repr(instance),
            "<WingRouteAttackPoint '63028.34;42772.13;500.0'>")


class WingRouteSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

    def test_wing_route_parser(self):
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
            'wing_route_3GvIAP01': [
                WingRouteTakeoffPoint(
                    type=RoutePointTypes.takeoff_normal,
                    pos=Point3D(193373.53, 99288.17, 0.0),
                    speed=0.0,
                    formation=None,
                    radio_silence=False,
                    delay=10,
                    spacing=20,
                ),
                WingRoutePoint(
                    type=RoutePointTypes.normal,
                    pos=Point3D(102105.11, 129548.84, 250.00),
                    speed=300.00,
                    radio_silence=False,
                    formation=None,
                ),
                WingRoutePatrolPoint(
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
                WingRouteAttackPoint(
                    type=RoutePointTypes.air_attack,
                    pos=Point3D(63028.34, 42772.13, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='r0100',
                    target_route_point=1,
                ),
                WingRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(99737.30, 79106.06, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='0_Chief',
                    target_route_point=0,
                ),
                WingRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(74338.61, 29746.57, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='4_Static',
                    target_route_point=0,
                ),
                WingRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(82387.92, 51163.75, 500.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='0_Rocket',
                    target_route_point=0,
                ),
                WingRouteAttackPoint(
                    type=RoutePointTypes.ground_attack,
                    pos=Point3D(98720.93, 108662.92, 250.00),
                    speed=300.00,
                    formation=None,
                    radio_silence=False,
                    target_id='0_Chief',
                    target_route_point=6,
                ),
                WingRoutePoint(
                    type=RoutePointTypes.landing_straight,
                    pos=Point3D(185304.27, 54570.12, 0.00),
                    speed=0.00,
                    formation=None,
                    radio_silence=True,
                ),
            ]
        }
        self.assertParser(WingRouteSectionParser, '3GvIAP01_Way', lines, expected)

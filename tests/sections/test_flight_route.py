# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.spatial import Point3D

from il2fb.parsers.mission.sections.flight_route import (
    FlightRouteSectionParser, FlightRoutePoint, FlightRouteTakeoffPoint,
    FlightRouteAttackPoint, FlightRoutePatrolPoint,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class FlightRoutePointTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            type=RoutePointTypes.landing_straight,
            pos=Point3D(185304.27, 54570.12, 0.00),
            speed=0.00,
            formation=None,
            radio_silence=True,
        )
        self.assertStructure(FlightRoutePoint, **data)

        instance = FlightRoutePoint(**data)
        self.assertEqual(
            repr(instance),
            "<FlightRoutePoint '185304.27;54570.12;0.0'>")


class FlightRouteTakeoffPointTestCase(StructureTestCaseMixin, unittest.TestCase):

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
        self.assertStructure(FlightRouteTakeoffPoint, **data)

        instance = FlightRouteTakeoffPoint(**data)
        self.assertEqual(
            repr(instance),
            "<FlightRouteTakeoffPoint '193373.53;99288.17;0.0'>")


class FlightRoutePatrolPointTestCase(StructureTestCaseMixin, unittest.TestCase):

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
        self.assertStructure(FlightRoutePatrolPoint, **data)

        instance = FlightRoutePatrolPoint(**data)
        self.assertEqual(
            repr(instance),
            "<FlightRoutePatrolPoint '98616.72;78629.31;500.0'>")


class FlightRouteAttackPointTestCase(StructureTestCaseMixin, unittest.TestCase):

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
        self.assertStructure(FlightRouteAttackPoint, **data)

        instance = FlightRouteAttackPoint(**data)
        self.assertEqual(
            repr(instance),
            "<FlightRouteAttackPoint '63028.34;42772.13;500.0'>")


class FlightRouteSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

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
        self.assertParser(FlightRouteSectionParser, '3GvIAP01_Way', lines, expected)

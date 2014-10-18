# -*- coding: utf-8 -*-

import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.flight import Formations, RoutePointTypes
from il2fb.commons.organization import AirForces, Belligerents

from il2fb.parsers.mission.structures import (
    Base, Point2D, Point3D, GroundRoutePoint, Building, StaticCamera,
    FrontMarker, Rocket, StationaryObject, StationaryArtillery,
    StationaryAircraft, StationaryShip, FlightRoutePoint,
    FlightRouteTakeoffPoint, FlightRoutePatrolPoint, FlightRouteAttackPoint,
)


class BaseTestCase(unittest.TestCase):

    class Foo(Base):
        __slots__ = ['a', 'b', 'c', ]

        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

    def test_creation(self):
        foo = BaseTestCase.Foo(1, 2, 3)
        self.assertEqual(foo.a, 1)
        self.assertEqual(foo.b, 2)
        self.assertEqual(foo.c, 3)

    def test_equals(self):
        foo = BaseTestCase.Foo(1, 2, 3)
        bar = BaseTestCase.Foo(1, 2, 3)

        self.assertNotEqual(id(foo), id(bar))
        self.assertEqual(foo, bar)

    def test_not_equals(self):
        self.assertNotEqual(
            BaseTestCase.Foo(1, 2, 3),
            BaseTestCase.Foo(4, 5, 6)
        )
        self.assertNotEqual(
            BaseTestCase.Foo(1, 2, 3),
            int(123),
        )

    def test_hash(self):
        foo = BaseTestCase.Foo(1, 2, 3)

        self.assertEqual(
            hash(foo),
            hash((1, 2, 3))
        )

        bar = BaseTestCase.Foo(1, 2, 3)
        d = {foo: 123}

        self.assertEqual(d[bar], 123)


class StructuresTestCase(unittest.TestCase):

    def _test_structure(self, structure_class, **kwargs):
        structure_a = structure_class(**kwargs)

        for key in kwargs.keys():
            self.assertEqual(
                getattr(structure_a, key),
                kwargs[key]
            )

        structure_b = structure_class(**kwargs)

        self.assertNotEqual(id(structure_a), id(structure_b))
        self.assertEqual(structure_a, structure_b)

    def test_point2d(self):
        data = dict(x=1, y=2)
        self._test_structure(Point2D, **data)
        self.assertEqual(
            repr(Point2D(**data)),
            "<Point2D '1.0;2.0'>"
        )

    def test_point3d(self):
        data = dict(x=1, y=2, z=3)
        self._test_structure(Point3D, **data)
        self.assertEqual(
            repr(Point3D(**data)),
            "<Point3D '1.0;2.0;3.0'>"
        )

    def test_ground_route_point(self):
        data = dict(
            pos=Point2D(21380.02, 41700.34),
            is_checkpoint=True,
            section_length=3,
            speed=3.055555582046509,
            delay=10
        )
        self._test_structure(GroundRoutePoint, **data)
        self.assertEqual(
            repr(GroundRoutePoint(**data)),
            "<GroundRoutePoint '21380.02;41700.34'>"
        )

    def test_building(self):
        data = dict(
            id='0_bld',
            belligerent=Belligerents.red,
            code='Tent_Pyramid_US',
            pos=Point2D(43471.34, 57962.08),
            rotation_angle=630.00
        )
        self._test_structure(Building, **data)
        self.assertEqual(
            repr(Building(**data)),
            "<Building '0_bld'>"
        )

    def test_static_camera(self):
        data = dict(
            belligerent=Belligerents.blue,
            pos=Point3D(38426.0, 65212.0, 35.0),
        )
        self._test_structure(StaticCamera, **data)
        self.assertEqual(
            repr(StaticCamera(**data)),
            "<StaticCamera '38426.0;65212.0;35.0'>"
        )

    def test_front_marker(self):
        data = dict(
            id='FrontMarker0',
            belligerent=Belligerents.red,
            pos=Point2D(7636.65, 94683.02),
        )
        self._test_structure(FrontMarker, **data)
        self.assertEqual(
            repr(FrontMarker(**data)),
            "<FrontMarker 'FrontMarker0'>"
        )

    def test_rocket(self):
        data = dict(
            id='0_Rocket',
            code='Fi103_V1_ramp',
            belligerent=Belligerents.blue,
            pos=Point2D(84141.38, 114216.82),
            rotation_angle=360.00,
            delay=60.0,
            count=10,
            period=80.0,
            destination=Point2D(83433.91, 115445.49),
        )
        self._test_structure(Rocket, **data)
        self.assertEqual(
            repr(Rocket(**data)),
            "<Rocket '0_Rocket'>"
        )

    def test_stationary_object(self):
        data = dict(
            belligerent=Belligerents.none,
            id='6_Static',
            code='Smoke20',
            pos=Point2D(151404.61, 89009.57),
            rotation_angle=360.00,
            type=UnitTypes.stationary,
        )
        self._test_structure(StationaryObject, **data)
        self.assertEqual(
            repr(StationaryObject(**data)),
            "<StationaryObject '6_Static'>"
        )

    def test_stationary_artillery(self):
        data = dict(
            id='1_Static',
            belligerent=Belligerents.blue,
            code='SdKfz251',
            pos=Point2D(31333.62, 90757.91),
            rotation_angle=600.29,
            type=UnitTypes.artillery,
            range=0,
            skill=Skills.average,
            use_spotter=True,
            awakening_time=0.0,
        )
        self._test_structure(StationaryArtillery, **data)
        self.assertEqual(
            repr(StationaryArtillery(**data)),
            "<StationaryObject '1_Static'>"
        )

    def test_stationary_aircraft(self):
        data = dict(
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
        )
        self._test_structure(StationaryAircraft, **data)
        self.assertEqual(
            repr(StationaryAircraft(**data)),
            "<StationaryObject '3_Static'>"
        )

    def test_stationary_ship(self):
        data = dict(
            belligerent=Belligerents.red,
            id='9_Static',
            code='G5',
            recharge_time=1.4,
            pos=Point2D(83759.05, 115021.15),
            rotation_angle=360.00,
            skill=Skills.ace,
            type=UnitTypes.ship,
            awakening_time=60.0,
        )
        self._test_structure(StationaryShip, **data)
        self.assertEqual(
            repr(StationaryShip(**data)),
            "<StationaryObject '9_Static'>"
        )

    def test_flight_route_point(self):
        data = dict(
            type=RoutePointTypes.landing_straight,
            pos=Point3D(185304.27, 54570.12, 0.00),
            speed=0.00,
            formation=None,
            radio_silence=True,
        )
        self._test_structure(FlightRoutePoint, **data)
        self.assertEqual(
            repr(FlightRoutePoint(**data)),
            "<FlightRoutePoint '185304.27;54570.12;0.0'>"
        )

    def test_flight_route_takeoff_point(self):
        data = dict(
            type=RoutePointTypes.takeoff_normal,
            pos=Point3D(193373.53, 99288.17, 0.0),
            speed=0.0,
            formation=None,
            radio_silence=False,
            delay=10,
            spacing=20,
        )
        self._test_structure(FlightRouteTakeoffPoint, **data)
        self.assertEqual(
            repr(FlightRouteTakeoffPoint(**data)),
            "<FlightRoutePoint '193373.53;99288.17;0.0'>"
        )

    def test_flight_route_patrol_point(self):
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
        self._test_structure(FlightRoutePatrolPoint, **data)
        self.assertEqual(
            repr(FlightRoutePatrolPoint(**data)),
            "<FlightRoutePoint '98616.72;78629.31;500.0'>"
        )

    def test_flight_route_attack_point(self):
        data = dict(
            type=RoutePointTypes.air_attack,
            pos=Point3D(63028.34, 42772.13, 500.00),
            speed=300.00,
            formation=None,
            radio_silence=False,
            target_id='r0100',
            target_route_point=1,
        )
        self._test_structure(FlightRouteAttackPoint, **data)
        self.assertEqual(
            repr(FlightRouteAttackPoint(**data)),
            "<FlightRoutePoint '63028.34;42772.13;500.0'>"
        )

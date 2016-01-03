# -*- coding: utf-8 -*-

import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.organization import Belligerents, AirForces
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.nstationary import (
    NStationaryParser, StationaryObject, StationaryArtillery,
    StationaryAircraft, StationaryShip,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class StationaryObjectTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            belligerent=Belligerents.none,
            id='6_Static',
            code='Smoke20',
            pos=Point2D(151404.61, 89009.57),
            rotation_angle=360.00,
            type=UnitTypes.stationary,
        )
        self.assertStructure(StationaryObject, **data)

        instance = StationaryObject(**data)
        self.assertEqual(repr(instance), "<StationaryObject '6_Static'>")


class StationaryArtilleryTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
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
        self.assertStructure(StationaryArtillery, **data)

        instance = StationaryArtillery(**data)
        self.assertEqual(repr(instance), "<StationaryArtillery '1_Static'>")


class StationaryAircraftTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
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
        self.assertStructure(StationaryAircraft, **data)

        instance = StationaryAircraft(**data)
        self.assertEqual(repr(instance), "<StationaryAircraft '3_Static'>")


class StationaryShipTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
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
        self.assertStructure(StationaryShip, **data)

        instance = StationaryShip(**data)
        self.assertEqual(repr(instance), "<StationaryShip '9_Static'>")


class NStationaryParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``NStationary`` section parser.
    """

    def test_valid_data(self):
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
        self.assertParser(NStationaryParser, 'NStationary', lines, expected)

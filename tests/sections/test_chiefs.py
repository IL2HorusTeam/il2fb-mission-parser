# -*- coding: utf-8 -*-

import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.chiefs import (
    ChiefsSectionParser, ChiefRoadSectionParser, GroundRoutePoint,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class ChiefsSectionParserTestCase(
    SectionParserTestCaseMixin, unittest.TestCase,
):
    """
    Test ``Chiefs`` section parser.

    """

    def test_valid_data(self):
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
        self.assertParser(ChiefsSectionParser, 'Chiefs', lines, expected)


class GroundRoutePointTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            pos=Point2D(21380.02, 41700.34),
            is_checkpoint=True,
            section_length=3,
            speed=3.055555582046509,
            delay=10,
        )
        self.assertStructure(GroundRoutePoint, **data)

        instance = GroundRoutePoint(**data)
        self.assertEqual(
            repr(instance),
            "<GroundRoutePoint '21380.02;41700.34'>",
        )


class ChiefRoadSectionParserTestCase(
    SectionParserTestCaseMixin,
    unittest.TestCase,
):

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
                    speed=11.0,
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
                    speed=9.5,
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
        self.assertParser(
            ChiefRoadSectionParser,
            '0_Chief_Road',
            lines,
            expected,
        )

    def test_invalid_section_name(self):
        parser = ChiefRoadSectionParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('X_Chief_Road'))

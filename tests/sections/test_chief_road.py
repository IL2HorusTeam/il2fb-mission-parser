# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.chief_road import (
    ChiefRoadParser, GroundRoutePoint,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


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
            "<GroundRoutePoint '21380.02;41700.34'>")


class ChiefRoadParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

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
        self.assertParser(ChiefRoadParser, '0_Chief_Road', lines, expected)

    def test_invalid_section_name(self):
        parser = ChiefRoadParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('X_Chief_Road'))

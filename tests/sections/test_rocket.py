# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.rocket import RocketParser, Rocket

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class RocketTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
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
        self.assertStructure(Rocket, **data)

        instance = Rocket(**data)
        self.assertEqual(repr(instance), "<Rocket '0_Rocket'>")


class RocketParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Rocket`` section parser.
    """

    def test_valid_data(self):
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
        self.assertParser(RocketParser, 'Rocket', lines, expected)

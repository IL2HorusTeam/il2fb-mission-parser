# coding: utf-8

import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.buildings import BuildingsSectionParser, Building

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class BuildingTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            id='0_bld',
            belligerent=Belligerents.red,
            code='Tent_Pyramid_US',
            pos=Point2D(43471.34, 57962.08),
            rotation_angle=630.00,
        )
        self.assertStructure(Building, **data)

        instance = Building(**data)
        self.assertEqual(repr(instance), "<Building '0_bld'>")


class BuildingsSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Buildings`` section parser.
    """

    def test_valid_data(self):
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
        self.assertParser(BuildingsSectionParser, 'Buildings', lines, expected)

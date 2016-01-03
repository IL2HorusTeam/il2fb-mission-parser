# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.mission.sections.front_marker import (
    FrontMarkerSectionParser, FrontMarker,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class FrontMarkerTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            id='FrontMarker0',
            belligerent=Belligerents.red,
            pos=Point2D(7636.65, 94683.02),
        )
        self.assertStructure(FrontMarker, **data)

        instance = FrontMarker(**data)
        self.assertEqual(repr(instance), "<FrontMarker 'FrontMarker0'>")


class FrontMarkerSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``FrontMarker`` section parser.
    """

    def test_valid_data(self):
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
        self.assertParser(FrontMarkerSectionParser, 'FrontMarker', lines, expected)

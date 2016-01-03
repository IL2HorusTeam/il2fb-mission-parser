# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point3D

from il2fb.parsers.mission.sections.static_camera import (
    StaticCameraSectionParser, StaticCamera,
)

from ..mixins import StructureTestCaseMixin
from .mixins import SectionParserTestCaseMixin


class StaticCameraTestCase(StructureTestCaseMixin, unittest.TestCase):

    def test_valid_data(self):
        data = dict(
            belligerent=Belligerents.blue,
            pos=Point3D(38426.0, 65212.0, 35.0),
        )
        self.assertStructure(StaticCamera, **data)

        instance = StaticCamera(**data)
        self.assertEqual(
            repr(instance),
            "<StaticCamera '38426.0;65212.0;35.0'>")


class StaticCameraSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``StaticCamera`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "38426 65212 35 2",
        ]
        expected = {
            'cameras': [
                StaticCamera(
                    belligerent=Belligerents.blue,
                    pos=Point3D(38426.0, 65212.0, 35.0),
                ),
            ],
        }
        self.assertParser(StaticCameraSectionParser, 'StaticCamera', lines, expected)

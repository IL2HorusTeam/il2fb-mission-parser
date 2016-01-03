# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import Belligerents

from il2fb.parsers.mission.sections.mds_scouts import MDSScoutsParser

from .mixins import SectionParserTestCaseMixin


class MDSScoutsParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``MDS_Scouts`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "B-25H-1NA",
            "B-25J-1NA",
            "BeaufighterMk21",
        ]
        expected = {
            'scouts_red': {
                'belligerent': Belligerents.red,
                'aircrafts': [
                    "B-25H-1NA",
                    "B-25J-1NA",
                    "BeaufighterMk21",
                ],
            },
        }
        self.assertParser(MDSScoutsParser, 'MDS_Scouts_Red', lines, expected)

    def test_invalid_section_name(self):
        parser = MDSScoutsParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('MDS_Scouts_'))

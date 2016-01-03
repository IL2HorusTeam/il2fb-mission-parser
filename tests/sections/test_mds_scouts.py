# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import Belligerents

from il2fb.parsers.mission.sections.mds_scouts import MDSScoutsSectionParser

from .mixins import SectionParserTestCaseMixin


class MDSScoutsSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
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
        self.assertParser(MDSScoutsSectionParser, 'MDS_Scouts_Red', lines, expected)

    def test_invalid_section_name(self):
        parser = MDSScoutsSectionParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('MDS_Scouts_'))

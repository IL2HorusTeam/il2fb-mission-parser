# -*- coding: utf-8 -*-

import unittest

from il2fb.parsers.mission.sections.wing import WingSectionParser

from .mixins import SectionParserTestCaseMixin


class WingSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Wing`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "1GvIAP12",
            "1GvIAP13",
        ]
        expected = {
            'flights': [
                "1GvIAP12",
                "1GvIAP13",
            ],
        }
        self.assertParser(WingSectionParser, 'Wing', lines, expected)

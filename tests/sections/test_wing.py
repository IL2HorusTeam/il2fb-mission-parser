# -*- coding: utf-8 -*-

import unittest

from il2fb.parsers.mission.sections.wing import WingParser

from .mixins import SectionParserTestCaseMixin


class WingParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
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
        self.assertParser(WingParser, 'Wing', lines, expected)

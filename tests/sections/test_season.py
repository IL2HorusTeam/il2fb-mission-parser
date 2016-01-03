# -*- coding: utf-8 -*-

import datetime
import unittest

from il2fb.parsers.mission.sections.season import SeasonParser

from .mixins import SectionParserTestCaseMixin


class SeasonParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``SEASON`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "Year 1942",
            "Month 8",
            "Day 25",
        ]
        expected = {
            'date': datetime.date(1942, 8, 25),
        }
        self.assertParser(SeasonParser, 'SEASON', lines, expected)

# coding: utf-8

import unittest

from il2fb.parsers.mission.sections.base import (
    SectionParser, ValuesParser, CollectingParser,
)

from .mixins import SectionParserTestCaseMixin


class SectionParserTestCase(unittest.TestCase):

    class Parser(SectionParser):

        def check_section_name(self, section_name):
            return True

        def init_parser(self, section_name):
            pass

        def parse_line(self, line):
            pass

    def setUp(self):
        self.parser = self.Parser()

    def test_clean(self):
        self.parser.start("foo")
        result = self.parser.stop()
        self.assertIsNone(result)

    def test_stop_with_failure(self):
        self.assertRaises(RuntimeError, self.parser.stop)


class ValuesParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

    class Parser(ValuesParser):

        def check_section_name(self, section_name):
            return True

    def test_values_parser(self):
        lines = [
            "one first",
            "two second",
            "skin0 $13.JG52_Bf 109E-4_white1.bmp",
        ]
        expected = {
            'one': "first",
            'two': "second",
            'skin0': "$13.JG52_Bf 109E-4_white1.bmp",
        }
        self.assertParser(self.Parser, None, lines, expected)


class CollectingParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

    class Parser(CollectingParser):

        def check_section_name(self, section_name):
            return True

    def test_values_parser(self):
        lines = [
            "one first",
            "two second",
        ]
        expected = [
            "one first",
            "two second",
        ]
        self.assertParser(self.Parser, None, lines, expected)

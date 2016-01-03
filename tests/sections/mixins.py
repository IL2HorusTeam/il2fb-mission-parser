# -*- coding: utf-8 -*-

from ..mixins import ParserTestCaseMixin


class SectionParserTestCaseMixin(ParserTestCaseMixin):

    maxDiff = None

    def assertParser(self, parser_class, section_name, lines, expected):
        parser = parser_class()
        self.assertTrue(parser.start(section_name))
        for line in lines:
            parser.parse_line(line)
        result = parser.stop()
        self.assertEqual(result, expected)

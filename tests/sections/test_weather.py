# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.weather import Gust, Turbulence

from il2fb.parsers.mission.sections.weather import WeatherSectionParser

from .mixins import SectionParserTestCaseMixin


class WeatherSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``WEATHER`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "WindDirection 120.0",
            "WindSpeed 3.0",
            "Gust 0",
            "Turbulence 4",
        ]
        expected = {
            'weather': {
                'wind': {
                    'direction': 120.0,
                    'speed': 3.0,
                },
                'gust': Gust.none,
                'turbulence': Turbulence.very_strong,
            },
        }
        self.assertParser(WeatherSectionParser, 'WEATHER', lines, expected)

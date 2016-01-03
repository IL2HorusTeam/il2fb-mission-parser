# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.organization import AirForces

from il2fb.parsers.mission.sections.born_place_air_forces import BornPlaceAirForcesSectionParser

from .mixins import SectionParserTestCaseMixin


class BornPlaceAirForcesSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``BornPlaceCountriesN`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "de",
            "ru",
            "nn",
        ]
        expected = {
            'home_base_air_forces_1': [
                AirForces.luftwaffe,
                AirForces.vvs_rkka,
                AirForces.none,
            ],
        }
        self.assertParser(BornPlaceAirForcesSectionParser, 'BornPlaceCountries1',
                          lines, expected)

    def test_invalid_section_name(self):
        parser = BornPlaceAirForcesSectionParser()
        self.assertFalse(parser.start('foo section'))
        self.assertFalse(parser.start('BornPlaceCountriesX'))

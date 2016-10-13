# coding: utf-8

import datetime
import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.weather import Conditions

from il2fb.parsers.mission.sections.main import MainSectionParser

from .mixins import SectionParserTestCaseMixin


class MainSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``MAIN`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "MAP Moscow/sload.ini",
            "TIME 11.75",
            "TIMECONSTANT 1",
            "WEAPONSCONSTANT 1",
            "CloudType 1",
            "CloudHeight 1500.0",
            "player fiLLv24fi00",
            "army 1",
            "playerNum 0",
        ]
        expected = {
            'location_loader': 'Moscow/sload.ini',
            'time': {
                'value': datetime.time(11, 45),
                'is_fixed': True,
            },
            'weather_conditions': Conditions.good,
            'cloud_base': 1500,
            'player': {
                'belligerent': Belligerents.red,
                'flight_id': "fiLLv24fi00",
                'aircraft_index': 0,
                'fixed_weapons': True,
            },
        }
        self.assertParser(MainSectionParser, 'MAIN', lines, expected)

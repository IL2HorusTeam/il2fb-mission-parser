# -*- coding: utf-8 -*-

import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.organization import Belligerents

from il2fb.parsers.mission.sections.chiefs import ChiefsParser

from .mixins import SectionParserTestCaseMixin


class ChiefsParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Chiefs`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "0_Chief Armor.1-BT7 2",
            "1_Chief Vehicles.GAZ67 1",
            "2_Chief Trains.USSR_FuelTrain/AA 1",
            "3_Chief Ships.G5 1 60 3 2.0",
            "4_Chief SomethingUnknown.XXX 1",
            "5_Chief Ships.Niobe 2",
        ]
        expected = {
            'moving_units': [
                {
                    'id': '0_Chief',
                    'code': '1-BT7',
                    'type': UnitTypes.armor,
                    'belligerent': Belligerents.blue,
                },
                {
                    'id': '1_Chief',
                    'code': 'GAZ67',
                    'type': UnitTypes.vehicle,
                    'belligerent': Belligerents.red,
                },
                {
                    'id': '2_Chief',
                    'code': 'USSR_FuelTrain/AA',
                    'type': UnitTypes.train,
                    'belligerent': Belligerents.red,
                },
                {
                    'id': '3_Chief',
                    'code': 'G5',
                    'type': UnitTypes.ship,
                    'belligerent': Belligerents.red,
                    'hibernation': 60,
                    'skill': Skills.ace,
                    'recharge_time': 2.0,
                },
                {
                    'id': '4_Chief',
                    'code': 'XXX',
                    'type': 'SomethingUnknown',
                    'belligerent': Belligerents.red,
                },
                {
                    'id': '5_Chief',
                    'code': 'Niobe',
                    'type': UnitTypes.ship,
                    'belligerent': Belligerents.blue,
                },
            ],
        }
        self.assertParser(ChiefsParser, 'Chiefs', lines, expected)

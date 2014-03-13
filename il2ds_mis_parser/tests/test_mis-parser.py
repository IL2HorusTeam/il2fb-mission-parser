# -*- coding: utf-8 -*-
"""
 Testing the application il2ds-mis-parser
"""
import unittest
import os

from il2ds_mis_parser import parser_mis
from il2ds_mis_parser.constants import *


class TestParser(unittest.TestCase):

    def test_parser(self):
        """
        The test parse a section MAIN with parameters
        """

        example_settings = {
            'MAIN': {
                'MAP': 'Moscow/sload.ini',
                'army': '1',
                'playerNum': '0',
                'CloudHeight': '1500.0',
                'CloudType': '1',
                'TIME': '11.75'
            }
        }

        mis_file = os.path.join(os.path.dirname(__file__), 'missions', 'T_1942_Vyazma.mis')
        settings = parser_mis(mis_file, MAIN)
        self.assertEqual(example_settings, settings)
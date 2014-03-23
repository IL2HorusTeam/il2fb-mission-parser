# -*- coding: utf-8 -*-
"""
 Testing the application il2ds-mis-parser
"""
import unittest
import os
from datetime import date

from il2ds_mis_parser import RootParser


class TestParserMis(unittest.TestCase):

    parser = RootParser()
    file_path = os.path.join(os.path.dirname(__file__), 'missions', 'TEST.mis')

    def test_parser_main(self):
        """
        The test parse a section MAIN with parameters
        """
        example = {
            'MAP': 'Moscow/sload.ini',
            'army': '1',
            'playerNum': '0',
            'CloudHeight': '1500.0',
            'CloudType': '1',
            'TIME': '11.75'
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings['MAIN'])

    def test_parser_season(self):
        """
        The test parse a section SEASON with parameters
        """
        example = {
            'Day': 25,
            'Month': 8,
            'Year': 1942
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings['SEASON'])

    def test_parser_mds(self):
        """
        The test parse a section MDS with parameters Misc
        """
        example = {
        'HidePlayersCountOnHomeBase': '0',
        'DespawnAIPlanesAfterLanding': '1',
        'DisableAIRadioChatter': '1',
        'BombsCat3_CratersVisibilityMultiplier': '1.0',
        'BombsCat2_CratersVisibilityMultiplier': '1.0',
        'BombsCat1_CratersVisibilityMultiplier': '1.0'
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings['MDS']['Misc'])

    def test_parser_chiefs(self):
        """
        The test parse a section Chiefs with parameters
        """
        example = {
            '0_Chief': {
                'code': 'US_Supply_Cpy',
                'type': 'Vehicles',
                'army': 1
            },
            '10_Chief': {
                'code': 'PzKp_PIVF2',
                'type': 'Armor',
                'army': 2
            },
            '6_Chief': {
                'code': 'Germany_CargoTrain/AA',
                'type': 'Trains',
                'army': 2
            }
        }

        settings = self.parser.parser(self.file_path)
        #self.assertEqual(example, settings['Chiefs'])
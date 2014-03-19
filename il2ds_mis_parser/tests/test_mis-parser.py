# -*- coding: utf-8 -*-
"""
 Testing the application il2ds-mis-parser
"""
import unittest
import os

from il2ds_mis_parser.constants import *
from il2ds_mis_parser import ParserRoot


class TestParserMis(unittest.TestCase):

    parser = ParserRoot()
    file_path = os.path.join(os.path.dirname(__file__), 'missions', 'TEST.mis')

    def test_parser_main(self):
        """
        The test parse a section MAIN with parameters
        """
        example = {
            'MAP': 'Moscow/sload.ini',
            'army': 1,
            'playerNum': 0,
            'CloudHeight': 1500.0,
            'CloudType': 1,
            'TIME': 11.75
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings[MAIN])

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
        self.assertEqual(example, settings[SEASON])

    def test_parser_mds(self):
        """
        The test parse a section MDS with parameters Misc
        """
        example = {
        'HidePlayersCountOnHomeBase': 0,
        'DespawnAIPlanesAfterLanding': 1,
        'DisableAIRadioChatter': 1,
        'BombsCat3_CratersVisibilityMultiplier': 1.0,
        'BombsCat2_CratersVisibilityMultiplier': 1.0,
        'BombsCat1_CratersVisibilityMultiplier': 1.0
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings[MDS]['Misc'])

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
        self.assertEqual(example, settings[CHIEFS])

    def test_parser_buildings(self):
        """
        The test parse a section Buildings with parameters
        """
        example = {
            '0_bld': {
                'pos_x': 43471.34,
                'code': 'Tent_Pyramid_US',
                'army': 1,
                'height': 630.00,
                'pos_y': 57962.08,
                'type': 'House'
            },
            '1_bld': {
                'pos_x': 43506.53,
                'code': 'FurnitureTreeBroad1',
                'army': 1,
                'height': 690.00,
                'pos_y': 57926.16,
                'type': 'House'
            }
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings[BUILDINGS])

    def test_parser_target(self):
        """
        The test parse a section Target with parameters
        """
        example = {
            'FrontMarker1': {
                'pos_x': 24063.11,
                'pos_y': 92544.04,
                'army': 2
            },
            'FrontMarker0': {
                'pos_x': 7636.65,
                'pos_y': 94683.02,
                'army': 1
            }
        }

        settings = self.parser.parser(self.file_path)
        #self.assertEqual(example, settings[TARGET])
        print settings[TARGET]

    def test_parser_front_marker(self):
        """
        The test parse a section FrontMarker with parameters
        """
        example = {
            'FrontMarker1': {
                'pos_x': 24063.11,
                'pos_y': 92544.04,
                'army': 2
            },
            'FrontMarker0': {
                'pos_x': 7636.65,
                'pos_y': 94683.02,
                'army': 1
            }
        }

        settings = self.parser.parser(self.file_path)
        self.assertEqual(example, settings[FRONT_MARKER])
# -*- coding: utf-8 -*-

import unittest

from il2fb.parsers.mission.sections.mds import MDSParser

from .mixins import SectionParserTestCaseMixin


class MDSParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``MDS`` section parser.
    """

    def test_valid_data(self):
        lines = [
            "MDS_Radar_SetRadarToAdvanceMode 1",
            "MDS_Radar_RefreshInterval 0",
            "MDS_Radar_DisableVectoring 0",
            "MDS_Radar_EnableTowerCommunications 1",
            "MDS_Radar_ShipsAsRadar 0",
            "MDS_Radar_ShipRadar_MaxRange 100",
            "MDS_Radar_ShipRadar_MinHeight 100",
            "MDS_Radar_ShipRadar_MaxHeight 5000",
            "MDS_Radar_ShipSmallRadar_MaxRange 25",
            "MDS_Radar_ShipSmallRadar_MinHeight 0",
            "MDS_Radar_ShipSmallRadar_MaxHeight 2000",
            "MDS_Radar_ScoutsAsRadar 0",
            "MDS_Radar_ScoutRadar_MaxRange 2",
            "MDS_Radar_ScoutRadar_DeltaHeight 1500",
            "MDS_Radar_ScoutGroundObjects_Alpha 5",
            "MDS_Radar_ScoutCompleteRecon 0",
            "MDS_Misc_DisableAIRadioChatter 0",
            "MDS_Misc_DespawnAIPlanesAfterLanding 1",
            "MDS_Radar_HideUnpopulatedAirstripsFromMinimap 0",
            "MDS_Misc_HidePlayersCountOnHomeBase 0",
            "MDS_Misc_BombsCat1_CratersVisibilityMultiplier 1.0",
            "MDS_Misc_BombsCat2_CratersVisibilityMultiplier 1.0",
            "MDS_Misc_BombsCat3_CratersVisibilityMultiplier 1.0",
        ]
        expected = {
            'conditions': {
                'radar': {
                    'advanced_mode': True,
                    'refresh_interval': 0,
                    'ships': {
                        'big': {
                            'max_range': 100,
                            'min_height': 100,
                            'max_height': 5000,
                        },
                        'small': {
                            'max_range': 25,
                            'min_height': 0,
                            'max_height': 2000,
                        },
                    },
                    'scouts': {
                        'max_range': 2,
                        'max_height': 1500,
                        'alpha': 5,
                    },
                },
                'scouting': {
                    'scouts_affect_radar': False,
                    'ships_affect_radar': False,
                    'only_scouts_complete_targets': False,
                },
                'home_bases': {
                    'hide_unpopulated': False,
                    'hide_players_count': False,
                    'hide_ai_aircrafts_after_landing': True,
                },
                'communication': {
                    'vectoring': True,
                    'tower_communication': True,
                    'ai_radio_silence': False,
                },
                'crater_visibility_muptipliers': {
                    'le_100kg': 1.0,
                    'le_1000kg': 1.0,
                    'gt_1000kg': 1.0,
                },
            }
        }
        self.assertParser(MDSParser, 'MDS', lines, expected)

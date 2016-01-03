# -*- coding: utf-8 -*-

from ..converters import to_bool
from . import ValuesParser


class MDSSectionParser(ValuesParser):
    """
    Parses ``MDS`` section.
    View :ref:`detailed description <mds-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "MDS"

    def parse_line(self, line):
        super(MDSSectionParser, self).parse_line(line.replace('MDS_', ''))

    def clean(self):
        return {
            'conditions': {
                'radar': {
                    'advanced_mode': to_bool(self.data['Radar_SetRadarToAdvanceMode']),
                    'refresh_interval': int(self.data['Radar_RefreshInterval']),
                    'ships': {
                        'big': {
                            'max_range': int(self.data['Radar_ShipRadar_MaxRange']),
                            'min_height': int(self.data['Radar_ShipRadar_MinHeight']),
                            'max_height': int(self.data['Radar_ShipRadar_MaxHeight']),
                        },
                        'small': {
                            'max_range': int(self.data['Radar_ShipSmallRadar_MaxRange']),
                            'min_height': int(self.data['Radar_ShipSmallRadar_MinHeight']),
                            'max_height': int(self.data['Radar_ShipSmallRadar_MaxHeight']),
                        },
                    },
                    'scouts': {
                        'max_range': int(self.data['Radar_ScoutRadar_MaxRange']),
                        'max_height': int(self.data['Radar_ScoutRadar_DeltaHeight']),
                        'alpha': int(self.data['Radar_ScoutGroundObjects_Alpha']),
                    },
                },
                'scouting': {
                    'ships_affect_radar': to_bool(self.data['Radar_ShipsAsRadar']),
                    'scouts_affect_radar': to_bool(self.data['Radar_ScoutsAsRadar']),
                    'only_scouts_complete_targets': to_bool(self.data['Radar_ScoutCompleteRecon']),
                },
                'communication': {
                    'tower_communication': to_bool(self.data['Radar_EnableTowerCommunications']),
                    'vectoring': not to_bool(self.data['Radar_DisableVectoring']),
                    'ai_radio_silence': to_bool(self.data['Misc_DisableAIRadioChatter']),
                },
                'home_bases': {
                    'hide_ai_aircrafts_after_landing': to_bool(self.data['Misc_DespawnAIPlanesAfterLanding']),
                    'hide_unpopulated': to_bool(self.data['Radar_HideUnpopulatedAirstripsFromMinimap']),
                    'hide_players_count': to_bool(self.data['Misc_HidePlayersCountOnHomeBase']),
                },
                'crater_visibility_muptipliers': {
                    'le_100kg': float(self.data['Misc_BombsCat1_CratersVisibilityMultiplier']),
                    'le_1000kg': float(self.data['Misc_BombsCat2_CratersVisibilityMultiplier']),
                    'gt_1000kg': float(self.data['Misc_BombsCat3_CratersVisibilityMultiplier']),
                },
            },
        }

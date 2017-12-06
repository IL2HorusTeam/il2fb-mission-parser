# coding: utf-8


from il2fb.commons.organization import Belligerents

from il2fb.parsers.mission.converters import to_bool
from il2fb.parsers.mission.sections.base import CollectingParser
from il2fb.parsers.mission.sections.base import ValuesParser


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


class MDSScoutsSectionParser(CollectingParser):
    """
    Parses ``MDS_Scouts`` section.
    View :ref:`detailed description <mds-scouts-section>`.
    """
    input_prefix = "MDS_Scouts_"
    output_prefix = "scouts_"

    def check_section_name(self, section_name):
        if not section_name.startswith(self.input_prefix):
            return False
        belligerent_name = self._get_belligerent_name(section_name)
        return bool(belligerent_name)

    def init_parser(self, section_name):
        super(MDSScoutsSectionParser, self).init_parser(section_name)
        belligerent_name = self._get_belligerent_name(section_name)
        self.belligerent = Belligerents[belligerent_name]
        self.output_key = "{0}{1}".format(self.output_prefix, belligerent_name)

    def _get_belligerent_name(self, section_name):
        return section_name[len(self.input_prefix):].lower()

    def clean(self):
        return {
            self.output_key: {
                'belligerent': self.belligerent,
                'aircrafts': self.data,
            },
        }

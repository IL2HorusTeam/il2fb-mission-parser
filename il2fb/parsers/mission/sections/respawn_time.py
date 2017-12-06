# coding: utf-8

from il2fb.parsers.mission.sections.base import ValuesParser


class RespawnTimeSectionParser(ValuesParser):
    """
    Parses ``RespawnTime`` section.
    View :ref:`detailed description <respawn-time-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "RespawnTime"

    def clean(self):
        return {
            'respawn_time': {
                'ships': {
                    'big': int(self.data['Bigship']),
                    'small': int(self.data['Ship']),
                },
                'balloons': int(self.data['Aeroanchored']),
                'artillery': int(self.data['Artillery']),
                'searchlights': int(self.data['Searchlight']),
            },
        }

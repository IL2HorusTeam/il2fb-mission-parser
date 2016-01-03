# -*- coding: utf-8 -*-

from il2fb.commons.organization import Belligerents

from . import CollectingParser


class MDSScoutsParser(CollectingParser):
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
        super(MDSScoutsParser, self).init_parser(section_name)
        belligerent_name = self._get_belligerent_name(section_name)
        self.belligerent = Belligerents[belligerent_name]
        self.output_key = "{}{}".format(self.output_prefix, belligerent_name)

    def _get_belligerent_name(self, section_name):
        return section_name[len(self.input_prefix):].lower()

    def clean(self):
        return {
            self.output_key: {
                'belligerent': self.belligerent,
                'aircrafts': self.data,
            },
        }

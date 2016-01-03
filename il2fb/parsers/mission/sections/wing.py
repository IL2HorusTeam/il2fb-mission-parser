# -*- coding: utf-8 -*-

from . import CollectingParser


class WingSectionParser(CollectingParser):
    """
    Parses ``Wing`` section.
    View :ref:`detailed description <wing-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Wing"

    def clean(self):
        return {'flights': self.data}

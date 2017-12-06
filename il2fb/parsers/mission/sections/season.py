# coding: utf-8

import datetime

from il2fb.parsers.mission.sections.base import ValuesParser


class SeasonSectionParser(ValuesParser):
    """
    Parses ``SEASON`` section.
    View :ref:`detailed description <season-section>`.
    """

    def check_section_name(self, section_name):
        """
        Implements abstract method. See
        :meth:`SectionParser.check_section_name` for semantics.
        """
        return section_name == "SEASON"

    def clean(self):
        """
        Redefines base method. See :meth:`SectionParser.clean` for
        semantics.

        Combines day, time and year into :class:`datetime.date` object.
        """
        date = datetime.date(int(self.data['Year']),
                             int(self.data['Month']),
                             int(self.data['Day']))
        return {'date': date, }

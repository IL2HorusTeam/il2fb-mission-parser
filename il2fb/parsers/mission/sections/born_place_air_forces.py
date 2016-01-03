# -*- coding: utf-8 -*-

from ..converters import to_air_force
from . import CollectingParser


class BornPlaceAirForcesSectionParser(CollectingParser):
    """
    Parses ``BornPlaceCountriesN`` section.
    View :ref:`detailed description <bornplace-air-forces-section>`.
    """
    input_prefix = 'BornPlaceCountries'
    output_prefix = 'home_base_air_forces_'

    def check_section_name(self, section_name):
        if not section_name.startswith(self.input_prefix):
            return False
        try:
            self._extract_section_number(section_name)
        except ValueError:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(BornPlaceAirForcesSectionParser, self).init_parser(section_name)
        self.output_key = (
            "{}{}".format(self.output_prefix,
                          self._extract_section_number(section_name)))
        self.countries = {}

    def _extract_section_number(self, section_name):
        start = len(self.input_prefix)
        return int(section_name[start:])

    def parse_line(self, line):
        air_force = to_air_force(line.strip())
        self.data.append(air_force)

    def clean(self):
        return {self.output_key: self.data, }

# -*- coding: utf-8 -*-

from ..constants import WEAPONS_CONTINUATION_MARK
from . import CollectingParser


class BornPlaceAircraftsParser(CollectingParser):
    """
    Parses ``BornPlaceN`` section.
    View :ref:`detailed description <bornplace-aircrafts-section>`.
    """
    input_prefix = 'BornPlace'
    output_prefix = 'home_base_aircrafts_'

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
        super(BornPlaceAircraftsParser, self).init_parser(section_name)
        self.output_key = (
            "{}{}".format(self.output_prefix,
                          self._extract_section_number(section_name)))
        self.aircraft = None

    def _extract_section_number(self, section_name):
        start = len(self.input_prefix)
        return int(section_name[start:])

    def parse_line(self, line):
        parts = line.split()

        if parts[0] == WEAPONS_CONTINUATION_MARK:
            self.aircraft['weapon_limitations'].extend(parts[1:])
        else:
            if self.aircraft:
                # Finalize previous aircraft
                self.data.append(self.aircraft)
            self.aircraft = BornPlaceAircraftsParser._parse_new_item(parts)

    @staticmethod
    def _parse_new_item(parts):
        code = parts.pop(0)
        limit = BornPlaceAircraftsParser._extract_limit(parts)
        return {
            'code': code,
            'limit': limit,
            'weapon_limitations': parts,
        }

    @staticmethod
    def _extract_limit(parts):
        if parts:
            limit = int(parts.pop(0))
            limit = limit if limit >= 0 else None
        else:
            limit = None
        return limit

    def clean(self):
        if self.aircraft:
            aircraft, self.aircraft = self.aircraft, None
            self.data.append(aircraft)

        return {self.output_key: self.data, }

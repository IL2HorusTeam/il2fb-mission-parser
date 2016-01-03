# -*- coding: utf-8 -*-

from ..converters import to_belligerent, to_skill, to_unit_type
from . import CollectingParser


class ChiefsSectionParser(CollectingParser):
    """
    Parses ``Chiefs`` section.
    View :ref:`detailed description <chiefs-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Chiefs"

    def parse_line(self, line):
        params = line.split()
        (uid, type_code, belligerent), params = params[0:3], params[3:]

        chief_type, code = type_code.split('.')
        try:
            chief_type = to_unit_type(chief_type)
        except Exception:
            # Use original string as unit type
            pass

        unit = {
            'id': uid,
            'code': code,
            'type': chief_type,
            'belligerent': to_belligerent(belligerent),
        }
        if params:
            hibernation, skill, recharge_time = params
            unit.update({
                'hibernation': int(hibernation),
                'skill': to_skill(skill),
                'recharge_time': float(recharge_time),
            })
        self.data.append(unit)

    def clean(self):
        return {'moving_units': self.data, }

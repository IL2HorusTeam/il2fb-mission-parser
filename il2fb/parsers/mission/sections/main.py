# -*- coding: utf-8 -*-

import datetime
import math

from il2fb.commons.weather import Conditions

from ..converters import to_belligerent
from . import ValuesParser


class MainParser(ValuesParser):
    """
    Parses ``MAIN`` section.
    View :ref:`detailed description <main-section>`.
    """

    def check_section_name(self, section_name):
        """
        Implements abstract method. See
        :meth:`SectionParser.check_section_name` for semantics.
        """
        return section_name == "MAIN"

    def clean(self):
        """
        Redefines base method. See :meth:`SectionParser.clean` for
        semantics.
        """
        weather_conditions = int(self.data['CloudType'])
        return {
            'location_loader': self.data['MAP'],
            'time': {
                'value': self._to_time(self.data['TIME']),
                'is_fixed': 'TIMECONSTANT' in self.data,
            },
            'weather_conditions': Conditions.get_by_value(weather_conditions),
            'cloud_base': int(float(self.data['CloudHeight'])),
            'player': {
                'belligerent': to_belligerent(self.data['army']),
                'flight_id': self.data.get('player'),
                'aircraft_index': int(self.data['playerNum']),
                'fixed_weapons': 'WEAPONSCONSTANT' in self.data,
            },
        }

    def _to_time(self, value):
        time = float(value)
        minutes, hours = math.modf(time)
        return datetime.time(int(hours), int(minutes * 60))

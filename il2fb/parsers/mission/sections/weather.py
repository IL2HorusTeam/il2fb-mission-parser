# coding: utf-8

from il2fb.commons.weather import Gust, Turbulence

from il2fb.parsers.mission.sections.base import ValuesParser


class WeatherSectionParser(ValuesParser):
    """
    Parses ``WEATHER`` section.
    View :ref:`detailed description <weather-section>`.
    """

    def check_section_name(self, section_name):
        """
        Implements abstract method. See
        :meth:`SectionParser.check_section_name` for semantics.
        """
        return section_name == "WEATHER"

    def clean(self):
        """
        Redefines base method. See :meth:`SectionParser.clean` for
        semantics.
        """
        gust = int(self.data['Gust'])
        turbulence = int(self.data['Turbulence'])
        return {
            'weather': {
                'wind': {
                    'direction': float(self.data['WindDirection']),
                    'speed': float(self.data['WindSpeed']),
                },
                'gust': Gust.get_by_value(gust),
                'turbulence': Turbulence.get_by_value(turbulence),
            },
        }

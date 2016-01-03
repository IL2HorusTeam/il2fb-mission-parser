# -*- coding: utf-8 -*-

from il2fb.commons.organization import AirForces, Regiments

from ..converters import to_skill
from . import ValuesParser


class FlightInfoParser(ValuesParser):
    """
    Parses settings for a moving flight group.
    View :ref:`detailed description <flight-info-section>`.
    """

    def check_section_name(self, section_name):
        try:
            self._decompose_section_name(section_name)
        except Exception:
            return False
        else:
            return True

    def init_parser(self, section_name):
        super(FlightInfoParser, self).init_parser(section_name)
        self.output_key = section_name
        self.flight_info = self._decompose_section_name(section_name)

    def _decompose_section_name(self, section_name):
        prefix = section_name[:-2]
        squadron, flight = section_name[-2:]

        try:
            regiment = None
            air_force = AirForces.get_by_flight_prefix(prefix)
        except ValueError:
            regiment = Regiments.get_by_code_name(prefix)
            air_force = regiment.air_force

        return {
            'id': section_name,
            'air_force': air_force,
            'regiment': regiment,
            'squadron_index': int(squadron),
            'flight_index': int(flight),
        }

    def clean(self):
        count = int(self.data['Planes'])
        code = self.data['Class'].split('.', 1)[1]
        aircrafts = []

        def _add_if_present(target, key, value):
            if value:
                target[key] = value

        for i in range(count):
            aircraft = {
                'index': i,
                'has_markings': self._has_markings(i),
                'skill': self._get_skill(i),
            }
            _add_if_present(
                aircraft, 'aircraft_skin', self._get_skin('skin', i))
            _add_if_present(
                aircraft, 'nose_art', self._get_skin('nose_art', i))
            _add_if_present(
                aircraft, 'pilot_skin', self._get_skin('pilot', i))
            _add_if_present(
                aircraft, 'spawn_object', self._get_spawn_object_id(i))
            aircrafts.append(aircraft)

        self.flight_info.update({
            'ai_only': 'OnlyAI' in self.data,
            'aircrafts': aircrafts,
            'code': code,
            'fuel': int(self.data['Fuel']),
            'with_parachutes': 'Parachute' not in self.data,
            'count': count,
            'weapons': self.data['weapons'],
        })

        return {self.output_key: self.flight_info}

    def _get_skill(self, aircraft_id):
        if 'Skill' in self.data:
            return to_skill(self.data['Skill'])
        else:
            return to_skill(self.data['Skill{:}'.format(aircraft_id)])

    def _has_markings(self, aircraft_id):
        return 'numberOn{:}'.format(aircraft_id) not in self.data

    def _get_skin(self, prefix, aircraft_id):
        return self.data.get('{:}{:}'.format(prefix, aircraft_id))

    def _get_spawn_object_id(self, aircraft_id):
        return self.data.get('spawn{:}'.format(aircraft_id))

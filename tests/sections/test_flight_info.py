# -*- coding: utf-8 -*-

import unittest

from il2fb.commons import Skills
from il2fb.commons.organization import AirForces, Regiments

from il2fb.parsers.mission.sections.flight_info import FlightInfoParser

from .mixins import SectionParserTestCaseMixin


class FlightInfoParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):

    def test_check_section_name(self):
        parser = FlightInfoParser()
        self.assertTrue(parser.check_section_name('r0100'))
        self.assertTrue(parser.check_section_name('3GvIAP00'))

    def test_multiple_aircrafts(self):
        lines = [
            "Planes 2",
            "Skill0 1",
            "Class air.A_20C",
            "Fuel 100",
            "weapons default",
            "Skill0 2",
            "Skill1 3",
            "Skill2 1",
            "Skill3 1",
            "skin0 Funky.bmp",
            "numberOn1 0",
            "spawn0 0_Static",
        ]
        expected = {
            '3GvIAP00': {
                'id': '3GvIAP00',
                'squadron_index': 0,
                'flight_index': 0,
                'air_force': AirForces.vvs_rkka,
                'regiment': Regiments.get_by_code_name('3GvIAP'),
                'code': "A_20C",
                'count': 2,
                'fuel': 100,
                'weapons': "default",
                'ai_only': False,
                'with_parachutes': True,
                'aircrafts': [
                    {
                        'index': 0,
                        'skill': Skills.veteran,
                        'aircraft_skin': "Funky.bmp",
                        'has_markings': True,
                        'spawn_object': '0_Static',
                    },
                    {
                        'index': 1,
                        'skill': Skills.ace,
                        'has_markings': False,
                    },
                ],
            },
        }
        self.assertParser(FlightInfoParser, '3GvIAP00', lines, expected)

    def test_single_aircraft(self):
        lines = [
            "Planes 1",
            "Skill 1",
            "Class air.A_20C",
            "Fuel 100",
            "weapons default",
            "skin0 Funky.bmp",
            "numberOn0 0",
            "spawn0 0_Static",
        ]
        expected = {
            '3GvIAP01': {
                'id': '3GvIAP01',
                'squadron_index': 0,
                'flight_index': 1,
                'air_force': AirForces.vvs_rkka,
                'regiment': Regiments.get_by_code_name('3GvIAP'),
                'code': "A_20C",
                'count': 1,
                'fuel': 100,
                'weapons': "default",
                'with_parachutes': True,
                'ai_only': False,
                'aircrafts': [
                    {
                        'index': 0,
                        'skill': Skills.average,
                        'aircraft_skin': "Funky.bmp",
                        'has_markings': False,
                        'spawn_object': '0_Static',
                    },
                ],
            },
        }
        self.assertParser(FlightInfoParser, '3GvIAP01', lines, expected)

    def test_invalid_section_name(self):
        p = FlightInfoParser()
        self.assertFalse(p.check_section_name("Something unknown"))

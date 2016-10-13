# coding: utf-8

import datetime
import unittest

from il2fb.commons import Skills, UnitTypes
from il2fb.commons.organization import AirForces, Belligerents

from il2fb.parsers.mission.constants import NULL
from il2fb.parsers.mission.converters import (
    to_bool, to_belligerent, to_skill, to_unit_type, to_air_force,
    to_time,
)


class ConvertersTestCase(unittest.TestCase):

    def test_to_bool(self):
        self.assertFalse(to_bool('0'))
        self.assertTrue(to_bool('1'))
        self.assertTrue(to_bool('-1'))

    def test_to_belligerent(self):
        self.assertEqual(to_belligerent('0'), Belligerents.none)
        self.assertEqual(to_belligerent('1'), Belligerents.red)
        self.assertEqual(to_belligerent('2'), Belligerents.blue)

    def test_to_skill(self):
        self.assertEqual(to_skill('3'), Skills.ace)

    def test_to_unit_type(self):
        self.assertEqual(to_unit_type('planes'), UnitTypes.aircraft)

    def test_to_air_force(self):
        self.assertIsNone(to_air_force(""))
        self.assertEqual(to_air_force(NULL), AirForces.vvs_rkka)
        self.assertEqual(to_air_force("nn"), AirForces.none)

    def test_to_time(self):
        self.assertEqual(to_time("11.75"), datetime.time(11, 45))

# -*- coding: utf-8 -*-

import unittest

from il2fb.commons.spatial import Point2D
from il2fb.commons.targets import TargetTypes, TargetPriorities

from il2fb.parsers.mission.sections.target import TargetSectionParser

from .mixins import SectionParserTestCaseMixin


class TargetSectionParserTestCase(SectionParserTestCaseMixin, unittest.TestCase):
    """
    Test ``Target`` section parser.
    """

    def test_target_destroy(self):
        """
        Test ``destroy`` target type parser.
        """
        lines = [
            "0 0 0 0 500 90939 91871 0 1 10_Chief 91100 91500",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.destroy,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': False,
                    'delay': 0,
                    'destruction_level': 50,
                    'pos': Point2D(90939.0, 91871.0),
                    'object': {
                        'waypoint': 1,
                        'id': '10_Chief',
                        'pos': Point2D(91100.0, 91500.0),
                    },
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_destroy_area(self):
        """
        Test 'destroy area' target type parser.
        """
        lines = [
            "1 1 1 60 750 133960 87552 1350",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.destroy_area,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'delay': 60,
                    'destruction_level': 75,
                    'pos': Point2D(133960.0, 87552.0),
                    'radius': 1350,
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_destroy_bridge(self):
        """
        Test 'destroy bridge' target type parser.
        """
        lines = [
            "2 2 1 30 500 135786 84596 0 0  Bridge84 135764 84636",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.destroy_bridge,
                    'priority': TargetPriorities.hidden,
                    'in_sleep_mode': True,
                    'delay': 30,
                    'pos': Point2D(135786.0, 84596.0),
                    'object': {
                        'id': 'Bridge84',
                        'pos': Point2D(135764.0, 84636.0),
                    },
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_recon(self):
        """
        Test ``recon`` target type parser.
        """
        lines = [
            "3 1 1 50 500 133978 87574 1150",
            "3 0 1 40 501 134459 85239 300 0 1_Chief 134360 85346",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.recon,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'delay': 50,
                    'requires_landing': False,
                    'pos': Point2D(133978.0, 87574.0),
                    'radius': 1150,
                },
                {
                    'type': TargetTypes.recon,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': True,
                    'delay': 40,
                    'requires_landing': True,
                    'pos': Point2D(134459.0, 85239.0),
                    'radius': 300,
                    'object': {
                        'waypoint': 0,
                        'id': '1_Chief',
                        'pos': Point2D(134360.0, 85346.0),
                    },
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_escort(self):
        """
        Test ``escort`` target type parser.
        """
        lines = [
            "4 0 1 10 750 134183 85468 0 1 r0100 133993 85287",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.escort,
                    'priority': TargetPriorities.primary,
                    'in_sleep_mode': True,
                    'delay': 10,
                    'destruction_level': 75,
                    'pos': Point2D(134183.0, 85468.0),
                    'object': {
                        'waypoint': 1,
                        'id': 'r0100',
                        'pos': Point2D(133993.0, 85287.0),
                    },
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_cover(self):
        """
        Test ``cover`` target type parser.
        """
        lines = [
            "5 1 1 20 250 132865 87291 0 1 1_Chief 132866 86905",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.cover,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'delay': 20,
                    'destruction_level': 25,
                    'pos': Point2D(132865.0, 87291.0),
                    'object': {
                        'waypoint': 1,
                        'id': '1_Chief',
                        'pos': Point2D(132866.0, 86905.0),
                    },
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_cover_area(self):
        """
        Test 'cover area' target type parser.
        """
        lines = [
            "6 1 1 30 500 134064 88188 1350",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.cover_area,
                    'priority': TargetPriorities.secondary,
                    'in_sleep_mode': True,
                    'delay': 30,
                    'destruction_level': 50,
                    'pos': Point2D(134064.0, 88188.0),
                    'radius': 1350,
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

    def test_target_cover_bridge(self):
        """
        Test 'cover bridge' target type parser.
        """
        lines = [
            "7 2 1 30 500 135896 84536 0 0  Bridge84 135764 84636",
        ]

        expected = {
            'targets': [
                {
                    'type': TargetTypes.cover_bridge,
                    'priority': TargetPriorities.hidden,
                    'in_sleep_mode': True,
                    'delay': 30,
                    'pos': Point2D(135896.0, 84536.0),
                    'object': {
                        'id': 'Bridge84',
                        'pos': Point2D(135764.0, 84636.0),
                    },
                },
            ],
        }
        self.assertParser(TargetSectionParser, 'Target', lines, expected)

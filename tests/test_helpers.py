# -*- coding: utf-8 -*-

import unittest

from il2fb.parsers.mission.helpers import move_if_present, set_if_present


class HelpersTestCase(unittest.TestCase):

    def test_move_if_present(self):
        dst = {}
        src = {
            'foo': "foo_string",
            'bar_buz': "bar_string",
        }

        move_if_present(dst, src, 'foo')
        move_if_present(dst, src, 'bar', 'bar_buz')
        move_if_present(dst, src, 'qux')

        self.assertEquals(
            dst,
            {
                'foo': "foo_string",
                'bar': "bar_string",
            }
        )

    def test_set_if_present(self):
        dst = {}

        set_if_present(dst, 'foo', 1)
        set_if_present(dst, 'bar', None)
        set_if_present(dst, 'baz', [])

        self.assertEquals(dst, {'foo': 1})

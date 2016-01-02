# -*- coding: utf-8 -*-

import itertools
import unittest

from il2fb.parsers.mission.constants import COMMENT_MARKERS
from il2fb.parsers.mission.utils import (
    move_if_present, set_if_present, strip_comments,
)


class UtilsTestCase(unittest.TestCase):

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

    def test_strip_comments(self):
        line = "  123   \n"
        self.assertEqual(strip_comments(line), "123")

        line = "  {:} \n".format(''.join(COMMENT_MARKERS))
        self.assertEqual(strip_comments(line), "")

        for marker in COMMENT_MARKERS:
            line = "  123 {:} 456 ".format(marker)
            self.assertEqual(strip_comments(line), "123")

        for combination in itertools.permutations(COMMENT_MARKERS):
            line = "  123 {:} 456 ".format(''.join(combination))
            self.assertEqual(strip_comments(line), "123")

# coding: utf-8

from il2fb.parsers.mission.constants import COMMENT_MARKERS


def move_if_present(dst, src, dst_key, src_key=None):
    src_key = src_key or dst_key
    if src_key in src:
        dst[dst_key] = src.pop(src_key)


def set_if_present(dst, key, value):
    if value:
        dst[key] = value


def strip_comments(line):
    for marker in COMMENT_MARKERS:
        line = line.split(marker, 1)[0]

    return line.strip()

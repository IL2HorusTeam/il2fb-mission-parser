# -*- coding: utf-8 -*-


def move_if_present(dst, src, dst_key, src_key=None):
    src_key = src_key or dst_key
    if src_key in src:
        dst[dst_key] = src.pop(src_key)


def set_if_present(dst, key, value):
    if value:
        dst[key] = value

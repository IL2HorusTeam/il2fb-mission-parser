# -*- coding: utf-8 -*-
"""
Different helpers.
"""

try:
    from django.conf import settings
    if settings.configured:
        from django.utils.translation import ugettext_lazy
        _ = ugettext_lazy
    else:
        raise ImportError()
except ImportError:
    def _(value):
        return value


def covert_str(value):
    """
    Conversion of type str to a type int or float
    On error, returns the type str
    """
    result = value
    try:
        result = int(value)
    except ValueError:
        result = float(value)
    finally:
        return result
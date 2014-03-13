# -*- coding: utf-8 -*-
"""
Regular expression.
"""
import re


"""Flags to be used for matching strings."""
RE_FLAGS = re.VERBOSE

"""
Pattern for parser section in the configuration files missions
Method re.sub
Input format: [MAIN]
Output format: MAIN
"""
RE_SECTION = """
\[|           # left section wrapper
\]|           # right section wrapper
\s            # line feed
$             # end of the string
"""
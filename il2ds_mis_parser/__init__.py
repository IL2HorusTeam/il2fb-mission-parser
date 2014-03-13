# -*- coding: utf-8 -*-
"""
Parser files missions and properties.
"""
from il2ds_mis_parser.constants import *
from il2ds_mis_parser.regex import *


def parser_section(section_line):
    """
    Returns the name of the section without the characters [ and ]
    """
    section_name = re.sub(RE_SECTION, '', section_line, flags=RE_FLAGS)
    return section_name


def parser_line(line_setting, pattern):
    """
    The parser settings
    """
    setting = re.compile(pattern)
    return setting


def parser_mis(mis_file, section):
    """
    The parser file mission
    """
    settings = {}
    try:
        with open(mis_file) as f:
            for line in f:
                if line.startswith(section):
                    section_name = parser_section(line)
                elif line.startswith('['):
                    break
                else:
                    line_setting = line.split()
                    settings.update({line_setting[0]: line_setting[1]})
                    if line.startswith('['):
                        break
        return {
            section_name: settings
        }
    except IOError as e:
        print 'No such file or directory: %s' % e.strerror
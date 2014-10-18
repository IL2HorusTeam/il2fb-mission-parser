# -*- coding: utf-8 -*-

from .parsers import FileParser
from .version import VERSION

parse_mission = FileParser().parse

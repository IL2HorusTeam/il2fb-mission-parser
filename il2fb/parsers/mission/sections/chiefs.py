# coding: utf-8

from il2fb.commons.spatial import Point2D
from il2fb.commons.structures import BaseStructure

from il2fb.parsers.mission.converters import to_belligerent
from il2fb.parsers.mission.converters import to_skill
from il2fb.parsers.mission.converters import to_speed
from il2fb.parsers.mission.converters import to_unit_type
from il2fb.parsers.mission.sections.base import CollectingParser


class ChiefsSectionParser(CollectingParser):
    """
    Parses ``Chiefs`` section.
    View :ref:`detailed description <chiefs-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Chiefs"

    def parse_line(self, line):
        params = line.split()
        (uid, type__code, belligerent), params = params[0:3], params[3:]

        type_code, unit_code = type__code.split('.')
        unit_type = self._get_unit_type(type_code)

        unit = {
            'id': uid,
            'code': unit_code,
            'type': unit_type,
            'belligerent': to_belligerent(belligerent),
        }
        if params:
            hibernation, skill, recharge_time = params
            unit.update({
                'hibernation': int(hibernation),
                'skill': to_skill(skill),
                'recharge_time': float(recharge_time),
            })
        self.data.append(unit)

    @staticmethod
    def _get_unit_type(type_code):
        try:
            return to_unit_type(type_code)
        except:
            # Use original string as unit type
            return type_code

    def clean(self):
        return {'moving_units': self.data, }


class GroundRoutePoint(BaseStructure):
    __slots__ = ['pos', 'is_checkpoint', 'delay', 'section_length', 'speed', ]

    def __init__(self, pos, is_checkpoint, delay=None, section_length=None,
                 speed=None):
        self.pos = pos
        self.is_checkpoint = is_checkpoint
        self.delay = delay
        self.section_length = section_length
        self.speed = speed

    def __repr__(self):
        return "<GroundRoutePoint '{0};{1}'>".format(self.pos.x, self.pos.y)


class ChiefRoadSectionParser(CollectingParser):
    """
    Parses ``N_Chief_Road`` section.
    View :ref:`detailed description <chief-road-section>`.
    """
    id_suffix = "_Chief"
    section_suffix = "_Road"
    input_suffix = id_suffix + section_suffix
    output_prefix = 'route_'

    def check_section_name(self, section_name):
        if not section_name.endswith(self.input_suffix):
            return False
        unit_id = self._extract_unit_id(section_name)
        stop = unit_id.index(self.id_suffix)
        return unit_id[:stop].isdigit()

    def init_parser(self, section_name):
        super(ChiefRoadSectionParser, self).init_parser(section_name)
        unit_id = self._extract_unit_id(section_name)
        self.output_key = "{0}{1}".format(self.output_prefix, unit_id)

    def _extract_unit_id(self, section_name):
        stop = section_name.index(self.section_suffix)
        return section_name[:stop]

    def parse_line(self, line):
        params = line.split()
        pos, params = params[0:2], params[3:]

        args = {
            'pos': Point2D(*pos),
        }

        is_checkpoint = bool(params)
        args['is_checkpoint'] = is_checkpoint

        if is_checkpoint:
            args['delay'] = int(params[0])
            args['section_length'] = int(params[1])
            args['speed'] = to_speed(params[2])

        point = GroundRoutePoint(**args)
        self.data.append(point)

    def clean(self):
        return {self.output_key: self.data}

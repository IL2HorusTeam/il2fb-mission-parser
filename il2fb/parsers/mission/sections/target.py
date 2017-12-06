# coding: utf-8

from il2fb.commons.spatial import Point2D
from il2fb.commons.targets import TargetTypes, TargetPriorities

from il2fb.parsers.mission.converters import to_bool
from il2fb.parsers.mission.sections.base import CollectingParser


def to_destruction_level(value):
    return int(value) / 10


class TargetSectionParser(CollectingParser):
    """
    Parses ``Target`` section.
    View :ref:`detailed description <target-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Target"

    def parse_line(self, line):
        params = line.split()

        type_code, priority, in_sleep_mode, delay = params[:4]
        params = params[4:]

        target_type = TargetTypes.get_by_value(int(type_code))
        target = {
            'type': target_type,
            'priority': TargetPriorities.get_by_value(int(priority)),
            'in_sleep_mode': to_bool(in_sleep_mode),
            'delay': int(delay),
        }

        subparser = self._subparsers.get(target_type)
        if subparser is not None:
            target.update(subparser(params))

        self.data.append(target)

    def parse_destroy_or_cover_or_escort(params):
        """
        Parse extra parameters for targets with type 'destroy' or 'cover' or
        'escort'.
        """
        destruction_level = to_destruction_level(params[0])
        pos, waypoint, object_code = params[1:3], params[4], params[5]
        object_pos = params[6:8]
        return {
            'destruction_level': destruction_level,
            'pos': Point2D(*pos),
            'object': {
                'waypoint': int(waypoint),
                'id': object_code,
                'pos': Point2D(*object_pos),
            },
        }

    def parse_destroy_or_cover_bridge(params):
        """
        Parse extra parameters for targets with type 'destroy bridge' or
        'cover bridge'.
        """
        pos, object_code, object_pos = params[1:3], params[5], params[6:8]
        return {
            'pos': Point2D(*pos),
            'object': {
                'id': object_code,
                'pos': Point2D(*object_pos),
            },
        }

    def parse_destroy_or_cover_area(params):
        """
        Parse extra parameters for targets with type 'destroy area' or
        'cover area'.
        """
        destruction_level = to_destruction_level(params[0])
        pos_x, pos_y, radius = params[1:]
        return {
            'destruction_level': destruction_level,
            'pos': Point2D(pos_x, pos_y),
            'radius': int(radius),
        }

    def parse_recon(params):
        """
        Parse extra parameters for targets with 'recon' type.
        """
        requires_landing = params[0] != '500'
        pos, radius, params = params[1:3], params[3], params[4:]
        data = {
            'radius': int(radius),
            'requires_landing': requires_landing,
            'pos': Point2D(*pos),
        }
        if params:
            waypoint, object_code = params[:2]
            object_pos = params[2:]
            data['object'] = {
                'waypoint': int(waypoint),
                'id': object_code,
                'pos': Point2D(*object_pos),
            }
        return data

    _subparsers = {
        TargetTypes.destroy: parse_destroy_or_cover_or_escort,
        TargetTypes.destroy_bridge: parse_destroy_or_cover_bridge,
        TargetTypes.destroy_area: parse_destroy_or_cover_area,
        TargetTypes.recon: parse_recon,
        TargetTypes.escort: parse_destroy_or_cover_or_escort,
        TargetTypes.cover: parse_destroy_or_cover_or_escort,
        TargetTypes.cover_area: parse_destroy_or_cover_area,
        TargetTypes.cover_bridge: parse_destroy_or_cover_bridge,
    }

    def clean(self):
        return {'targets': self.data, }

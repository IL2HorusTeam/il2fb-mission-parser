# -*- coding: utf-8 -*-

from il2fb.commons.spatial import Point2D
from il2fb.commons.structures import BaseStructure

from ..constants import NULL, IS_STATIONARY_AIRCRAFT_RESTORABLE
from ..converters import (
    to_bool, to_skill, to_air_force, to_unit_type, to_belligerent,
)
from . import CollectingParser


class StationaryObject(BaseStructure):
    __slots__ = [
        'id', 'belligerent', 'code', 'pos', 'rotation_angle', 'type',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type):
        self.id = id
        self.belligerent = belligerent
        self.code = code
        self.pos = pos
        self.rotation_angle = rotation_angle
        self.type = type

    def __repr__(self):
        return "<{0} '{1}'>".format(self.__class__.__name__, self.id)


class StationaryArtillery(StationaryObject):
    __slots__ = StationaryObject.__slots__ + [
        'awakening_time', 'range', 'skill', 'use_spotter',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type,
                 awakening_time, range, skill, use_spotter):
        super(StationaryArtillery, self).__init__(
            id, belligerent, code, pos, rotation_angle, type)
        self.awakening_time = awakening_time
        self.range = range
        self.skill = skill
        self.use_spotter = use_spotter


class StationaryAircraft(StationaryObject):
    __slots__ = StationaryObject.__slots__ + [
        'air_force', 'allows_spawning', 'is_restorable', 'skin',
        'show_markings',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type,
                 air_force, allows_spawning, is_restorable, skin,
                 show_markings):
        super(StationaryAircraft, self).__init__(
            id, belligerent, code, pos, rotation_angle, type)
        self.air_force = air_force
        self.allows_spawning = allows_spawning
        self.is_restorable = is_restorable
        self.skin = skin
        self.show_markings = show_markings


class StationaryShip(StationaryObject):
    __slots__ = StationaryObject.__slots__ + [
        'awakening_time', 'recharge_time', 'skill',
    ]

    def __init__(self, id, belligerent, code, pos, rotation_angle, type,
                 awakening_time, recharge_time, skill):
        super(StationaryShip, self).__init__(
            id, belligerent, code, pos, rotation_angle, type)
        self.awakening_time = awakening_time
        self.recharge_time = recharge_time
        self.skill = skill


class NStationarySectionParser(CollectingParser):
    """
    Parses ``NStationary`` section.
    View :ref:`detailed description <nstationary-section>`.
    """

    def __parse_artillery(params):
        """
        Parse additional options for ``artillery`` type
        """
        try:
            awakening_time, the_range, skill, use_spotter = params
            skill = to_skill(skill)
            use_spotter = to_bool(use_spotter)
        except ValueError:
            try:
                awakening_time, the_range = params
            except ValueError:
                awakening_time, the_range = params[0], 0
            skill, use_spotter = None, False

        return {
            'awakening_time': float(awakening_time),
            'range': int(the_range),
            'skill': skill,
            'use_spotter': use_spotter,
        }

    def __parse_aircraft(params):
        """
        Parse additional options for ``planes`` type
        """
        try:
            air_force, allows_spawning__restorable = params[1:3]
            skin, show_markings = params[4:]
        except ValueError:
            air_force, allows_spawning__restorable = None, 0
            skin, show_markings = params[1:]

        is_restorable = allows_spawning__restorable == IS_STATIONARY_AIRCRAFT_RESTORABLE
        skin = None if skin == NULL else skin

        return {
            'air_force': to_air_force(air_force),
            'allows_spawning': to_bool(allows_spawning__restorable),
            'is_restorable': is_restorable,
            'skin': skin,
            'show_markings': to_bool(show_markings),
        }

    def __parse_ship(params):
        """
        Parse additional options for ``ships`` type
        """
        awakening_time, skill, recharge_time = params[1:]
        return {
            'awakening_time': float(awakening_time),
            'recharge_time': float(recharge_time),
            'skill': to_skill(skill),
        }

    subparsers = {
        'artillery': (StationaryArtillery, __parse_artillery),
        'planes': (StationaryAircraft, __parse_aircraft),
        'ships': (StationaryShip, __parse_ship),
    }

    def check_section_name(self, section_name):
        return section_name == "NStationary"

    def parse_line(self, line):
        params = line.split()

        oid, object_name, belligerent = params[0], params[1], params[2]
        pos = params[3:5]
        rotation_angle = params[5]
        params = params[6:]

        type_name = self._get_type_name(object_name)
        try:
            object_type = to_unit_type(type_name)
        except Exception:
            # Use original string as object's type
            object_type = type_name

        the_object = {
            'id': oid,
            'belligerent': to_belligerent(belligerent),
            'code': self._get_code(object_name),
            'pos': Point2D(*pos),
            'rotation_angle': float(rotation_angle),
            'type': object_type,
        }

        if type_name in self.subparsers:
            structure, subparser = self.subparsers.get(type_name)
            the_object.update(subparser(params))
        else:
            structure = StationaryObject

        self.data.append(structure(**the_object))

    def _get_type_name(self, object_name):
        if object_name.startswith('ships'):
            return "ships"
        else:
            start = object_name.index('.') + 1
            stop = object_name.rindex('.')
            return object_name[start:stop]

    def _get_code(self, code):
        start = code.index('$') + 1
        return code[start:]

    def clean(self):
        return {'stationary': self.data, }

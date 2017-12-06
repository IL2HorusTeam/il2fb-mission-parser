# coding: utf-8

from il2fb.commons.spatial import Point2D
from il2fb.commons.structures import BaseStructure

from il2fb.parsers.mission.converters import to_angle
from il2fb.parsers.mission.converters import to_belligerent
from il2fb.parsers.mission.sections.base import CollectingParser


class Building(BaseStructure):
    __slots__ = ['id', 'belligerent', 'code', 'pos', 'rotation_angle', ]

    def __init__(self, id, belligerent, code, pos, rotation_angle):
        self.id = id
        self.belligerent = belligerent
        self.code = code
        self.pos = pos
        self.rotation_angle = rotation_angle

    def __repr__(self):
        return "<Building '{0}'>".format(self.id)


class BuildingsSectionParser(CollectingParser):
    """
    Parses ``Buildings`` section.
    View :ref:`detailed description <buildings-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "Buildings"

    def parse_line(self, line):
        params = line.split()
        oid, building_object, belligerent = params[:3]
        pos_x, pos_y, rotation_angle = params[3:]
        code = building_object.split('$')[1]
        self.data.append(Building(
            id=oid,
            belligerent=to_belligerent(belligerent),
            code=code,
            pos=Point2D(pos_x, pos_y),
            rotation_angle=to_angle(rotation_angle),
        ))

    def clean(self):
        return {'buildings': self.data, }

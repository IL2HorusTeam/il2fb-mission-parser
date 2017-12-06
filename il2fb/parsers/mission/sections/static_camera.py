# coding: utf-8


from il2fb.commons.spatial import Point3D
from il2fb.commons.structures import BaseStructure

from il2fb.parsers.mission.converters import to_belligerent
from il2fb.parsers.mission.sections.base import CollectingParser


class StaticCamera(BaseStructure):
    __slots__ = ['belligerent', 'pos', ]

    def __init__(self, belligerent, pos):
        self.belligerent = belligerent
        self.pos = pos

    def __repr__(self):
        return (
            "<StaticCamera '{0};{1};{2}'>"
            .format(self.pos.x, self.pos.y, self.pos.z)
        )


class StaticCameraSectionParser(CollectingParser):
    """
    Parses ``StaticCamera`` section.
    View :ref:`detailed description <static-camera-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "StaticCamera"

    def parse_line(self, line):
        pos_x, pos_y, pos_z, belligerent = line.split()
        self.data.append(StaticCamera(
            belligerent=to_belligerent(belligerent),
            pos=Point3D(pos_x, pos_y, pos_z),
        ))

    def clean(self):
        return {'cameras': self.data, }

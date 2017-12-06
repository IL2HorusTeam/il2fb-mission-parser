# coding: utf-8

from il2fb.commons.spatial import Point2D
from il2fb.commons.structures import BaseStructure

from il2fb.parsers.mission.converters import to_belligerent
from il2fb.parsers.mission.sections.base import CollectingParser


class FrontMarker(BaseStructure):
    __slots__ = ['id', 'belligerent', 'pos', ]

    def __init__(self, id, belligerent, pos):
        self.id = id
        self.belligerent = belligerent
        self.pos = pos

    def __repr__(self):
        return "<FrontMarker '{0}'>".format(self.id)


class FrontMarkerSectionParser(CollectingParser):
    """
    Parses ``FrontMarker`` section.
    View :ref:`detailed description <front-marker-section>`.
    """

    def check_section_name(self, section_name):
        return section_name == "FrontMarker"

    def parse_line(self, line):
        oid, pos_x, pos_y, belligerent = line.split()
        self.data.append(FrontMarker(
            id=oid,
            belligerent=to_belligerent(belligerent),
            pos=Point2D(pos_x, pos_y),
        ))

    def clean(self):
        return {'markers': self.data, }

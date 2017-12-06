# coding: utf-8

from il2fb.commons.spatial import Point2D
from il2fb.commons.structures import BaseStructure

from il2fb.parsers.mission.converters import to_angle
from il2fb.parsers.mission.converters import to_belligerent
from il2fb.parsers.mission.sections.base import CollectingParser


class Rocket(BaseStructure):
    __slots__ = [
        'id', 'code', 'belligerent', 'pos', 'rotation_angle', 'delay', 'count',
        'period', 'destination',
    ]

    def __init__(
        self, id, code, belligerent, pos, rotation_angle, delay, count, period,
        destination,
    ):
        self.id = id
        self.code = code
        self.belligerent = belligerent
        self.pos = pos
        self.rotation_angle = rotation_angle
        self.delay = delay
        self.count = count
        self.period = period
        self.destination = destination

    def __repr__(self):
        return "<Rocket '{0}'>".format(self.id)


class RocketSectionParser(CollectingParser):
    """
    Parses ``Rocket`` section.
    View :ref:`detailed description <rocket-section>`.

    """

    def check_section_name(self, section_name):
        return section_name == "Rocket"

    def parse_line(self, line):
        params = line.split()

        oid, code, belligerent = params[0:3]
        pos = params[3:5]
        rotation_angle, delay, count, period = params[5:9]
        destination = params[9:]

        self.data.append(Rocket(
            id=oid,
            code=code,
            belligerent=to_belligerent(belligerent),
            pos=Point2D(*pos),
            rotation_angle=to_angle(rotation_angle),
            delay=float(delay),
            count=int(count),
            period=float(period),
            destination=Point2D(*destination) if destination else None
        ))

    def clean(self):
        return {'rockets': self.data}

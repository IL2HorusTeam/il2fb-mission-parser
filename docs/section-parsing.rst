Section parsing
===============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80-%D1%81%D0%B5%D0%BA%D1%86%D0%B8%D0%B9>`_


This chapter describes output formats for all parsers. Datailed description of
input data aslo included.

Note, that :class:`~il2fb.parsers.mission.MissionParser` is the root
parser. It gets data from all other parsers and organizes it in special manner.

.. note::

    Format of mission files can be very tricky in some sections and original
    key names may be misleading. We made our best to adopt strange things
    for normal humans, but some questions still may appear in your mind.
    Get ready!

.. note::

    If you are not familiar with missions, take a look at `some of them <https://github.com/IL2HorusTeam/il2fb-mission-parser/tree/b3424b40e1ff69018c75591214f4755943fe6491/tests/data>`_.

.. toctree::
    :maxdepth: 1

    parsers/main
    parsers/season
    parsers/weather
    parsers/respawn-time
    parsers/mds
    parsers/mds-scouts
    parsers/chiefs
    parsers/chief-road
    parsers/nstationary
    parsers/buildings
    parsers/target
    parsers/bornplace
    parsers/bornplace-aircrafts
    parsers/bornplace-air-forces
    parsers/static-camera
    parsers/front-marker
    parsers/rocket
    parsers/wing
    parsers/flight-info
    parsers/flight-route
    parsers/file-parser

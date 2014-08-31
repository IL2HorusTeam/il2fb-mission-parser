Output format
=============

This chapter describes output formats for all parsers. Datailed description of
input data aslo included.

Note, that :class:`~il2fb.parsers.mission.parsers.FileParser` is the root
parser. It gets data from all other parsers and organizes it in special manner.

.. note::

    Format of mission files can be very tricky in some sections and original
    key names may be misleading. We made our best to adopt strange things
    for normal humans, but some questions still may appear in your mind.
    Get ready!

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
    parsers/bornplace-airforces
    parsers/file-parser

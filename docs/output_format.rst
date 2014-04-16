Output format
=============

This chapter describes output formats for all parsers. Datailed description of
input data aslo included.

Note, that :class:`~il2_mis_parser.parsers.FileParser` is the root parser. It
gets data from all other parsers and organizes it in special manner.

.. note::

    Format of mission files can be very tricky in some sections and original
    key names may be misleading. We made our best to adopt strange things
    for normal humans, but some questions still may appear in your mind.
    Get ready!

.. toctree::
    :maxdepth: 2

    parsers/main_parser
    parsers/season_parser
    parsers/weather_parser
    parsers/file_parser

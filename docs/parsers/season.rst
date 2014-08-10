.. _season-section:

SEASON section
==============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Season>`_

:class:`~il2fb.parsers.mission.parsers.SeasonParser` is responsible for parsing
``SEASON`` section. This section describes mission's date and contains 3 lines
with key-value pairs. Each line contains year, month and day respectively.

Parser returns a dictionary with :class:`datetime.date` object which is
accessible by ``date`` key.

Section example::

    [SEASON]
      Year 1942
      Month 8
      Day 25

Output example:

.. code-block:: python

    {
        'date': datetime.date(1942, 8, 25),
    }

Season parser
=============

.. _season-parser:

:class:`~il2fb.parsers.mission.parsers.SeasonParser` is responsible for parsing
``SEASON`` section. This section describes mission's date and contains 3 lines
with key-value pairs. Each line contains year, month and date respectively.

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

.. _flight-section:

Flight section
============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Flight>`_

:class:`~il2fb.parsers.mission.sections.wing.FlightSectionParser` is
responsible for parsing ``Wing`` section. This section contains a list of
defined air flights.

Each line contains an ID of a single air flight. ID consists of regiment code
or default squadron prefix, squadron index and flight index.

Section example::

  [Wing]
    r0100
    1GvIAP12
    1GvIAP13

Output example:

.. code-block:: python

  {
      'flights': [
          "r0100",
          "1GvIAP12",
          "1GvIAP13",
      ],
  }

The output of the parser is a :class:`dict` with ``flights`` item. It contains
a list of strings, where a each line represents a single flight ID.

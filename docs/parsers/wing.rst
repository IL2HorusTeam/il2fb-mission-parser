.. _wing-section:

Wing section
============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Wing>`_

:class:`~il2fb.parsers.mission.parsers.WingParser` is responsible for parsing
``Wing`` section. This section contains a list of defined air flights.

Each line contains an ID of a single air flight. ID consists of regiment code
or default squadron prefix, squadron number and flight number.

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

The output of the parser is a dictionary with a single item. It is accessible
by ``flights`` key. The value is a list of strings, where a each line
represents a single flight ID.

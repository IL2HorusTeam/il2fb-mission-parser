.. _flight-route-section:

Flight route section
===================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Flight-route>`_

:class:`~il2fb.parsers.mission.parsers.FlightRouteParser` is responsible for
parsing section which provide information about route of a single flight.

Route consists of separate points. Each point is defined on a single line. Lines
starting with ``TRIGGERS`` keyword indicate options for a point define in the
previous line.

The output of the parser is a dictionary with a single item. It is accessible by
``FLIGHT_ID_route`` key, where ``FLIGHT_ID`` is an ID of the flight which is
listed in :ref:`wing-section`. The value is a list of dictionaries, where each
dictionary represents a single point of route.

Section example::

  [3GvIAP01_Way]
    TAKEOFF 193373.53 99288.17 0 0 &0
    TRIGGERS 0 10 20 0
    NORMFLY_401 98616.72 78629.31 500.00 300.00 &0 F2
    TRIGGERS 1 1 25 5 500
    NORMFLY 63028.34 42772.13 500.00 300.00 r0100 1 &0
    GATTACK 99737.30 79106.06 500.00 300.00 0_Chief 0 &0
    GATTACK 74338.61 29746.57 500.00 300.00 4_Static 0 &0
    GATTACK 82387.92 51163.75 500.00 300.00 0_Rocket 0 &0
    LANDING_104 185304.27 54570.12 0 0 &1

Output example:

.. code-block:: python

  {
      '3GvIAP01_route': [
          {
              'type': <constant 'RoutePointTypes.takeoff_normal'>,
              'pos': {
                  'x': 193373.53,
                  'y': 99288.17,
                  'z': 0.0,
              },
              'speed': 0.0,
              'formation': None,
              'radio_silence': False,
              'options': {
                  'delay': 10,
                  'spacing': 20,
              }
          },
          {
              'type': <constant 'RoutePointTypes.patrol_triangle'>,
              'pos': {
                  'x': 98616.72,
                  'y': 78629.31,
                  'z': 500.00,
              },
              'speed': 300.00,
              'formation': Formations.echelon_right,
              'radio_silence': False,
              'options': {
                  'cycles': 1,
                  'timeout': 1,
              },
              'pattern': {
                  'heading': 25,
                  'size': 5,
                  'altitude_difference': 500,
              },
          },
          {
              'type': <constant 'RoutePointTypes.air_attack'>,
              'pos': {
                  'x': 63028.34,
                  'y': 42772.13,
                  'z': 500.00,
              },
              'speed': 300.00,
              'formation': None,
              'target': {
                  'id': "r0100",
                  'route_point': 1,
              },
              'radio_silence': False,
          },
          {
              'type': <constant 'RoutePointTypes.ground_attack'>,
              'pos': {
                  'x': 99737.30,
                  'y': 79106.06,
                  'z': 500.00,
              },
              'speed': 300.00,
              'target': {
                  'id': "0_Chief",
                  'route_point': 0,
              },
              'formation': None,
              'radio_silence': False,
          },
          {
              'type': <constant 'RoutePointTypes.ground_attack'>,
              'pos': {
                  'x': 74338.61,
                  'y': 29746.57,
                  'z': 500.00,
              },
              'speed': 300.00,
              'target': {
                  'id': "4_Static",
                  'route_point': 0,
              },
              'formation': None,
              'radio_silence': False,
          },
          {
              'type': <constant 'RoutePointTypes.ground_attack'>,
              'pos': {
                  'x': 82387.92,
                  'y': 51163.75,
                  'z': 500.00,
              },
              'speed': 300.00,
              'target': {
                  'id': "0_Rocket",
                  'route_point': 0,
              },
              'formation': None,
              'radio_silence': False,
          },
          {
              'type': <constant 'RoutePointTypes.landing_straight'>,
              'pos': {
                  'x': 185304.27,
                  'y': 54570.12,
                  'z': 0.00,
              },
              'speed': 0.00,
              'formation': None,
              'radio_silence': True,
          },
      ]
  }

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Take-off
--------

.. todo::


Normal
------

.. todo::


Attack
------

.. todo::


Landing
-------

.. todo::

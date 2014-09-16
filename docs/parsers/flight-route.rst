.. _flight-route-section:

Flight route section
====================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Flight-route>`_

:class:`~il2fb.parsers.mission.parsers.FlightRouteParser` is responsible for
parsing sections which provide information about route of a single flight.

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
                  'angle': 25,
                  'side_size': 5,
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

There are 4 different types of route points. Each of them has several subtypes.
All of them are described as `route point types`_.

Each point has type, X, Y, and Z coordinates, speed, tells about radio silence
and can have information about air formation.

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Take-off
--------

Take-off includes taxiing and instant takee-off which can have normal, pair and
line plane aligment. The latter two work off as runway take-off; i.e. planes
take-off in the direction of the next waypoint.

.. image:: images/take-off_direction.png
    :alt: Take-off direction
    :align: center

You can also set the distance between planes on the ground. You can also delay
the take-off.

If you set normal takeoff, plane position will be snapped to runway as usual if
the waypoint is less than 1250 m away from the runway. However, flight will
respect any delay that was set.

You can also specify all of those parameters for carrier take-off, but all
except the time delay will be ignored.

Definition example::

  TAKEOFF_003 80156.47 47263.58 0 0 &0
  TRIGGERS 0 2 20 0

Output example:

.. code-block:: python

  {
      'type': <constant 'RoutePointTypes.takeoff_in_line'>,
      'speed': 0.0,
      'pos': {
          'x': 80156.47,
          'y': 47263.58,
          'z': 0.0,
      },
      'formation': None,
      'radio_silence': False,
      'options': {
          'delay': 2,
          'spacing': 20,
      },
  }

Let's examine defined lines:

``TAKEOFF_003``
  Type of route point (take-off in line).

  :Output path: ``type``
  :Output type: complex constant `route point types`_

``80156.47``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``47263.58``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Z coordinate.

  :Output path: ``pos.z``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Speed.

  :Output path: ``speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``&0``
  Tells whether radio silence is enabled for this route point.

  :Output path: ``radio_silence``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``&1``, ``False`` otherwise

.. note::

  ``TRIGGERS`` line is not present for normal take-off

``TRIGGERS``
  Tells that this line contains additional options for previous one.

``0``
  Is not used for take-off.

``2``
  Time delay (in minutes)

  :Output path: ``options.delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``20``
  Distance between aircrafts (in meters).

  :Output path: ``options.spacing``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Is not used for take-off.


Normal
------

Normal flight mode includes cruising, patrolling, and artillery spotter.

Patrolling will establish circling movement in a particular pattern (triangle,
square, etc.). You can adjust orientation of the pattern (direction of first
waypoint in the pattern), side size (in km) and altitude difference from
waypoint to waypoint (climbing or descending pattern).

.. image:: images/flight-pattern.png
    :alt: Flight pattern
    :align: center

If number of cycles or timer are set, they will tell AI when to exit the pattern
and continue with subsequent waypoints. They work as OR logic, so whichever
comes first will make the AI exit the cycle. Zero value for either of the two
parameters means that this trigger is ignored.

Waypoints with type ``artillery spotter`` have such parameters as number of
cycles, timer, direction and side size. However, they do not have any effect.

Definition example::

  NORMFLY_401 98616.72 78629.31 500.00 300.00 &0 F2
  TRIGGERS 1 1 25 5 500

Output example:

.. code-block:: python

  {
      'type': <constant 'RoutePointTypes.patrol_triangle'>,
      'pos': {
          'x': 98616.72,
          'y': 98616.72,
          'z': 500.00,
      },
      'speed': 300.00,
      'formation': <constant 'Formations.echelon_right'>,
      'radio_silence': False,
      'options': {
          'cycles': 1,
          'timeout': 1,
      },
      'pattern': {
          'angle': 25,
          'side_size': 5,
          'altitude_difference': 500,
      },
  }

Let's examine defined lines:

``NORMFLY_401``
  Type of route point (patrolling using triangle pattern).

  :Output path: ``type``
  :Output type: complex constant `route point types`_

``98616.72``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``98616.72``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``500.00``
  Z coordinate.

  :Output path: ``pos.z``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``300.00``
  Speed.

  :Output path: ``speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``&0``
  Tells whether radio silence is enabled for this route point.

  :Output path: ``radio_silence``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``&1``, ``False`` otherwise

``F2``
  Type of air formation (echelon right).

  :Output path: ``formation``
  :Output type: complex constant `air formations`_ or ``None``

.. note::

  ``TRIGGERS`` line is not present for normal flight

``TRIGGERS``
  Tells that this line contains additional options for previous one.

``1``
  Number of cycles to repeat.

  :Output path: ``options.cycles``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``2``
  Timeout (in minutes).

  :Output path: ``options.timeout``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``25``
  Angle of pattern (in degrees).

  :Output path: ``pattern.angle``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``5``
  Size of pattern's side (in km).

  :Output path: ``pattern.side_size``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``500``
  Altitude difference (in meters).

  :Output path: ``pattern.altitude_difference``
  :Output type: :class:`int`
  :Output value: original value converted to integer number


Attack
------

There are 2 kinds of way points which tell AI to attack other units: attack
ground units and attack air units. Both of them have same parameters, but
different types. Former one is defined as ``GATTACK`` and the latter as
``NORMFLY``.

.. note::

  Yes, waypoints which tell AI to attack air units has type ``NORMFLY``, just
  if it is a normal flight point. This is misleading, so `route point types`_
  define this type as ``X_AIR_ATTACK``, where ``X`` tells that this is a fake
  type.

A target is any destroyable object: aircraft, moving vehicle, artillery,
rocket, static object, etc.

Definition example::

  NORMFLY 63028.34 42772.13 500.00 300.00 r0100 1 &0
  GATTACK 99737.30 79106.06 500.00 300.00 0_Chief 0 &0

Output example:

.. code-block:: python

  [
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
  ]

Let's examine second line:

``GATTACK``
  Type of route point (attack ground unit).

  :Output path: ``type``
  :Output type: complex constant `route point types`_

``99737.30``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``79106.06``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``500.00``
  Z coordinate.

  :Output path: ``pos.z``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``300.00``
  Speed.

  :Output path: ``speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0_Chief``
  ID of the unit to attack.

  :Output path: ``target.id``
  :Output type: :class:`str`
  :Output value: original string value

``0``
  Waypoint number of the unit to attack (not relevant for static objects).

  :Output path: ``target.route_point``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``&0``
  Tells whether radio silence is enabled for this route point.

  :Output path: ``radio_silence``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``&1``, ``False`` otherwise


Landing
-------

For landing you can choose one of the 5 landing patterns:

* right;
* left;
* short right;
* short left;
* straight in.

``Left`` pattern is the default pattern used in versions of the game before
4.12. The ``straight in`` landing is rather tricky to get correct and can cause
planes to crash into each other. You can set several flights with different
pattern to land on the same airfield. AI seems to handle this fairly well, but
there are no guarantees that they will not collide. All settings are ignored if
the flight is landing on a carrier (i.e. they use default ``left`` pattern).

Definition example::

  LANDING_104 185304.27 54570.12 0 0 &1

Output example:

.. code-block:: python

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
  }

Description:

``LANDING_104``
  Type of route point (landing using ``straight`` pattern).

  :Output path: ``type``
  :Output type: complex constant `route point types`_

``185304.27``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``54570.12``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Z coordinate.

  :Output path: ``pos.z``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Speed.

  :Output path: ``speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``&1``
  Tells whether radio silence is enabled for this route point.

  :Output path: ``radio_silence``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``&1``, ``False`` otherwise


.. _route point types: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/flight.py#L20
.. _air formations: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/flight.py#L10

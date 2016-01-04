.. _flight-route-section:

Flight route section
====================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Flight-route>`_

:class:`~il2fb.parsers.mission.sections.wing.FlightRouteSectionParser`
is responsible for parsing sections which provide information about route of a
single flight.

Route consists of separate points. Each point is defined on a single line.
Lines which start with ``TRIGGERS`` keyword indicate options for a point
which was defined in the previous line.

The output of the parser is a dictionary with a single item. It is accessible
by ``FLIGHT_ID_route`` key, where ``FLIGHT_ID`` is an ID of the flight which is
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
      'flight_route_3GvIAP01': [
          FlightRouteTakeoffPoint(
              type=RoutePointTypes.takeoff_normal,
              pos=Point3D(193373.53, 99288.17, 0.0),
              speed=0.0,
              formation=None,
              radio_silence=False,
              delay=10,
              spacing=20,
          ),
          FlightRoutePatrolPoint(
              type=RoutePointTypes.patrol_triangle,
              pos=Point3D(98616.72, 78629.31, 500.00),
              speed=300.00,
              formation=Formations.echelon_right,
              radio_silence=False,
              patrol_cycles=1,
              patrol_timeout=1,
              pattern_angle=25,
              pattern_side_size=5,
              pattern_altitude_difference=500,
          ),
          FlightRouteAttackPoint(
              type=RoutePointTypes.air_attack,
              pos=Point3D(63028.34, 42772.13, 500.00),
              speed=300.00,
              formation=None,
              radio_silence=False,
              target_id='r0100',
              target_route_point=1,
          ),
          FlightRouteAttackPoint(
              type=RoutePointTypes.ground_attack,
              pos=Point3D(99737.30, 79106.06, 500.00),
              speed=300.00,
              formation=None,
              radio_silence=False,
              target_id='0_Chief',
              target_route_point=0,
          ),
          FlightRouteAttackPoint(
              type=RoutePointTypes.ground_attack,
              pos=Point3D(74338.61, 29746.57, 500.00),
              speed=300.00,
              formation=None,
              radio_silence=False,
              target_id='4_Static',
              target_route_point=0,
          ),
          FlightRouteAttackPoint(
              type=RoutePointTypes.ground_attack,
              pos=Point3D(82387.92, 51163.75, 500.00),
              speed=300.00,
              formation=None,
              radio_silence=False,
              target_id='0_Rocket',
              target_route_point=0,
          ),
          FlightRoutePoint(
              type=RoutePointTypes.landing_straight,
              pos=Point3D(185304.27, 54570.12, 0.00),
              speed=0.00,
              formation=None,
              radio_silence=True,
          ),
      ]
  }


There are 4 different types of route points. Each of them has several subtypes.
All of them are described as `types of route points`_.

Each point has type, X, Y, and Z coordinates and speed. They also tell about
radio silence and can have information about air formation.

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Take-off
--------

Take-off includes taxiing and instant take-off. Aircrafts in take-off can be
aligned as ``normal``, ``pair`` or ``inline``. The latter two work off as
runway take-off; i.e. planes take-off in the direction of the next waypoint.

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

  FlightRouteTakeoffPoint(
      type=RoutePointTypes.takeoff_in_line,
      pos=Point3D(80156.47, 47263.58, 0.0),
      speed=0.0,
      formation=None,
      radio_silence=False,
      delay=2,
      spacing=20,
  )

Take-off points are defined by `FlightRouteTakeoffPoint data structure`_.

Let's examine defined lines:

``TAKEOFF_003``
  Type of route point (inline take-off).

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

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``20``
  Distance between aircrafts (in meters).

  :Output path: ``spacing``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Is not used for take-off.


Normal flight
-------------

Normal flight mode includes ``cruising``, ``patrolling``, and
``artillery spotter``.

Patrolling will establish circling movement in a particular pattern (triangle,
square, etc.). You can adjust orientation of the pattern (direction of first
waypoint in the pattern), side size (in km) and altitude difference from
waypoint to waypoint (climbing or descending pattern).

.. image:: images/flight-pattern.png
    :alt: Flight pattern
    :align: center

If number of cycles or timer are set, they will tell AI when to exit the
pattern and continue with subsequent waypoints. They work as OR logic, so
whichever comes first will make the AI exit the cycle. Zero value for either of
the two parameters means that this trigger is ignored.

Waypoints with type ``artillery spotter`` have such parameters as: number of
cycles, timer, direction and side size. However, they do not have any effect.

Definition example::

  NORMFLY_401 98616.72 78629.31 500.00 300.00 &0 F2
  TRIGGERS 1 1 25 5 500

Output example:

.. code-block:: python

  FlightRoutePatrolPoint(
      type=RoutePointTypes.patrol_triangle,
      pos=Point3D(98616.72, 98616.72, 500.00),
      speed=300.00,
      formation=Formations.echelon_right,
      radio_silence=False,
      patrol_cycles=1,
      patrol_timeout=1,
      pattern_angle=25,
      pattern_side_size=5,
      pattern_altitude_difference=500,
  )

Patrol points are defined by `FlightRoutePatrolPoint data structure`_. In
other cases (normal flight and artillery spotter)
`FlightRoutePoint data structure`_ is used.

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

``1`` [1]_
  Number of cycles to repeat.

  :Output path: ``patrol_cycles``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``2`` [1]_
  Timeout (in minutes).

  :Output path: ``patrol_timeout``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``25`` [1]_
  Angle of pattern (in degrees).

  :Output path: ``pattern_angle``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``5`` [1]_
  Size of pattern's side (in km).

  :Output path: ``pattern_side_size``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``500`` [1]_
  Altitude difference (in meters).

  :Output path: ``pattern_altitude_difference``
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
      FlightRouteAttackPoint(
          type=RoutePointTypes.air_attack,
          pos=Point3D(63028.34, 42772.13, 500.00),
          speed=300.00,
          formation=None,
          radio_silence=False,
          target_id='r0100',
          target_route_point=1,
      ),
      FlightRouteAttackPoint(
          type=RoutePointTypes.ground_attack,
          pos=Point3D(99737.30, 79106.06, 500.00),
          speed=300.00,
          formation=None,
          radio_silence=False,
          target_id='0_Chief',
          target_route_point=0,
      ),
  ]


Attack points are defined by `FlightRouteAttackPoint data structure`_.

Let's examine the second line:

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

  :Output path: ``target_id``
  :Output type: :class:`str`
  :Output value: original string value

``0``
  Waypoint number of the unit to attack (not relevant for static objects).

  :Output path: ``target_route_point``
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

  FlightRoutePoint(
      type=RoutePointTypes.landing_straight,
      pos=Point3D(185304.27, 54570.12, 0.00),
      speed=0.00,
      formation=None,
      radio_silence=True,
  )


Landing points do not have special parameters and they are defined by
`FlightRoutePoint data structure`_.

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


---------

Footnotes:

.. [#] For patrol points only.

.. _FlightRoutePoint data structure: https://github.com/IL2HorusTeam/il2fb-mission-parser/blob/master/il2fb/parsers/mission/structures.py#L187
.. _FlightRouteTakeoffPoint data structure: https://github.com/IL2HorusTeam/il2fb-mission-parser/blob/master/il2fb/parsers/mission/structures.py#L204
.. _FlightRoutePatrolPoint data structure: https://github.com/IL2HorusTeam/il2fb-mission-parser/blob/master/il2fb/parsers/mission/structures.py#L215
.. _FlightRouteAttackPoint data structure: https://github.com/IL2HorusTeam/il2fb-mission-parser/blob/master/il2fb/parsers/mission/structures.py#L233

.. _route point types: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/flight.py#L21
.. _types of route points: `route point types`_
.. _air formations: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/flight.py#L11

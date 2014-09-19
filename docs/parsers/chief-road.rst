.. _chief-road-section:

Chief Road section
==================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Chief_Road>`_

:class:`~il2fb.parsers.mission.parsers.ChiefRoadParser` is responsible for
parsing ``N_Chief_Road`` section. Every object listed in :ref:`chiefs-section`
has own route described in own ``N_Chief_Road`` section, where ``N`` is the
sequence number within ``Chiefs`` section.

Section example::

    [0_Chief_Road]
      21380.02 41700.34 120.00 10 2 3.055555582046509
      21500.00 41700.00 120.00
      50299.58 35699.85 120.00 0 3 2.6388890743255615
      60284.10 59142.93 120.00
      84682.13 98423.69 120.00


Output example:

.. code-block:: python

    {
        '0_chief_route': [
            {
                'is_check_point': True,
                'pos': {
                    'x': 21380.02,
                    'y': 41700.34,
                },
                'section_length': 2,
                'speed': 3.055555582046509,
                'delay': 10,
            },
            {
                'is_check_point': False,
                'pos': {
                    'x': 21500.00,
                    'y': 41700.00,
                },
            },
            {
                'is_check_point': True,
                'pos': {
                    'x': 50299.58,
                    'y': 35699.85,
                },
                'section_length': 3,
                'speed': 2.6388890743255615,
                'delay': 0,
            },
            {
                'is_check_point': False,
                'pos': {
                    'x': 60284.10,
                    'y': 59142.93,
                },
            },
            {
                'is_check_point': False,
                'pos': {
                    'x': 84682.13,
                    'y': 98423.69,
                },
            },
        ],
    }

**Description**:

Each line in ``N_Chief_Road`` section describes a single waypoint. There are
two types of waypoints: created by user and created automatically by full
mission editor.

The output of the parser is a dictionary with a single item. The key is the
name of the section and the value is a list of dictionaries. Each dictionary
represents a single waypoint.

Manually created waipoints have 6 parameters, while auto-created ones have only
3 of them. The last waypoint always has 3 parameters, and it is allways defined
by user. So, don't get mislead.

The purpose of intermediate auto-created waypoints is to create the most
efficient route:

#. vehicles tend to move by roads, by bridges, and by the most flat terrains;
#. trains can move only by rails; intermediate points are created in the points
   where the direction is changed;
#. ships tend to follow coastlines and river banks if they come to them close
   enough.

Let's examine a description of a manual waypoint which has all parameters
included::

    21380.02 41700.34 120.00 10 2 3.055555582046509

``21380.02``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``41700.34``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``120.00``
  This is the really strange parameter. The true meaning is not known, but its
  value depends on the type of surface the point is located on. Also, the
  value is specific for different types of units:

  #. vehicles: the value for all manual waypoints is set to ``120.0``.
     the value for auto-created waypoint can be set to ``20.0`` or ``120.0``.
     The former value tells that the point belongs to a road. The latter one
     tells that the point is located in the off-road. Negative values tell
     about start or end of a bridge. Usually, negative values come in pairs.
  #. trains: all waypoints have the value of ``20.0``. This means that trains
     can move only by railways. Negative values tell about start or end of a
     bridge. Usually, negative values come in pairs.
  #. ships: all waypoints have the value of ``120.0``. This means that ships
     can move only by water.

  :Output path: this value is not present in the output.

``10``
  Delay (in minutes): this parameter tells how much a unit have to wait until
  it starts movement to the next user-defined point.

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``2``
  Section length. Here ``section`` means current waypoint, next user-defined
  point and all intermediate points between them.

  :Output path: ``section_length``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``3.055555582046509``
  The speed of the unit at the current point of the route. This parameter is
  set automatically by full missions editor depending on the unit type.

  :Output path: ``speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

-----

  We decided to mark each user-defined waypoint as a check point (except the
  last one).

  :Output path: ``is_check_point``
  :Output type: :class:`bool`
  :Output value:
    ``True`` if a point defines start of a section, ``False`` if it is an
    intermediate point or the last point


.. _target-section:

Target section
===============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Target>`_

:class:`~il2fb.parsers.mission.parsers.TargetParser` is responsible for
parsing ``Target`` section. Each line of this section describes a single
mision target.

Section example::

  [Target]
    3 1 1 50 500 133978 87574 1150
    3 0 1 40 501 134459 85239 300 0 1_Chief 134360 85346

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.recon'>,
              'priority': <constant 'TargetPriorities.secondary'>,
              'in_sleep_mode': True,
              'delay': 50,
              'requires_landing': False,
              'pos': {
                  'x': 133978.0,
                  'y': 87574.0,
              },
              'radius': 1150,
          },
          {
              'type': <constant 'TargetTypes.recon'>,
              'priority': <constant 'TargetPriorities.primary'>,
              'in_sleep_mode': True,
              'delay': 40,
              'requires_landing': True,
              'pos': {
                  'x': 134459.0,
                  'y': 85239.0,
              },
              'radius': 300,
              'object': {
                  'waypoint': 0,
                  'id': '1_Chief',
                  'pos': {
                      'x': 134360.0,
                      'y': 85346.0,
                  },
              },
          },
      ],
  }

The output of the parser is a dictionary with a single item. It is accessible
by ``targets`` key. The value is a list of dictionaries. Each dictionary
represents a single target.

There are 8 different types of targets and 3 types of target priorities. Some
different types of targets have identical sets of parameters.

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Destroy
-------

Definition example::

  0 0 0 0 500 90939 91871 0 1 10_Chief 91100 91500

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.destroy'>,
              'priority': <constant 'TargetPriorities.primary'>,
              'in_sleep_mode': False,
              'delay': 0,
              'destruction_level': 50,
              'pos': {
                  'x': 90939.0,
                  'y': 91871.0,
              },
              'object': {
                  'waypoint': 1,
                  'id': '10_Chief',
                  'pos': {
                      'x': 91100.0,
                      'y': 91500.0,
                  },
              },
          },
      ],
  }

``0``
  Target type (destroy).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``0``
  Target priority (primary).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``0``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``0``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``500``
  Destruction level multiplied by 10.

  :Output path: ``destruction_level``
  :Output type: :class:`int`
  :Output value: original value converted to integer number and divided by 10

``90939``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``91871``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Is not used for this target type.

``1``
  Waypoint number of the object which must be destroyed.

  :Output path: ``object.waypoint``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``10_Chief``
  ID of the object which must be destroyed.

  :Output path: ``object.id``
  :Output type: :class:`str`
  :Output value: original string value

``91100``
  X coordinate of the object which must be destroyed.

  :Output path: ``object.pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``91500``
  Y coordinate of the object which must be destroyed.

  :Output path: ``object.pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


Destroy area
------------

Definition example::

  1 1 1 60 750 133960 87552 1350

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.destroy_area'>,
              'priority': <constant 'TargetPriorities.secondary'>,
              'in_sleep_mode': True,
              'delay': 60,
              'destruction_level': 75,
              'pos': {
                  'x': 133960.0,
                  'y': 87552.0,
              },
              'radius': 1350,
          },
      ],
  }

``1``
  Target type (destroy area).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``1``
  Target priority (secondary).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``60``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``750``
  Destruction level multiplied by 10.

  :Output path: ``destruction_level``
  :Output type: :class:`int`
  :Output value: original value converted to integer number and divided by 10

``133960``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``87552``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``1350``
  Area radius.

  :Output path: ``radius``
  :Output type: :class:`int`
  :Output value: original value converted to integer number


Destroy bridge
--------------

Definition example::

  2 2 1 30 500 135786 84596 0 0  Bridge84 135764 84636

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.destroy_bridge'>,
              'priority': <constant 'TargetPriorities.hidden'>,
              'in_sleep_mode': True,
              'delay': 30,
              'pos': {
                  'x': 135786.0,
                  'y': 84596.0,
              },
              'object': {
                  'id': 'Bridge84',
                  'pos': {
                      'x': 135764.0,
                      'y': 84636.0,
                  },
              },
          },
      ],
  }

``2``
  Target type (destroy bridge).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``2``
  Target priority (hidden).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``30``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``500``
  Is not used for this target type.

``133960``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``87552``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Is not used for this target type.

``0``
  Is not used for this target type.

``Bridge84``
  ID of the bridge which must be destroyed.

  :Output path: ``object.id``
  :Output type: :class:`str`
  :Output value: original string value

``135764``
  X coordinate of the bridge which must be destroyed.

  :Output path: ``object.pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``84636``
  Y coordinate of the bridge which must be destroyed.

  :Output path: ``object.pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


Recon
-----

There are 2 possible definitions::

  3 1 1 50 500 133978 87574 1150
  3 0 1 40 501 134459 85239 300 0 1_Chief 134360 85346

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.recon'>,
              'priority': <constant 'TargetPriorities.secondary'>,
              'in_sleep_mode': True,
              'delay': 50,
              'requires_landing': False,
              'pos': {
                  'x': 133978.0,
                  'y': 87574.0,
              },
              'radius': 1150,
          },
          {
              'type': <constant 'TargetTypes.recon'>,
              'priority': <constant 'TargetPriorities.primary'>,
              'in_sleep_mode': True,
              'delay': 40,
              'requires_landing': True,
              'pos': {
                  'x': 134459.0,
                  'y': 85239.0,
              },
              'radius': 300,
              'object': {
                  'waypoint': 0,
                  'id': '1_Chief',
                  'pos': {
                      'x': 134360.0,
                      'y': 85346.0,
                  },
              },
          },
      ],
  }

Let's examine second definition:

``3``
  Target type (recon).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``0``
  Target priority (primary).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``40``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``501``
  Tells whether you need to land near the target to succeed.

  :Output path: ``requires_landing``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``501``, ``False`` otherwise

``134459``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``87574``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``300``
  Maximal distance to target if you need to land.

  :Output path: ``radius``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Waypoint number of the object which you need to recon.

  :Output path: ``object.waypoint``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``1_Chief``
  ID of the object which you need to recon.

  :Output path: ``object.id``
  :Output type: :class:`str`
  :Output value: original string value

``134360``
  X coordinate of the object which you need to recon.

  :Output path: ``object.pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``85346``
  Y coordinate of the object which you need to recon.

  :Output path: ``object.pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


Escort
------

Definition example::

  4 0 1 10 750 134183 85468 0 1 r0100 133993 85287

Output example:

.. code-block:: python

  {
    'targets': [
        {
            'type': <constant 'TargetTypes.escort'>,
            'priority': <constant 'TargetPriorities.primary'>,
            'in_sleep_mode': True,
            'delay': 10,
            'destruction_level': 75,
            'pos': {
                'x': 134183.0,
                'y': 85468.0,
            },
            'object': {
                'waypoint': 1,
                'id': 'r0100',
                'pos': {
                    'x': 133993.0,
                    'y': 85287.0,
                },
            },
        },
    ],
}

``4``
  Target type (escort).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``0``
  Target priority (primary).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``10``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``750``
  Destruction level multiplied by 10.

  :Output path: ``destruction_level``
  :Output type: :class:`int`
  :Output value: original value converted to integer number and divided by 10

``134183``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``91871``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Is not used for this target type.

``1``
  Waypoint number of the flight which must be escorted.

  :Output path: ``object.waypoint``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``r0100``
  ID of the flight which must be escorted.

  :Output path: ``object.id``
  :Output type: :class:`str`
  :Output value: original string value

``133993``
  X coordinate of the flight which must be escorted.

  :Output path: ``object.pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``85287``
  Y coordinate of the flight which must be escorted.

  :Output path: ``object.pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


Cover
-----

Definition example::

  5 1 1 20 250 132865 87291 0 1 1_Chief 132866 86905

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.cover'>,
              'priority': <constant 'TargetPriorities.secondary'>,
              'in_sleep_mode': True,
              'delay': 20,
              'destruction_level': 25,
              'pos': {
                  'x': 132865.0,
                  'y': 87291.0,
              },
              'object': {
                  'waypoint': 1,
                  'id': '1_Chief',
                  'pos': {
                      'x': 132866.0,
                      'y': 86905.0,
                  },
              },
          },
      ],
  }


``5``
  Target type (cover).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``1``
  Target priority (secondary).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``20``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``250``
  Destruction level multiplied by 10.

  :Output path: ``destruction_level``
  :Output type: :class:`int`
  :Output value: original value converted to integer number and divided by 10

``132865``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``87291``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Is not used for this target type.

``1``
  Waypoint number of the object which must be covered.

  :Output path: ``object.waypoint``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``1_Chief``
  ID of the object which must be covered.

  :Output path: ``object.id``
  :Output type: :class:`str`
  :Output value: original string value

``132866``
  X coordinate of the object which must be covered.

  :Output path: ``object.pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``86905``
  Y coordinate of the object which must be covered.

  :Output path: ``object.pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


Cover area
----------

Definition example::

  6 1 1 30 500 134064 88188 1350

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.cover_area'>,
              'priority': <constant 'TargetPriorities.secondary'>,
              'in_sleep_mode': True,
              'delay': 30,
              'destruction_level': 50,
              'pos': {
                  'x': 134064.0,
                  'y': 88188.0,
              },
              'radius': 1350,
          },
      ],
  }

``6``
  Target type (cover area).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``1``
  Target priority (secondary).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``30``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``500``
  Destruction level multiplied by 10.

  :Output path: ``destruction_level``
  :Output type: :class:`int`
  :Output value: original value converted to integer number and divided by 10

``134064``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``88188``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``1350``
  Area radius.

  :Output path: ``radius``
  :Output type: :class:`int`
  :Output value: original value converted to integer number


Cover bridge
------------

Definition example::

  7 2 1 30 500 135896 84536 0 0  Bridge84 135764 84636

Output example:

.. code-block:: python

  {
      'targets': [
          {
              'type': <constant 'TargetTypes.cover_bridge'>,
              'priority': <constant 'TargetPriorities.hidden'>,
              'in_sleep_mode': True,
              'delay': 30,
              'pos': {
                  'x': 135896.0,
                  'y': 84536.0,
              },
              'object': {
                  'id': 'Bridge84',
                  'pos': {
                      'x': 135764.0,
                      'y': 84636.0,
                  },
              },
          },
      ],
  }

``7``
  Target type (cover bridge).

  :Output path: ``type``
  :Output type: complex `target type`_ constant

``2``
  Target priority (hidden).

  :Output path: ``priority``
  :Output type: complex `target priority`_ constant

``1``
  Tells whether sleep mode is turned on.

  :Output path: ``in_sleep_mode``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``30``
  Delay (in minutes).

  :Output path: ``delay``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``500``
  Is not used for this target type.

``135896``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``84536``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Is not used for this target type.

``0``
  Is not used for this target type.

``Bridge84``
  ID of the bridge which must be covered.

  :Output path: ``object.id``
  :Output type: :class:`str`
  :Output value: original string value

``135764``
  X coordinate of the bridge which must be covered.

  :Output path: ``object.pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``84636``
  Y coordinate of the bridge which must be covered.

  :Output path: ``object.pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


.. _target type: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/targets.py#L10
.. _target priority: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/targets.py#L21

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
              'waiting_time': 50,
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
              'waiting_time': 40,
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

The output of the parser is a dictionary with a single item. It it accessible by
``targets`` key. The value is a list of dictionaries. Each dictionary represents
a single target.

There are 8 different types of targets and 3 types of targer priorities. Some
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
              'waiting_time': 0,
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
  Waiting time (in minutes).

  :Output path: ``waiting_time``
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

todo


Destroy bridge
--------------

todo


Recon
-----

todo


Escort
------

todo


Cover
-----

todo


Cover area
----------

todo


Cover bridge
------------

todo


.. _target type: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/targets.py#L10
.. _target priority: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/targets.py#L21

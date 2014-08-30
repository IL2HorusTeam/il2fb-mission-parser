.. _nstationary-section:

NStationary section
===================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-NStationary>`_

:class:`~il2fb.parsers.mission.parsers.NStationaryParser` is responsible for
parsing ``NStationary`` section. Each line of this section describes a single
stationary object (except houses).

Section example::

  [NStationary]
    0_Static vehicles.stationary.Stationary$Wagon1 1 152292.72 89662.80 360.00 0.0
    1_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1
    2_Static vehicles.planes.Plane$I_16TYPE24 2 134146.89 88005.43 336.92 0.0 de 2 1.0 I-16type24_G1_RoW3.bmp 1
    3_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4


Output example:

.. code-block:: python

  {
      'stationary': [
          {
              'belligerent': <constant 'Belligerents.red'>,
              'id': '0_Static',
              'code': 'Wagon1',
              'pos': {
                  'x': 152292.72,
                  'y': 89662.80,
              },
              'rotation_angle': 360.00,
              'type': <constant 'UnitTypes.stationary'>,
          },
          {
              'belligerent': <constant 'Belligerents.blue'>,
              'id': '1_Static',
              'code': 'SdKfz251',
              'use_spotter': True,
              'pos': {
                  'x': 31333.62,
                  'y': 90757.91,
              },
              'rotation_angle': 600.29,
              'range': 0,
              'skill': <constant 'Skills.average'>,
              'type': <constant 'UnitTypes.artillery'>,
              'awakening_time': 0.0,
          },
          {
              'air_force': <constant 'AirForces.luftwaffe'>,
              'allows_spawning': True,
              'belligerent': <constant 'Belligerents.blue'>,
              'id': '3_Static',
              'code': 'I_16TYPE24',
              'show_markings': True,
              'pos': {
                  'x': 134146.89,
                  'y': 88005.43,
              },
              'rotation_angle': 336.92,
              'restorable': True,
              'skin': 'I-16type24_G1_RoW3.bmp',
              'type': <constant 'UnitTypes.airplane'>,
          },
          {
              'belligerent': <constant 'Belligerents.red'>,
              'id': '9_Static',
              'code': 'G5',
              'recharge_time': 1.4,
              'pos': {
                  'x': 83759.05,
                  'y': 115021.15,
              },
              'rotation_angle': 360.00,
              'skill': <constant 'Skills.ace'>,
              'awakening_time': 60,
              'type': <constant 'UnitTypes.ship'>,
          },
      ],
  }


The output of the parser is a dictionary with a single item. It is accessible by
``stationary`` key. The value is a list of dictionaries. Each dictionary
represents a single object.

Set of parameters may differ for different unit types:

#. all objects have at least 7 parameters;
#. artillery has 3 own extra parameters;
#. airplanes have 5 own extra parameters;
#. ships have 3 own extra parameters.

Let's examine all of them.

Common parameters
-----------------

Definition example::

  0_Static vehicles.stationary.Stationary$Wagon1 1 152292.72 89662.80 360.00 0.0

``0_Static``
  Object ID which is given by full mission editor. Contains ``Static`` word
  prefixed by a sequence number.

  :Output path: ``id``
  :Output type: :class:`str`
  :Output value: original string value

``vehicles.stationary.Stationary$Wagon1``
  Unit type (``stationary``) and code name (``Wagon1``).

  :Output path: ``type``
  :Output type: complex `unit type`_ constant

  ..

  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value

``1``
  Code number of army the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant

``152292.72``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``89662.80``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``360.00``
  Angle of rotation.

  :Output path: ``rotation_angle``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0.0``
  This parameter is not used in common case. It has a meaning only for artillery
  objects (see below).

Artillery-specific parameters
-----------------------------

Definition example::

  1_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1

``0.0``
  Time of awakening (in minutes): it's a time which will pass since enemy unit
  enters object's range till object will react on that unit.

  :Output path: ``awakening_time``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``0``
  Range of fire.

  :Output path: ``range``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``1``
  Skill level of gunners.

  :Output path: ``skill``
  :Output type: complex `skills`_ constant

``1``
  Tells whether to use spotter or not.

  :Output path: ``use_spotter``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

Airplanes-specific parameters
-----------------------------

Definition example::

  2_Static vehicles.planes.Plane$I_16TYPE24 2 134146.89 88005.43 336.92 0.0 de 2 1.0 I-16type24_G1_RoW3.bmp 1

``de``
  Air force code name.

  :Output path: ``air_force``
  :Output type: complex `air forces`_ constant
  :Default: ``null`` - VVS RKKA

``2``
  Polysemantic parameter which can have next values:


  .. list-table::
     :widths: 20 80
     :header-rows: 1

     * - Value
       - Meaning
     * - 0
       - Using this airplane by humans is **not allowed**
     * - 1
       - Using this airplane by humans is **allowed**
     * - 2
       - Using this airplane by humans is **allowed**, object will be restored
         after successfull landing

  :Output path: ``allows_spawning``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1`` or ``2``, ``False`` otherwise

  ..

  :Output path: ``restorable``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``2``, ``False`` otherwise


``1.0``
  Not used.

``I-16type24_G1_RoW3.bmp``
  Skin name.

  :Output path: ``skin``
  :Output type: :class:`str`
  :Output value: original string value
  :Default: ``null``

``1``
  Show markings or not.

  :Output path: ``show_markings``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise


Ships-specific parameters
-------------------------

Definition example::

  3_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4

``60``
  Time of awakening (in minutes): it's a time which will pass since enemy unit
  enters ship's range till ship will react on that unit.

  :Output path: ``awakening_time``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``3``
  Skill level of gunners.

  :Output path: ``skill``
  :Output type: complex `skills`_ constant

``1.4``
  Recharge time (in minutes) of anti-aircraft guns of the ship.

  :Output path: ``recharge_time``
  :Output type: :class:`float`
  :Output value: original value converted to float number


.. _unit type: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L34
.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L17
.. _skills: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L27
.. _air forces: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L89

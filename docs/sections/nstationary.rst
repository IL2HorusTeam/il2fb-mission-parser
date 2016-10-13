.. _nstationary-section:

NStationary section
===================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-NStationary>`_

:class:`~il2fb.parsers.mission.sections.nstationary.NStationarySectionParser`
is responsible for parsing ``NStationary`` section. Each line of this section
describes a single stationary object (except buildings and houses).

Section example::

  [NStationary]
    0_Static vehicles.stationary.Stationary$Wagon1 1 152292.72 89662.80 360.00 0.0
    1_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1
    2_Static vehicles.planes.Plane$I_16TYPE24 1 134146.89 88005.43 336.92 0.0 null 2 1.0 I-16type24_G1_RoW3.bmp 1
    3_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4


Output example:

.. code-block:: python

  {
      'stationary': [
          StationaryObject(
              belligerent=Belligerents.red,
              id='0_Static',
              code='Wagon1',
              pos=Point2D(152292.72, 89662.80),
              rotation_angle=0.00,
              type=UnitTypes.stationary,
          ),
          StationaryArtillery(
              id='1_Static',
              belligerent=Belligerents.blue,
              code='SdKfz251',
              pos=Point2D(31333.62, 90757.91),
              rotation_angle=240.29,
              type=UnitTypes.artillery,
              awakening_time=0.0,
              range=0,
              skill=Skills.average,
              use_spotter=True,
          ),
          StationaryAircraft(
              id='2_Static',
              code='I_16TYPE24',
              belligerent=Belligerents.red,
              pos=Point2D(134146.89, 88005.43),
              rotation_angle=336.92,
              type=UnitTypes.aircraft,
              air_force=AirForces.vvs_rkka,
              allows_spawning=True,
              show_markings=True,
              is_restorable=True,
              skin="I-16type24_G1_RoW3.bmp",
          ),
          StationaryShip(
              belligerent=Belligerents.red,
              id='9_Static',
              code='G5',
              recharge_time=1.4,
              pos=Point2D(83759.05, 115021.15),
              rotation_angle=0.00,
              skill=Skills.ace,
              type=UnitTypes.ship,
              awakening_time=60.0,
          ),
      ],
  }


The output of the parser is a dictionary with  ``stationary`` item which
contains a list of stationary objects.

Set of parameters may differ for different `types of units`_:

#. all objects have at least 7 parameters;
#. artillery has 3 own extra parameters;
#. aircrafts have 5 own extra parameters;
#. ships have 3 own extra parameters.

Let's examine all of them:

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Usual objects
-------------

Usual objects — these are all objects which have usual set of parameters,
namely: ballons, lights, radio stations, trains, vehicles and so on.

We use :class:`~il2fb.parsers.mission.sections.nstationary.StationaryObject`
data structure to store information about such objects.

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
  :Output value: original value converted to float number and taken modulo 360

``0.0``
  This parameter is not used by usual objects. It has a meaning only for
  artillery objects (see below).


Artillery
---------

Artillery has all the same parameters as usual objects. Also artillery in new
versions of game has some extra parameters which are described below.

We use :class:`~il2fb.parsers.mission.sections.nstationary.StationaryArtillery`
data structure to store information about artillery.

Definition example::

  1_Static vehicles.artillery.Artillery$SdKfz251 2 31333.62 90757.91 600.29 0.0 0 1 1

``0.0``
  Time of awakening (in minutes): it's a time which will pass since enemy unit
  enters object's range till object will react on that unit.

  :Output path: ``awakening_time``
  :Output type: :class:`float`
  :Output value:
    original value converted to float number
    (``0.0`` for objects from old game versions)

``0``
  Range of fire.

  :Output path: ``range``
  :Output type: :class:`int`
  :Output value:
    original value converted to integer number
    (``0`` for objects from old game versions)

``1``
  Skill level of gunners.

  :Output path: ``skill``
  :Output type:
    complex `skills`_ constant (``None`` for objects from old game versions)

``1``
  Tells whether to use spotter or not.

  :Output path: ``use_spotter``
  :Output type: :class:`bool`
  :Output value:
    ``True`` if ``1``, ``False`` otherwise
    (``False`` for objects from old game versions)


Aircrafts
---------

Aircrafts have all the same parameters as usual objects. Also aircrafts in new
versions of game have some extra parameters which are described below.

We use :class:`~il2fb.parsers.mission.sections.nstationary.StationaryAircraft`
data structure to store information about aircrafts.

Definition example::

  2_Static vehicles.planes.Plane$I_16TYPE24 2 134146.89 88005.43 336.92 0.0 de 2 1.0 I-16type24_G1_RoW3.bmp 1

``null``
  Code name of the air force. E.g., ``de`` or ``fr``. For some unknown reason
  air force of USSR has ``null`` code name in ``NStationary`` section.

  :Output path: ``air_force``
  :Output type: complex `air forces`_
  :Output value: constant (``None`` for objects from old game versions)

``2``
  Polysemantic parameter which can have next values:

  .. list-table::
     :widths: 20 80
     :header-rows: 1

     * - Value
       - Meaning
     * - 0
       - Usage of aircraft by humans is **not allowed**
     * - 1
       - Usage of aircraft by humans is **allowed**
     * - 2
       - Usage of aircraft by humans is **allowed**, object will be restored
         after successfull landing

  :Output path: ``allows_spawning``
  :Output type: :class:`bool`
  :Output value:
    ``True`` if ``1`` or ``2``, ``False`` otherwise
    (``False`` for objects from old game versions)

  ..

  :Output path: ``restorable``
  :Output type: :class:`bool`
  :Output value:
    ``True`` if ``2``, ``False`` otherwise
    (``False`` for objects from old game versions)

``1.0``
  Not used (not present in old game versions).

``I-16type24_G1_RoW3.bmp``
  Skin name.

  :Output path: ``skin``
  :Output type: :class:`str`
  :Output value:
    original string value or ``None`` if ``null``
    (``None`` for objects from old game versions)
  :Default: ``null``

``1``
  Show markings or not.

  :Output path: ``show_markings``
  :Output type: :class:`bool`
  :Output value:
    ``True`` if ``1``, ``False`` otherwise
    (``None`` for objects from old game versions)


Ships
-----

Ships have all the same parameters as usual objects. Also ships in new versions
of game have some extra parameters which are described below.

We use :class:`~il2fb.parsers.mission.sections.nstationary.StationaryShip` data
structure to store information about ships.

Definition example::

  3_Static ships.Ship$G5 1 83759.05 115021.15 360.00 0.0 60 3 1.4

``60``
  Time of awakening (in minutes): it's a time which will pass since enemy unit
  enters ship's range till ship will react on that unit.

  :Output path: ``awakening_time``
  :Output type: :class:`float`
  :Output value:
    original value converted to float number
    (``0.0`` for objects from old game versions)

``3``
  Skill level of gunners.

  :Output path: ``skill``
  :Output type: complex `skills`_ constant
  :Output value: constant (``None`` for objects from old game versions)

``1.4``
  Recharge time (in minutes) of anti-aircraft guns of the ship.

  :Output path: ``recharge_time``
  :Output type: :class:`float`
  :Output value:
    original value converted to float number
    (``0.0`` for objects from old game versions)


.. _unit type: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L27
.. _types of units: `unit type`_

.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L21
.. _skills: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L20
.. _air forces: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L108

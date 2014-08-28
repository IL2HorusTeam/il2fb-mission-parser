.. _chiefs-section:

Chiefs section
==============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Chiefs>`_

:class:`~il2fb.parsers.mission.parsers.ChiefsParser` is responsible for parsing
``Chiefs`` section. It describes moving objects or their groups. Each of them is
defined on a separate line. There are 4 types of moving objects:

#. usual vehicles;
#. armored vehicles;
#. trains;
#. ships.

First 3 types have same list of parameters. Ships have some extra parameters.

Section example::

    [Chiefs]
      0_Chief Armor.1-BT7 2
      1_Chief Vehicles.GAZ67 1
      2_Chief Trains.USSR_FuelTrain/AA 1
      3_Chief Ships.G5 1 60 3 2.0


Output example:

.. code-block:: python

    {
        'chiefs': [
            {
                'belligerent': <constant 'Belligerents.blue'>,
                'id': "0_Chief",
                'code': "1-BT7",
                'type': <constant 'UnitTypes.armor'>,
            },
            {
                'belligerent': <constant 'Belligerents.red'>,
                'id': "1_Chief",
                'code': "GAZ67",
                'type': <constant 'UnitTypes.vehicle'>,
            },
            {
                'belligerent': <constant 'Belligerents.red'>,
                'id': "2_Chief",
                'code': "USSR_FuelTrain/AA",
                'type': <constant 'UnitTypes.train'>,
            },
            {
                'belligerent': <constant 'Belligerents.red'>,
                'id': "3_Chief",
                'code': "G5",
                'recharge_time': 2.0,
                'skill': <constant 'Skills.ace'>,
                'waiting_time': 60,
                'type': <constant 'UnitTypes.ship'>,
            },
        ],
    }

**Description**:

Output is a list of dictionaries containing information about each object.

Common parameters
-----------------

Let's examine common parameters using first object as example::

    0_Chief Armor.1-BT7 2

``0_Chief``
  Object's ID. Contains ``Chief`` word prefixed by a sequence number. This
  ID identifies a moving object or a group of them. In latter case, events log
  will contain this code followed by an in-group number of an object, e.g.::

      [5:25:14 PM] 0_Chief9 destroyed by 1_Chief2 at 11149.903 43949.902

  Here we can see that 9th object from group ``0_Chief`` was destroyed by 2nd
  object from group ``1_Chief``.

  :Output path: ``id``
  :Output type: :class:`str`
  :Output value: original string value

``Armor.1-BT7``
  Defines `unit type`_ and object's code.

  :Output path: ``type``
  :Output type: complex `unit type`_ constant

  ..

  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value

``2``
  Code number of army the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant

Ships extra parameters
----------------------

Ships have 3 extra parameters. Let's see an example::

    3_Chief Ships.G5 1 60 3 2.0

First 3 parameters are similar to the ones described above. The other parameters
are:

``60``
  Waiting time (in minutes): during this time a ship will be inactive. After
  that it will start following own route.

  :Output path: ``waiting_time``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``3``
  Skill level of gunners managing anti-aircraft guns.

  :Output path: ``skill``
  :Output type: complex `skills`_ constant

``2.0``
  Recharge time (in minutes) of anti-aircraft guns of the ship.

  :Output path: ``recharge_time``
  :Output type: :class:`float`
  :Output value: original value converted to float number


.. _unit type: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L34
.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L17
.. _skills: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L27

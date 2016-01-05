.. _bornplace-section:

BornPlace section
=================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-BornPlace>`_

:class:`~il2fb.parsers.mission.sections.born_place.BornPlaceSectionParser` is
responsible for parsing ``BornPlace`` section. Each line of this section
describes a single homebase.

Section example::

  [BornPlace]
    1 3000 121601 74883 1 1000 200 0 0 0 5000 50 0 1 1 0 0 3.8 1 0 0 0 0

Output example:

.. code-block:: python

  {
      'home_bases': [
          {
              'range': 3000,
              'belligerent': Belligerents.red,
              'show_default_icon': False,
              'friction': {
                  'enabled': False,
                  'value': 3.8,
              },
              'spawning': {
                  'enabled': True,
                  'with_parachutes': True,
                  'max_pilots': 0,
                  'in_stationary': {
                      'enabled': False,
                      'return_to_start_position': False,
                  },
                  'in_air': {
                      'height': 1000,
                      'speed': 200,
                      'heading': 0,
                      'conditions': {
                          'always': False,
                          'if_deck_is_full': False,
                      },
                  },
                  'aircraft_limitations': {
                      'enabled': True,
                      'consider_lost': True,
                      'consider_stationary': True,
                  },
              },
              'radar': {
                  'range': 50,
                  'min_height': 0,
                  'max_height': 5000,
              },
              'pos': Point2D(121601.0, 74883.0),
          },
      ],
  }


**Description**:

The output of the parser is a :class:`dict` with  ``homebases`` item which
contains a list of of dictionaries. Each dictionary contains information about
single homebase.

``1``
  Code number of army the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant

``3000``
  Homebase range (in meters).

  :Output path: ``range``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``121601``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``74883``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``1``
  Tells whether users will have parachutes.

  :Output path: ``spawning.with_parachutes``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``1000``
  Initial height of aircraft (in meters) if it was spawned in the air.

  :Output path: ``spawning.in_air.height``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``200``
  Initial speed of aircraft (in km/h) if it was spawned in the air.

  :Output path: ``spawning.in_air.speed``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Initial heading of aircraft (in degrees) if it was spawned in the air.

  :Output path: ``spawning.in_air.heading``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Max number of pilots who can take off from this homebase. ``0`` means
  unlimited.

  :Output path: ``spawning.max_pilots``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Radar detection min height (in meters).

  :Output path: ``radar.min_height``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``5000``
  Radar detection max height (in meters).

  :Output path: ``radar.max_height``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``50``
  Radar detection range (in km).

  :Output path: ``radar.range``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``0``
  Spawn only in air.

  :Output path: ``spawning.in_air.conditions.always``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``1``
  Enable aircraft limits.

  :Output path: ``spawning.aircraft_limitations.enabled``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``1``
  Homebase looses aircrafts as they get destroyed.

  :Output path: ``spawning.aircraft_limitations.consider_lost``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``0``
  Disable spawning. Output has inverted value.

  :Output path: ``spawning.enabled``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``0``, ``False`` otherwise

``0``
  Enable friction.

  :Output path: ``friction.enabled``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``3.8``
  Friction value.

  :Output path: ``friction.value``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``1``
  Homebase looses aircrafts as stationary aircrafts get destroyed.

  :Output path: ``spawning.aircraft_limitations.consider_stationary``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``0``
  Render homebase icon at default position.

  :Output path: ``show_default_icon``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``0``
  Spawn in air if deck is full.

  :Output path: ``spawning.in_air.conditions.if_deck_is_full``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``0``
  Spawn in stationary aircrafts.

  :Output path: ``spawning.in_stationary.enabled``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``0``
  Return stationary aircraft to start position after landing.

  :Output path: ``spawning.in_stationary.return_to_start_position``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise


.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L21

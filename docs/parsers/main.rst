.. _main-section:

MAIN section
============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-MAIN>`_

:class:`~il2fb.parsers.mission.sections.main.MainSectionParser` is responsible
for parsing ``MAIN`` section. This section contains one key-value pair per each
line.

Section example::

    [MAIN]
      MAP Moscow/sload.ini
      TIME 11.75
      TIMECONSTANT 1
      WEAPONSCONSTANT 1
      CloudType 1
      CloudHeight 1500.0
      player fiLLv24fi00
      army 1
      playerNum 0

Output example:

.. code-block:: python

    {
        'location_loader': 'Moscow/sload.ini',
        'time': {
            'value': datetime.time(11, 45),
            'is_fixed': True,
        },
        'weather_conditions': <constant 'Conditions.good'>,
        'cloud_base': 1500,
        'player': {
            'belligerent': <constant 'Belligerents.red'>,
            'flight_id': "fiLLv24fi00",
            'aircraft_index': 0,
            'fixed_weapons': True,
        },
    }

As you can see, we have a :class:`dict` as a result.


**Description**:

``MAP``
  Name of location loader. Location loaders contain information about locations
  (textures, air pressure, air temperature, list of map labels, etc) and can be
  found inside ``fb_maps*.SFS`` archives.

  :Output path: ``location_loader``
  :Output type: :class:`str`
  :Output value: original string value

``TIME``
  Initial time in mission. Defined as a real number. Integer part defines
  hour. Fractional part defines minutes as a fraction of 60 minutes, so
  ``0.75`` is ``60 * 0.75 = 45`` minutes indeed.

  :Output path: ``time.value``
  :Output type: :class:`datetime.time`

``TIMECONSTANT``
  Whether time specified by ``TIME`` must be fixed during all mission long.

  :Output path: ``time.is_fixed``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``WEAPONSCONSTANT``
  Whether player's loadout is fixed (usually used in single player).

  :Output path: ``player.fixed_weapons``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

``CloudType``
  Describes type of weather by code in range ``[0-6]``.

  :Output path: ``weather_conditions``
  :Output type: complex `weather conditions`_ constant

``CloudHeight``
  A real number which defines cloud base.

  :Output path: ``cloud_base``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``player`` [1]_
  ID of AI flight which player will be the part of during single mission or
  campaign mission.

  :Output path: ``player.flight_id``
  :Output type: :class:`str`
  :Output value: original string value or ``None`` if not present

``army`` [1]_
  Code number of player's belligerent. This value is primarily used to
  correctly define types of targets for a particular player.

  For example, this value equals to ``1`` and there are 2 targets defined for
  mission:
  1) destroy an object; 2) protect objects in an area.

  In this case, Allies will see these targets on map without changes.

  But for the Axis these targets will be displayed with the opposite meaning,
  i.e.: 1) protect an object; 2) destroy objects in an area.

  This principle works only if there are only 2 belligerents in mission:
  red and blue.

  :Output path: ``player.belligerent``
  :Output type: complex `belligerents`_ constant

``playerNum`` [1]_
  Player's position in flight defined by ``player``. It's always equal to
  ``0`` if ``player`` is not set.

  :Output path: ``player.aircraft_index``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

----------

Footnotes:

.. [#] For single player mode only.


.. _weather conditions: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/weather.py#L11
.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L20


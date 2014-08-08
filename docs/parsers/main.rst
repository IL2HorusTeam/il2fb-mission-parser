.. _main-parser:

Main parser
===========

:class:`~il2fb.parsers.mission.parsers.MainParser` is responsible for parsing
``MAIN`` section. This section contains one key-value pair per each line.
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

Output example::

    {
      'loader': 'Moscow/sload.ini',
      'time': {
          'value': datetime.time(11, 45),
          'is_fixed': True,
      },
      'fixed_loadout': True,
      'weather_conditions': <constant 'Conditions.good'>,
      'cloud_base': 1500,
      'player': {
          'belligerent': <constant 'Belligerents.red'>,
          'regiment': "fiLLv24fi00",
          'number': 0,
      },
    }

**Description**:

MAP
  Name of location loader. Location loaders contain information about locations
  (textures, air pressure, air temperature, list of map labels, etc) and can be
  found inside ``fb_maps*.SFS`` archives.

  :Output path: ``loader``
  :Output type: :class:`str`
  :Output value: original string value

TIME
  Initial time in mission. Defined as a real number. Integer part defines
  hour. Fractional part defines minutes as a fraction of 60 minutes, so
  ``0.75`` is ``60 * 0.75 = 45`` indeed.

  :Output path: ``time.value``
  :Output type: :class:`datetime.time`

TIMECONSTANT
  Whether time specified by ``TIME`` must be fixed during all mission long.

  :Output path: ``time.is_fixed``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

WEAPONSCONSTANT
  Whether player's loadout is fixed.

  :Output path: ``fixed_loadout``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise

CloudType
  Describes type of weather by code in range ``[0-6]``.

  :Output path: ``weather_conditions``
  :Output type: complex `weather conditions`_ constant

CloudHeight
  A real number which defines cloud base.

  :Output path: `cloud_base``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

player [1]_
  Code name of player's regiment.

  :Output path: ``player.regiment``
  :Output type: :class:`str`
  :Output value: original string value or ``None`` if not present

army [1]_
  Code number of player's army.

  :Output path: ``player.belligerent``
  :Output type: complex `belligerents`_ constant

playerNum [1]_
  Player's position in flight. Always equal to ``0`` if ``player`` is not set

  :Output path: ``player.number``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

---------

Footnotes:

.. [#] For single player mode only.


.. _weather conditions: https://github.com/IL2HorusTeam/il2fb-commons/blob/4a3cb79301c792c685d472a17926d978cd703f14/il2fb/commons/weather.py#L10
.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/4a3cb79301c792c685d472a17926d978cd703f14/il2fb/commons/organization.py#L17

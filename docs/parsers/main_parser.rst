Main parser
===========

.. _main-parser:

:class:`~il2ds_mis_parser.parsers.MainParser` is responsible for parsing
``MAIN`` section. This section contains key-value pair on each line.

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
        'weather_type': 'clear',
        'clouds_height': 1500,
        'player': {
            'army': 'red',
            'regiment': "fiLLv24fi00",
            'number': 0,
        },
    }

**Description**:

MAP
  Name of location loader. Location loaders contain information about locations
  (textures, air pressure, air temperature, list of map labels, etc) and can be
  found inside ``fb_maps*.SFS`` archives.

  **Output path**: ``loader``

  **Output type**: :class:`str`

  **Output value**: original string value

TIME
  Initial time in mission. Defined as a real number. Integer part defines
  hour. Fractional part defines minutes as a fraction of 60 minutes, so
  ``0.75`` is ``60 * 0.75 = 45`` indeed.

  **Output path**: ``time.value``

  **Output type**: :class:`datetime.time`

TIMECONSTANT
  Whether time specified by ``TIME`` must be fixed during all mission long.

  **Output path**: ``time.is_fixed``

  **Output type**: :class:`bool`

  **Output value**: ``True`` if ``1``, ``False`` otherwise

WEAPONSCONSTANT
  Whether player's loadout is fixed.

  **Output path**: ``fixed_loadout``

  **Output type**: :class:`bool`

  **Output value**: ``True`` if ``1``, ``False`` otherwise

CloudType
  Describes type of weather by code in range ``[0-6]``.

  **Output path**: ``weather_type``

  **Output type**: :class:`str`

  **Output value**: a value from :data:`~il2ds_mis_parser.constants.WEATHER_TYPES`
  dictionary

CloudHeight
  A real number which defines height of clouds.

  **Output path**: ``clouds_height``

  **Output type**: :class:`float`

  **Output value**: original value converted to float number

player [1]_
  Code name of player's regiment.

  **Output path**: ``player.regiment``

  **Output type**: :class:`str`

  **Output value**: original string value or ``None`` if not present

army [1]_
  Code number of player's army.

  **Output path**: ``player.army``

  **Output type**: :class:`str`

  **Output value**: a value from :data:`~il2ds_mis_parser.constants.ARMIES`
  dictionary

playerNum [1]_
  Player's position in flight.

  **Output path**: ``player.number``

  **Output type**: :class:`int`

  **Output value**: original value converted to integer number

---------

Footnotes:

.. [#] For single player mode only.

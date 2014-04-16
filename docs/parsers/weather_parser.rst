Weather Parser
==============

.. _weather-parser:

:class:`~il2_mis_parser.parsers.WeatherParser` is responsible for parsing
``WEATHER`` section. This section contains one key-value pair per each line.

Section example::

    [WEATHER]
      WindDirection 120.0
      WindSpeed 3.0
      Gust 0
      Turbulence 0

Output example::

    {
        'weather': {
            'wind': {
                'direction': 120.0,
                'speed': 3.0,
            },
            'gust': 'none',
            'turbulence': 'none',
        },
    }

**Description**:

WindDirection
  Wind direction in degrees.

  **Output path**: ``weather.wind.direction``

  **Output type**: :class:`float`

  **Output value**: original value converted to float number

WindSpeed
  Wind speed in meters per second.

  **Output path**: ``weather.wind.speed``

  **Output type**: :class:`float`

  **Output value**: original value converted to float number

Gust
  Number in range ``[0-3]`` which defines strength of wind gusts.

  **Output path**: ``weather.gust``

  **Output type**: :class:`str`

  **Output value**: a value from :data:`~il2_mis_parser.constants.GUST_TYPES`
  dictionary

Turbulence
  Number in range ``[0-4]`` which defines strength of wind turbulence.

  **Output path**: ``weather.turbulence``

  **Output type**: :class:`str`

  **Output value**: a value from :data:`~il2_mis_parser.constants.TURBULENCE_TYPES`
  dictionary

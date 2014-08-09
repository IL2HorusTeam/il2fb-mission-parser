Weather Parser
==============

.. _weather-parser:

:class:`~il2fb.parsers.mission.parsers.WeatherParser` is responsible for parsing
``WEATHER`` section. This section contains one key-value pair per each line.

Section example::

    [WEATHER]
      WindDirection 120.0
      WindSpeed 3.0
      Gust 0
      Turbulence 4

Output example:

.. code-block:: python

    {
        'weather': {
            'wind': {
                'direction': 120.0,
                'speed': 3.0,
            },
            'gust': <constant 'Gust.none'>,
            'turbulence': <constant 'Turbulence.very_strong'>,
        },
    }

**Description**:

WindDirection
  Wind direction in degrees.

  :Output path: ``weather.wind.direction``
  :Output type: :class:`float`
  :Output value: original value converted to float number

WindSpeed
  Wind speed in meters per second.

  :Output path: ``weather.wind.speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

Gust
  Number in range ``[0-3]`` which defines strength of wind gusts.

  :Output path: ``weather.gust``
  :Output type: complex `gust`_ constant

Turbulence
  Number in range ``[0-4]`` which defines strength of wind turbulence.

  :Output path: ``weather.turbulence``
  :Output type: complex `turbulence`_ constant


.. _gust: https://github.com/IL2HorusTeam/il2fb-commons/blob/4a3cb79301c792c685d472a17926d978cd703f14/il2fb/commons/weather.py#L20
.. _turbulence: https://github.com/IL2HorusTeam/il2fb-commons/blob/4a3cb79301c792c685d472a17926d978cd703f14/il2fb/commons/weather.py#L27

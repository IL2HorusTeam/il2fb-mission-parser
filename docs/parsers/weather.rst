.. _weather-section:

WEATHER section
===============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Weather>`_

:class:`~il2fb.parsers.mission.sections.weather.WeatherSectionParser` is
responsible for parsing ``WEATHER`` section. This section describes additional
weather conditions and contains one key-value pair per each line.

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

Output contains a :class:`dict` with ``weather`` element.


**Description**:

``WindDirection``
  Wind direction in degrees.

  :Output path: ``weather.wind.direction``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``WindSpeed``
  Wind speed in meters per second.

  :Output path: ``weather.wind.speed``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``Gust``
  Number in range ``[0-3]`` which defines strength of wind gusts.

  :Output path: ``weather.gust``
  :Output type: complex `gust`_ constant

``Turbulence``
  Number in range ``[0-4]`` which defines strength of wind turbulence.

  :Output path: ``weather.turbulence``
  :Output type: complex `turbulence`_ constant


.. _gust: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/weather.py#L21
.. _turbulence: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/weather.py#L28

.. _bornplace-air-forces-section:

BornPlace air forces section
============================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-BornPlace-Air-Forces>`_

:class:`~il2fb.parsers.mission.parsers.BornPlaceAirForcesParser` is responsible
for parsing ``BornPlaceCountriesN`` section, where ``N`` is sequence number of
the homebase. This section defines a list of available airforces for
homebase #N.

Each line contains a code name of a single air force.

Section example::

  [BornPlaceCountries1]
    de
    ru

Output example:

.. code-block:: python

  {
      'home_base_air_forces_1': [
          <constant 'AirForces.luftwaffe'>,
          <constant 'AirForces.vvs_rkka'>,
      ],
  }

The output of the parser is a :class:`dict` with ``home_base_air_forces_N``
item, where ``N`` is original homebase number. The value is a list of
`air forces`_.


.. _air forces: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L94

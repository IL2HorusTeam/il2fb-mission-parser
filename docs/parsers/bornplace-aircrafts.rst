.. _bornplace-aircrafts-section:

BornPlace aircrafts section
===========================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-BornPlace-Aircrafts>`_

:class:`~il2fb.parsers.mission.parsers.BornPlaceAircraftsParser` is responsible
for parsing ``BornPlaceN`` section, where ``N`` is sequence number of the
homebase. This section describes aircrafts which are available on the
homebase #N.

Each line describes attributes of a single aircraft. Lines which start with
``+`` mark continuation of previous line. Max line lenght is approximately
210-220 characters.

Section example::

  [BornPlace1]
    Bf-109F-4 -1 1sc250 4sc50
    Bf-109G-6_Late 0
    Ju-88A-4 10 28xSC50 28xSC50_2xSC250 28xSC50_4xSC250
    + 2xSC1800 2xSC2000

Output example:

.. code-block:: python

  {
      'homebase_aircrafts_1': [
          {
              'code': 'Bf-109F-4',
              'limit': None,
              'weapon_limits': [
                  '1sc250',
                  '4sc50',
              ],
          },
          {
              'code': 'Bf-109G-6_Late',
              'limit': 0,
              'weapon_limits': [],
          },
          {
              'code': 'Ju-88A-4',
              'limit': 10,
              'weapon_limits': [
                  '28xSC50',
                  '28xSC50_2xSC250',
                  '28xSC50_4xSC250',
                  '2xSC1800',
                  '2xSC2000',
              ],
          },
      ],
  }

**Description**:

The output of the parser is a dictionary with a single item. It is accessible by
``homebase_aircrafts_N`` key, where ``N`` is original homebase number. The value
is a list of dictionaries. Each dictionary represents a single aircraft.

Let's examine first line.

``Bf-109F-4``
  Aircraft code name.

  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value

``0``
  Number of available aircrafts. This parameter makes sence only if homebase
  has aircraft limitation turned on.

  ``-1`` means that the number of aircrafts is unlimited.

  ``0`` means that aircraft will not even be presentin the list of available
  aircrafts.

  :Output path: ``limit``
  :Output type: :class:`int`
  :Output value:
    ``None`` if ``-1``, original value converted to integer number otherwise

``1sc250 4sc50``
  List of code names of allowed weapons for this aircraft. This part is
  optional: if it is not present, than all available weapons will be allowed.

  :Output path: ``weapon_limits``
  :Output type: :class:`list`
  :Output value: list of strings

.. _bornplace-aircrafts-section:

BornPlace aircrafts section
===========================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-BornPlace-Aircrafts>`_

:class:`~il2fb.parsers.mission.sections.born_place_aircrafts.BornPlaceAircraftsSectionParser`
is responsible for parsing ``BornPlaceN`` section, where ``N`` is sequence
number of the home base. This section describes aircrafts which are available
on the home base #N.

Each line describes attributes of a single aircraft. Lines, which start with
``+``, mark continuation of previous line. Max line length is approximately
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
      'home_base_aircrafts_1': [
          {
              'code': 'Bf-109F-4',
              'limit': None,
              'weapon_limitations': [
                  '1sc250',
                  '4sc50',
              ],
          },
          {
              'code': 'Bf-109G-6_Late',
              'limit': 0,
              'weapon_limitations': [],
          },
          {
              'code': 'Ju-88A-4',
              'limit': 10,
              'weapon_limitations': [
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

The output of the parser is a :class:`dict` with ``home_base_aircrafts_N``
item, where ``N`` is original home base number. This item contains a list of
dictionaries. Each dictionary stores information about single aircraft.

Let's examine the first line.

``Bf-109F-4``
  Aircraft code name.

  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value

``0``
  Number of available aircrafts. This parameter makes sence only if home base
  has aircraft limitations turned on.

  ``-1`` means that the number of aircrafts is unlimited.

  ``0`` means that aircraft will not even be present in the list of available
  aircrafts in briefing.

  :Output path: ``limit``
  :Output type: :class:`int`
  :Output value:
    ``None`` if ``-1``, original value converted to integer number otherwise
    (always ``None`` for games of old versions)

``1sc250 4sc50``
  List of code names of allowed weapons for this aircraft. This part is
  optional: if it is not present, than all available weapons will be allowed.

  :Output path: ``weapon_limits``
  :Output type: :class:`list`
  :Output value:
    list of strings (list is always empty for games of old versions)

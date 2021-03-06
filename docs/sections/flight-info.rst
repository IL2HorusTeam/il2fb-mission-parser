.. _flight-info-section:

Flight info section
===================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Flight-info>`_

:class:`~il2fb.parsers.mission.sections.wing.FlightInfoSectionParser` is
responsible for parsing sections which provide information about aircrafts in a
single flight. That information includes general data about all aircrafts and
it can include data about individual aircrafts.

The output of the parser is a :class:`dict` with a ``FLIGHT_ID_info`` item,
where ``FLIGHT_ID`` is ID of the flight which is listed in :doc:`wing`.
The item contains a dictionary with information about flight.

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Section names
-------------

Sections which describe flights use flight IDs as their names. Flight ID
consists of code name and two digits at the right side, e.g. ``3GvIAP10``.

Code name is a code name of a regiment or a default code of a particular air
force. For example, ``3GvIAP`` is a name of regiment of VVS RKKA and ``r01``
is default prefix for that air force (see the `list of air forces`_).

Two digits in the flight ID mean squadron and flight indexes respectively. Both
of them use zero-based numbering, so ``00`` means 1st squadron, 1st flight.
There can be up to 4 squadrons in a regiment with up to 4 flights in a
squadron. Code of the 4th flight in the 4th squadron will be ``33``.

Parser's output contains air force, regiment, squadron and flight number:

  :Output path: ``air_force``
  :Output type: `air force`_ constant

..

  :Output path: ``regiment``
  :Output type: class `Regiment`_
  :Output value: ``Regiment`` object or ``None``

..

  :Output path: ``squadron_index``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

..

  :Output path: ``flight_index``
  :Output type: :class:`int`
  :Output value: original value converted to integer number


General information
-------------------

Section example::

  [3GvIAP10]
    Planes 3
    OnlyAI 1
    Parachute 0
    Skill 1
    Class air.A_20C
    Fuel 100
    weapons default

Output example:

.. code-block:: python

  {
      '3GvIAP10_info': {
          'id': '3GvIAP10',
          'air_force': AirForces.vvs_rkka,
          'regiment': <Regiment '3GvIAP'>,
          'squadron_index': 1,
          'flight_index': 0,
          'code': 'A_20C',
          'count': 3,
          'weapons': 'default',
          'fuel': 100,
          'ai_only': True,
          'with_parachutes': False,
          'aircrafts': [
              {
                  'index': 0,
                  'has_markings': True,
                  'skill': Skills.average,
              },
              {
                  'index': 1,
                  'has_markings': True,
                  'skill': Skills.average,
              },
              {
                  'index': 2,
                  'has_markings': True,
                  'skill': Skills.average,
              },
          ],
      },
  }


Description:

``Planes``
  Number of planes in flight. Maximal value is 4.

  :Input presence: always present
  :Output path: ``count``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``OnlyAI``
  Tells whether users cannot join flight.

  :Input presence: present only if turned off
  :Output path: ``ai_only``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise
  :Output default: ``False``

``Parachute``
  Tells whether crew members of all planes in flight have parachutes.

  :Input presence: present only if turned off
  :Output path: ``with_parachutes``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise
  :Output default: ``True``

``Skill``
  Skill level for all planes in flight.

  :Input presence:
    present only if all aircrafts in flight have same level of skills
  :Output path:
    ``aircrafts[i].skill``, where ``i`` is aircraft index. Skills are applied
    to every aircraft individually (see section below)
  :Output type: complex `skills`_ constant

``Class``
  Aircraft code name with ``air.`` prefix.

  :Input presence: always present
  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value without ``air.`` prefix

``Fuel``
  Fullness of fuel (in percents).

  :Input presence: always present
  :Output path: ``fuel``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``weapons``
  Weapons code name.

  :Input presence: always present
  :Output path: ``weapons``
  :Output type: :class:`str`
  :Output value: original string value


Individual skills
-----------------

Section example::

  [UN_NN03]
    Planes 2
    Skill0 2
    Skill1 3
    Skill2 1
    Skill3 1
    Class air.B_17G
    Fuel 100
    weapons default

Output example:

.. code-block:: python

    {
        'UN_NN03_info': {
            'air_force': AirForces.usn,
            'regiment': None,
            'squadron_index': 0,
            'flight_index': 3,
            'code': 'B_17G',
            'count': 2,
            'weapons': 'default',
            'fuel': 100,
            'ai_only': False,
            'with_parachutes': True,
            'aircrafts': [
                {
                    'index': 0,
                    'has_markings': True,
                    'skill': Skills.veteran,
                },
                {
                    'index': 1,
                    'has_markings': True,
                    'skill': Skills.ace,
                },
            ],
        },
    }


As you can see from the previous section, flight info can contain ``Skill``
parameter. It defines skill level for all aircrafts in the flight. However,
if you need to override skill level even for a single aircraft, ``Skill``
paramenter will be decomposed into 4 paramenters (even if you have less than 4
aircraft in the flight): ``Skill0``, ``Skill1``, ``Skill2`` and ``Skill3``.

In our example we have 2 aircrafts in a flight with veteran (``Skill0 2``) and
ace (``Skill1 3``) skill levels respectively. Other skill entries (``Skill2 1``
and ``Skill3 1``) have really no meaning. Their values are equal to default
skill level for this flight which was set before it was overridden.


Other individual parameters
---------------------------

Section example::

  [UN_NN02]
    Planes 1
    Skill 1
    Class air.B_17G
    Fuel 100
    weapons default
    skin0 RRG_N7-B_Damaged.bmp
    noseart0 Angry_Ox.bmp
    pilot0 fi_18.bmp
    numberOn0 0
    spawn0 0_Static

Output example:

.. code-block:: python

    {
        'UN_NN02_info': {
            'air_force': AirForces.usn,
            'regiment': None,
            'squadron_index': 1,
            'flight_index': 3,
            'code': 'B_17G',
            'count': 1,
            'weapons': 'default',
            'fuel': 100,
            'ai_only': False,
            'with_parachutes': True,
            'aircrafts': [
                {
                    'index': 0,
                    'has_markings': False,
                    'skill': Skills.average,
                    'aircraft_skin': 'RRG_N7-B_Damaged.bmp',
                    'pilot_skin': 'fi_18.bmp',
                    'nose_art': 'Angry_Ox.bmp',
                    'spawn_object': '0_Static',
                },
            ],
        },
    }


As you can see from the previous examples, parsed individual parameters for
are stored in ``aircrafts`` list. Each element of this list is a dictionary
with information about a single aircraft.

Aircraft index is accessed by ``index`` key. Index is a number in range 0-3.

We have discussed individual skills already: skill level is accessed by
``skill`` key.

Section with information about flight may contain some extra individual
parameters which are suffixed by index of the aircraft they are related to:

``skinX``
  Name of custom skin for aircraft with index ``X``.

  :Input presence: present only if non-default skin was selected
  :Output path: ``aircraft_skin``
  :Output type: :class:`str`
  :Output value: original string value

``noseartX``
  Name of used nose art for aircraft with index ``X``.

  :Input presence: present only if nose art was selected
  :Output path: ``nose_art``
  :Output type: :class:`str`
  :Output value: original string value

``pilotX``
  Name of custom skin for crew members of aircraft with index ``X``.

  :Input presence: present only if non-default skin was selected
  :Output path: ``pilot_skin``
  :Output type: :class:`str`
  :Output value: original string value

``numberOnX``
  Tells whether markings are present for aircraft with index ``X``.

  :Input presence: present only if turned off
  :Output path: ``has_markings``
  :Output type: :class:`bool`
  :Output value: ``True`` if ``1``, ``False`` otherwise
  :Output default: ``True``

``spawnX``
  ID of static object which is used for spawning aircraft with index ``X``.

  :Input presence: present only if spawn object was set
  :Output path: ``spawn_object``
  :Output type: :class:`str`
  :Output value: original string value


.. _air force: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L108
.. _list of air forces: `air force`_

.. _skills: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/__init__.py#L20
.. _Regiment: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L282

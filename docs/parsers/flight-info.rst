.. _flight-info-section:

Flight info section
===================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Flight info>`_

:class:`~il2fb.parsers.mission.parsers.FlightInfoParser` is responsible for
parsing ``FlightInfoParser`` section. This section provides information about
aircrafts in a single flight. That information includes general data about
all aircrafts and it can include data about individual aircrafts.

The output of the parser is a dictionary with a single item. It is accessible by
``FLIGHT_ID`` key, where ``FLIGHT_ID`` is an ID of the flight which is listed
in :ref:`wing-section`. The value is a dictionary with information about flight.

.. contents::
    :local:
    :depth: 1
    :backlinks: none


General information
-------------------

Section example::

  [UN_NN10]
    Planes 3
    OnlyAI 1
    Parachute 0
    Skill 1
    Class air.B_17G
    Fuel 100
    weapons default

Output example:

  .. code-block:: python

    {
        'UN_NN10_info': {
            'air_force': <constant 'AirForces.usn'>,
            'regiment': None,
            'squadron': 2,
            'flight': 1,
            'count': 3,
            'code': 'B_17G',
            'weapons': 'default',
            'fuel': 100,
            'ai_only': True,
            'with_parachutes': False,
            'aircrafts': [
                {
                    'nose_art': None,
                    'number': 0,
                    'spawn_object': None,
                    'has_markings': True,
                    'skill': <constant 'Skills.average'>,
                    'aircraft_skin': None,
                    'pilot_skin': None,
                },
                {
                    'nose_art': None,
                    'number': 1,
                    'spawn_object': None,
                    'has_markings': True,
                    'skill': <constant 'Skills.average'>,
                    'aircraft_skin': None,
                    'pilot_skin': None,
                },
                {
                    'nose_art': None,
                    'number': 2,
                    'spawn_object': None,
                    'has_markings': True,
                    'skill': <constant 'Skills.average'>,
                    'aircraft_skin': None,
                    'pilot_skin': None,
                },
            ],
        },
    }

Description:

.. todo::


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
              'air_force': <constant 'AirForces.usn'>,
              'regiment': None,
              'squadron': 1,
              'flight': 4,
              'count': 2,
              'code': 'B_17G',
              'weapons': 'default',
              'fuel': 100,
              'ai_only': False,
              'with_parachutes': True,
              'aircrafts': [
                  {
                      'nose_art': None,
                      'number': 0,
                      'spawn_object': None,
                      'has_markings': True,
                      'skill': <constant 'Skills.veteran'>,
                      'aircraft_skin': None,
                      'pilot_skin': None,
                  },
                  {
                      'nose_art': None,
                      'number': 1,
                      'spawn_object': None,
                      'has_markings': True,
                      'skill': <constant 'Skills.ace'>,
                      'aircraft_skin': None,
                      'pilot_skin': None,
                  },
              ],
          },
      }


Description:

.. todo::


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
              'air_force': <constant 'AirForces.usn'>,
              'regiment': None,
              'squadron': 1,
              'flight': 3,
              'count': 1,
              'code': 'B_17G',
              'weapons': 'default',
              'fuel': 100,
              'ai_only': False,
              'with_parachutes': True,
              'aircrafts': [
                  {
                      'number': 0,
                      'spawn_object': '0_Static',
                      'has_markings': False,
                      'skill': <constant 'Skills.average'>,
                      'aircraft_skin': 'RRG_N7-B_Damaged.bmp',
                      'pilot_skin': 'fi_18.bmp',
                      'nose_art': 'Angry_Ox.bmp',
                  },
              ],
          },
      }


Description:

.. todo::


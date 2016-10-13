.. _mission-parser:

Mission parser
==============

.. note::

  `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%9F%D0%B0%D1%80%D1%81%D0%B5%D1%80-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0-%D0%BC%D0%B8%D1%81%D1%81%D0%B8%D0%B8>`_


:class:`~il2fb.parsers.mission.MissionParser` is responsible for parsing
whole mission files or sequences of strings which look like mission definition.

This parser detects sections in the stream of strings, selects a proper parser
for a certain section and combines results from all parsers into a single
whole. The output of this parser is a :class:`dict`.

Since many sections are optional (e.g., a list of moving ground units, their
routes, a list of available aircrafts at airfields, etc.) and some sections
may not be available in previous versions of the game (e.g., ``MDS``), so
we cannot talk about a clear and predefined structure of parser's result.
To understand what may be in the output, it will be much easier and
clearer to :doc:`use project's demo <demo>`.

Here we will go through the very principles on which the final result is
formed. It *may* contain the following elements:

.. contents::
    :local:
    :depth: 2
    :backlinks: none


Example of parser result:

.. code-block:: python

    {
       'location_loader': 'Slovakia/load_online.ini',
       'player': {
          'aircraft_index': 0,
          'belligerent': Belligerents.red,
          'fixed_weapons': False,
          'flight_id': None,
       },
       'targets': [
          {
             'type': TargetTypes.recon,
             'priority': TargetPriorities.secondary,
             'in_sleep_mode': True,
             'delay': 50,
             'requires_landing': False,
             'pos': Point2D(133978.0, 87574.0),
             'radius': 1150,
          },
          {
             'type': TargetTypes.recon,
             'priority': TargetPriorities.primary,
             'in_sleep_mode': True,
             'delay': 40,
             'requires_landing': True,
             'pos': Point2D(134459.0, 85239.0),
             'radius': 300,
             'object': {
                 'waypoint': 0,
                 'id': '1_Chief',
                 'pos': Point2D(134360.0, 85346.0),
             },
          },
       ],
       'conditions': {
          'time_info': {
             'date': datetime.date(1945, 4, 5),
             'time': datetime.time(10, 0),
             'is_fixed': False,
          },
          'meteorology': {
             'cloud_base': 1300,
             'gust': Gust.none,
             'turbulence': Turbulence.none,
             'weather': Conditions.hazy,
             'wind': {
                'direction': 180.0,
                'speed': 2.0,
             },
          },
          'communication': {
             'ai_radio_silence': False,
             'tower_communication': True,
             'vectoring': True,
          },
          'scouting': {
             'only_scouts_complete_targets': False,
             'scouts_affect_radar': False,
             'ships_affect_radar': False,
          },
          'respawn_time': {
             'artillery': 1000000,
             'balloons': 1000000,
             'searchlights': 1000000,
             'ships': {
                'big': 1000000,
                'small': 1000000,
             },
          },
          'radar': {
             'advanced_mode': False,
             'refresh_interval': 0,
             'scouts': {
                'alpha': 5,
                'max_height': 1500,
                'max_range': 2,
             },
             'ships': {
                'big': {
                   'max_height': 5000,
                   'max_range': 100,
                   'min_height': 100,
                },
                'small': {
                   'max_height': 2000,
                   'max_range': 25,
                   'min_height': 0,
                },
             },
          },
          'home_bases': {
             'hide_ai_aircrafts_after_landing': False,
             'hide_players_count': False,
             'hide_unpopulated': True,
          },
          'crater_visibility_muptipliers': {
             'gt_1000kg': 1.0,
             'le_1000kg': 1.0,
             'le_100kg': 1.0,
          },
       },
       'objects': {
          'moving_units': [
             {
                'id': '0_Chief',
                'type': UnitTypes.train,
                'code': 'Germany_CargoTrainA/AA',
                'belligerent': Belligerents.blue,
                'route': [
                   GroundRoutePoint(
                      pos=Point2D(21380.02, 41700.34),
                      is_checkpoint=True,
                      delay=10,
                      section_length=2,
                      speed=11.0,
                   ),
                   GroundRoutePoint(
                      pos=Point2D(21500.00, 41700.00),
                      is_checkpoint=False,
                   ),
                ],
             },
          ],
          'flights': [
             {
                'ai_only': False,
                'air_force': AirForces.luftwaffe,
                'aircrafts': [
                   {
                      'index': 0,
                      'has_markings': True,
                      'skill': Skills.ace,
                   },
                ],
                'code': 'Do217_K2',
                'count': 1,
                'flight_index': 0,
                'fuel': 100,
                'id': 'g0100',
                'regiment': None,
                'squadron_index': 0,
                'weapons': 'default',
                'with_parachutes': True,
                'route': [
                   FlightRouteTakeoffPoint(
                      type=RoutePointTypes.takeoff_normal,
                      pos=Point3D(193373.53, 99288.17, 0.0),
                      speed=0.0,
                      formation=None,
                      radio_silence=False,
                      delay=10,
                      spacing=20,
                   ),
                   FlightRoutePoint(
                      type=RoutePointTypes.landing_straight,
                      pos=Point3D(185304.27, 54570.12, 0.00),
                      speed=0.00,
                      formation=None,
                      radio_silence=True,
                   ),
                ],
             },
          ],
          'home_bases': [
             {
                'belligerent': Belligerents.red,
                'friction': {
                   'enabled': False,
                   'value': 3.8,
                },
                'pos': Point2D(151796.0, 71045.0),
                'radar': {
                   'max_height': 5000,
                   'min_height': 0,
                   'range': 50,
                },
                'range': 3000,
                'show_default_icon': False,
                'spawning': {
                   'aircraft_limitations': {
                      'allowed_aircrafts': [
                         {
                            'code': 'Il-2_3',
                            'limit': None,
                            'weapon_limitations': [
                               '4xRS82',
                               '4xBRS82',
                               '4xRS132',
                            ]
                         },
                         {
                            'code': 'Il-2_M3',
                            'limit': None,
                            'weapon_limitations': [
                               '4xBRS132',
                               '4xM13',
                               '216xAJ-2',
                            ],
                         },
                      ],
                      'consider_lost': True,
                      'consider_stationary': True,
                      'enabled': True,
                   },
                   'allowed_air_forces': [
                      AirForces.vvs_rkka,
                   ],
                   'enabled': True,
                   'in_air': {
                      'conditions': {
                         'always': False,
                         'if_deck_is_full': False,
                      },
                      'heading': 0,
                      'height': 1000,
                      'speed': 200,
                   },
                   'in_stationary': {
                      'enabled': False,
                      'return_to_start_position': False,
                   },
                  'max_pilots': 0,
                  'with_parachutes': True,
                },
             },
          ],
          'stationary': [
             StationaryObject(
                belligerent=Belligerents.none,
                id='6_Static',
                code='Smoke20',
                pos=Point2D(151404.61, 89009.57),
                rotation_angle=0.00,
                type=UnitTypes.stationary,
             ),
          ],
          'buildings': [
             Building(
                id='0_bld',
                belligerent=Belligerents.red,
                code='Tent_Pyramid_US',
                pos=Point2D(43471.34, 57962.08),
                rotation_angle=270.00,
             ),
          ],
          'cameras': [
             StaticCamera(
                belligerent=Belligerents.blue,
                pos=Point3D(38426.0, 65212.0, 35.0),
             ),
          ],
          'markers': [
             FrontMarker(
                id='FrontMarker0',
                belligerent=Belligerents.red,
                pos=Point2D(7636.65, 94683.02),
             ),
          ],
          'rockets': [
             Rocket(
                id='0_Rocket',
                code='Fi103_V1_ramp',
                belligerent=Belligerents.blue,
                pos=Point2D(84141.38, 114216.82),
                rotation_angle=0.00,
                delay=60.0,
                count=10,
                period=80.0,
                destination=Point2D(83433.91, 115445.49),
             ),
          ],
       },
    }


location_loader
---------------

Contains name of location loader which is defined in :doc:`sections/main`.
Usually this element is always present.


player
------

Contains a :class:`dict` with information about player which is defined in
:doc:`sections/main`. Usually this element is always present.


targets
-------

Contains a list of targets which are defined in :doc:`sections/target`.


conditions
----------

Contains a :class:`dict` with information about different conditions in
mission:


time_info
^^^^^^^^^

A :class:`dict` with information about date and time from :doc:`sections/main`
and :doc:`sections/season`.


meteorology
^^^^^^^^^^^

A :class:`dict` with information about meteorology from :doc:`sections/main`
and :doc:`sections/weather`.


scouting
^^^^^^^^

A :class:`dict` with information about scouting from :doc:`sections/mds`. Can
also contain lists of scouts separately per each belligerent
(see :doc:`sections/mds-scouts`).


respawn_time
^^^^^^^^^^^^

Contains result of parsing :doc:`sections/respawn-time`.


radar
^^^^^

Contains common settings for radars from :doc:`sections/mds`.


communication
^^^^^^^^^^^^^

Contains common communication settings from :doc:`sections/mds`.


home_bases
^^^^^^^^^^

Contains common settings for home bases from :doc:`sections/mds`.


crater_visibility_muptipliers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contains settings for craters visibility from :doc:`sections/mds`.


objects
-------

A :class:`dict` which contains lists of objects defined in mission:


moving_units
^^^^^^^^^^^^

List of moving ground units which is defined in :doc:`sections/chiefs`. Each
unit also contains own route which is defined in :doc:`sections/chief-road`.


flights
^^^^^^^

List of AI flights. Information is taken from
:doc:`Flight info sections <sections/flight-info>` which are listed in
:doc:`sections/wing`. Each flight also contains own route which is defined in
:doc:`sections/flight-route`.


home_bases
^^^^^^^^^^

List of airfields which are defined in
:doc:`BornPlace sections <sections/bornplace>`. Airfields also may contain
information about allowed air forces from
:doc:`BornPlace air forces sections <sections/bornplace-air-forces>` and
information about allowed aircrafts from
:doc:`BornPlace aircrafts sections <sections/bornplace-aircrafts>`.


stationary
^^^^^^^^^^

List of stationary objects defined in :doc:`sections/nstationary`.


buildings
^^^^^^^^^

List of buildings defined in :doc:`sections/buildings`.


cameras
^^^^^^^

List of stationary cameras defined in :doc:`sections/static-camera`.


markers
^^^^^^^

List of frontline markers defined in :doc:`sections/front-marker`.


rockets
^^^^^^^

List of rockets defined in :doc:`sections/rocket`.

.. _file-parser:

File parser
===========

.. note::

  `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%9F%D0%B0%D1%80%D1%81%D0%B5%D1%80-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0-%D0%BC%D0%B8%D1%81%D1%81%D0%B8%D0%B8>`_


:class:`~il2fb.parsers.mission.parsers.FileParser` is responsible for parsing
whole mission files or sequences of strings which look like mission definition.
Instance of exactly this class is used when you call ``parse_mission`` function
(see :doc:`../usage`).


This parser detects sections in the stream of strings, selects a proper parser
for a certain section and combines results from all parser into a single whole.
The output of this parser is a :class:`dict`.

Since many sections are optional (e.g., a list of moving ground units, their
routes, a list of available aircrafts at airfields, etc.) and some sections
may not be available in previous versions of the game (eg, ``MDS``), so
we cannot talk about a clear and predefined structure of parser's result.
To understand what may be in the output, it will be much easier and
clearer to :doc:`use project's demo <../demo>`.

Here we will go through the very principles on which the final result is
formed. It *may* contain the following elements:


.. contents::
    :local:
    :depth: 2
    :backlinks: none


location_loader
---------------

Contains name of location loader which is defined in :doc:`main`. Usually
this element is always present.


player
------

Contains a :class:`dict` with information about player which is defined in
:doc:`main`. Usually this element is always present.


targets
-------

Contains a list of targets which are defined in :doc:`target`.


conditions
----------

Contains a :class:`dict` with information about different conditions in
mission:


time_info
^^^^^^^^^

A :class:`dict` with information about date and time from :doc:`main` and
:doc:`season`.


meteorology
^^^^^^^^^^^

A :class:`dict` with information about meteorology from :doc:`main` and
:doc:`weather`.


scouting
^^^^^^^^

A :class:`dict` with information about scouting from :doc:`mds`. Can also
contain lists of scouts separately per each belligerent
(see :doc:`mds-scouts`).


respawn_time
^^^^^^^^^^^^

Contains result of parsing :doc:`respawn-time`.


radar
^^^^^

Contains common settings for radars from :doc:`mds`.


communication
^^^^^^^^^^^^^

Contains common communication settings from :doc:`mds`.


home_bases
^^^^^^^^^^

Contains common settings for home bases from :doc:`mds`.


crater_visibility_muptipliers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contains settings for craters visibility from :doc:`mds`.


objects
-------

A :class:`dict` which contains lists of objects defined in mission:


moving_units
^^^^^^^^^^^^

List of moving ground units which is defined in :doc:`chiefs`. Each unit also
contains own route which is defined in :doc:`chief-road`.


flights
^^^^^^^

List of AI flights. Information is taken from
:doc:`Flight info sections <flight-info>` which are listed in :doc:`wing`.
Each flight also contains own route which is defined in :doc:`flight-route`.


home_bases
^^^^^^^^^^

List of airfields which are defined in :doc:`BornPlace sections <bornplace>`.
Airfields also may contain information about allowed air forces from
:doc:`BornPlace air forces sections <bornplace-air-forces>` and information
about allowed aircrafts from
:doc:`BornPlace aircrafts sections <bornplace-aircrafts>`.


stationary
^^^^^^^^^^

List of stationary objects defined in :doc:`nstationary`.


buildings
^^^^^^^^^

List of buildings defined in :doc:`buildings`.


cameras
^^^^^^^

List of stationary cameras defined in :doc:`static-camera`.


markers
^^^^^^^

List of frontline markers defined in :doc:`front-marker`.


rockets
^^^^^^^

List of rockets defined in :doc:`rocket`.

.. _rocket-section:

Rocket section
==============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Rocket>`_

:class:`~il2fb.parsers.mission.sections.rocket.RocketSectionParser` is
responsible for parsing ``Rocket`` section. Each line of this section describes
a single launchable rocket.

Section example::

  [Rocket]
    0_Rocket Fi103_V1_ramp 2 84141.38 114216.82 360.00 60.0 10 80.0 83433.91 115445.49
    1_Rocket Fi103_V1_ramp 2 84141.38 114216.82 360.00 60.0 10 80.0

Output example:

.. code-block:: python

  {
      'rockets': [
          Rocket(
              id='0_Rocket',
              code='Fi103_V1_ramp',
              belligerent=Belligerents.blue,
              pos=Point2D(84141.38, 114216.82),
              rotation_angle=360.00,
              delay=60.0,
              count=10,
              period=80.0,
              destination=Point2D(83433.91, 115445.49),
          ),
          Rocket(
              id='1_Rocket',
              code='Fi103_V1_ramp',
              belligerent=Belligerents.blue,
              pos=Point2D(84141.38, 114216.82),
              rotation_angle=360.00,
              delay=60.0,
              count=10,
              period=80.0,
              destination=None,
          ),
      ],
  }


The output of the parser is a :class:`dict` with ``rockets`` item. It contains
a list of dictionaries where each dictionary represents a single rocket.

A line can have 2 optional parameters: ``X`` and ``Y`` destination coordinates.

Let's examine the first line.

``0_Rocket``
  Rocket ID which is given by full mission editor. Contains ``Rocket`` word
  prefixed by a sequence number.

  :Output path: ``id``
  :Output type: :class:`str`
  :Output value: original string value

``Fi103_V1_ramp``
  Code name.

  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value

``2``
  Code number of army the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant

``84141.38``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``114216.82``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``360.00``
  Angle of rotation.

  :Output path: ``rotation_angle``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``60.0``
  Delay (in minutes): this parameter tells how much a rocket have to wait until
  it will be launched.

  :Output path: ``delay``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``10``
  Number of rockets to launch.

  :Output path: ``count``
  :Output type: :class:`int`
  :Output value: original value converted to integer number

``80.0``
  Period of rocket launch.

  :Output path: ``period``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``83433.91``
  Destination X coordinate.

  :Output path: ``destination.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``115445.49``
  Destination Y coordinate.

  :Output path: ``destination.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number


.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L20

.. _front-marker-section:

FrontMarker section
===================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-FrontMarker>`_

:class:`~il2fb.parsers.mission.sections.front_marker.FrontMarkerSectionParser`
is responsible for parsing ``FrontMarker`` section. Each line of this section
describes a single frontline marker.

Section example::

  [FrontMarker]
    FrontMarker0 7636.65 94683.02 1

Output example:

.. code-block:: python

  {
      'markers': [
          FrontMarker(
              id="FrontMarker0",
              belligerent=Belligerents.red,
              pos=Point2D(7636.65, 94683.02),
          ),
      ],
  }


**Description**:

The output of the parser is a :class:`dict` with  ``markers`` item. It contains
a list of dictionaries where each dictionary represents a single frontline
marker.

``FrontMarker0``
  Marker ID which is given by full mission editor. Contains ``FrontMarker``
  word suffixed by a sequence number.

  :Output path: ``id``
  :Output type: :class:`str`
  :Output value: original string value

``7636.65``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``94683.02``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``1``
  Code number of army the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant


.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L21

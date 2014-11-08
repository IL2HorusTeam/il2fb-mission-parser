.. _buildings-section:

Buildings section
=================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Buildings>`_

:class:`~il2fb.parsers.mission.parsers.BuildingsParser` is responsible for
parsing ``Buildings`` section. Each line of this section describes a single
building.

Section example::

  [Buildings]
    0_bld House$Tent_Pyramid_US 1 43471.34 57962.08 630.00

Output example:

.. code-block:: python

  {
      'buildings': [
          Building(
              id='0_bld',
              belligerent=Belligerents.red,
              code='Tent_Pyramid_US',
              pos=Point2D(43471.34, 57962.08),
              rotation_angle=630.00,
          ),
      ],
  }

The result is a :class:`dict` with ``buildings`` item which contains a list of
buildings.

We use `Building structure`_ to store information about buildings.


**Description**:

``0_bld``
  Object ID which is given by full mission editor. Contains ``bld`` word
  prefixed by a sequence number.

  :Output path: ``id``
  :Output type: :class:`str`
  :Output value: original string value

``House$Tent_Pyramid_US``
  Building type (``House``) and code name (``Tent_Pyramid_US``). Type is not
  present in the output because all buildings have type ``house``.

  :Output path: ``code``
  :Output type: :class:`str`
  :Output value: original string value

``1``
  Code number of belligerent the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant

``43471.34``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``57962.08``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``630.00``
  Angle of rotation.

  :Output path: ``rotation_angle``
  :Output type: :class:`float`
  :Output value: original value converted to float number


.. _Building structure: https://github.com/IL2HorusTeam/il2fb-mission-parser/blob/master/il2fb/parsers/mission/structures.py#L61
.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L20

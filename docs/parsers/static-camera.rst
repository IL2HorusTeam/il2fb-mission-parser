.. _static-camera-section:

StaticCamera section
====================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-StaticCamera>`_

:class:`~il2fb.parsers.mission.parsers.StaticCameraParser` is responsible for
parsing ``StaticCamera`` section. Each line of this section describes a single
camera.

Section example::

  [StaticCamera]
    38426 65212 35 2

Output example:

.. code-block:: python

  {
      'cameras': [
          {
              'belligerent': Belligerents.blue,
              'pos': {
                  'x': 38426.0,
                  'y': 65212.0,
                  'z': 35.0,
              },
          },
      ],
  }

**Description**:

The output of the parser is a dictionary with a single item. It is accessible by
``cameras`` key. The value is a list of dictionaries. Each dictionary represents
a single camera.

``38426``
  X coordinate.

  :Output path: ``pos.x``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``65212``
  Y coordinate.

  :Output path: ``pos.y``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``35``
  Z coordinate.

  :Output path: ``pos.z``
  :Output type: :class:`float`
  :Output value: original value converted to float number

``2``
  Code number of army the object belongs to.

  :Output path: ``belligerent``
  :Output type: complex `belligerents`_ constant


.. _belligerents: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L17

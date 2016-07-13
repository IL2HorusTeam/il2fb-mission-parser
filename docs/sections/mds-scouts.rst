.. _mds-scouts-section:

MDS_Scouts section
==================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-MDS_Scouts>`_

:class:`~il2fb.parsers.mission.sections.mds.MDSScoutsSectionParser` is
responsible for parsing sections which starts with ``MDS_Scouts_`` prefix.
Those sections define lists of aircrafts which can be used as scouts.

There are two known sections:

#. ``MDS_Scouts_Red``
#. ``MDS_Scouts_Blue``

Each line of those sections contains a code name of an aircraft.

Section example::

    [MDS_Scouts_Red]
      B-25H-1NA
      B-25J-1NA
      BeaufighterMk21

Output example:

.. code-block:: python

    {
        'scouts_red': {
          'belligerent': Belligerents.red,
          'aircrafts': [
              "B-25H-1NA",
              "B-25J-1NA",
              "BeaufighterMk21",
          ],
        }
    }

Output contains a dictionary with a single value. It can be accessed by
``scouts_{suffix}`` key, where ``suffix`` is original suffix, converted to
lower case. So, possible keys are:

#. ``scouts_red``
#. ``scouts_blue``

The value itself is also a dictionary, which contains a list of aircraft code
names and a `belligerent`_ constant.


.. _belligerent: https://github.com/IL2HorusTeam/il2fb-commons/blob/master/il2fb/commons/organization.py#L21

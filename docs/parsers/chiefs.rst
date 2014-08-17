.. _chiefs-section:

Chiefs section
==============

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%A1%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-Chiefs>`_

:class:`~il2fb.parsers.mission.parsers.ChiefsParser` is responsible for parsing
``Chiefs`` section. It describes moving objects or their groups. Each of them is
defined on a separate line. There are 4 types of moving objects:

#. usual vehicles;
#. armored vehicles;
#. trains;
#. ships.

First 3 types have same list of parameters. Ships have some extra parameters.

Section example::

    [Chiefs]
      0_Chief Armor.1-BT7 2
      1_Chief Vehicles.GAZ67 1
      2_Chief Trains.USSR_FuelTrain/AA 1
      3_Chief Ships.G5 1 60 3 2.0


Output example:

.. code-block:: python

    {
        'chiefs': [
            {
                'code': "0_Chief",
                'code_name': "1-BT7",
                'type': "armor",
                'belligerent': <constant 'Belligerents.blue'>,
            },
            {
                'code': "1_Chief",
                'code_name': "GAZ67",
                'type': "vehicles",
                'belligerent': <constant 'Belligerents.red'>,
            },
            {
                'code': "2_Chief",
                'code_name': "USSR_FuelTrain/AA",
                'type': "trains",
                'belligerent': <constant 'Belligerents.red'>,
            },
            {
                'code': "3_Chief",
                'code_name': "G5",
                'type': "ships",
                'belligerent': <constant 'Belligerents.red'>,
                'timeout': 60,
                'skill': <constant 'Skills.ace'>,
                'recharge_time': 2.0,
            },
        ],
    }

**Description**:

.. todo:: write description

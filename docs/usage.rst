Usage
=====

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%98%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5>`_

The main purpose of this library is to parse a whole mission file.


Parse by file name
------------------

The most common usage case is to give path to a mission file and get a parsed
result:

.. code-block:: python

    >>> from il2fb.parsers.mission import parse_mission
    >>> mission = parse_mission("path/to/your/mission.mis")

This will put a big dictionary into a ``mission`` variable. That's it. You do
not need to do something else.


Parse sequence of lines
-----------------------

``parse_mission`` function can accept not only a path to a file, but any object
which can generate a sequence of lines: a text file, list, generator and so on.
For example:

.. code-block:: python

    >>> from il2fb.parsers.mission import parse_mission
    >>> with open("path/to/your/mission.mis") as f:
    ...     mission = parse_mission(f)

Or:

.. code-block:: python

    >>> lines = [
    ...     "[Wing]",
    ...     "  r0100",
    ...     "[r0100]",
    ...     "  Planes 1",
    ...     "  Skill 1",
    ...     "  Class air.A_20C",
    ...     "  Fuel 100",
    ...     "  weapons default",
    ... ]
    >>> mission = parse_mission(lines)


Dealing with result
-------------------

Since the output dictionary can be really big and complex, it's recommended to
use `t_dict`_ or `aadict`_ library to make access to elements of result easier.

You can go forward to :doc:`description of output format <parsers/file-parser>`
to get to know what is contained inside ``mission`` or you can continue reading
this chapter.


Behind the scene
----------------

Let's talk about what's going on above. This library provides a Python module
called :mod:`il2fb.parsers.mission.parsers` which has a lot of parsers for each
kind of section in mission files (see :doc:`all of them <section-parsing>`).

The function ``parse_mission``, which was used in the example above, is a
reference to :meth:`~il2fb.parsers.mission.MissionParser.parse` method
which belongs to an instanse of :class:`~il2fb.parsers.mission.MissionParser`.
This parser just like a swiss-knife combines all of the other parsers in
itself, processes the whole mission file and gives all you need at one time.

You can use any other parser separately for your needs also (see below).


Manual section parsing
----------------------

Each parser listed in :doc:`section-parsing` (except ``MissionParser``) extends an
abstract class :class:`~il2fb.parsers.mission.parsers.SectionParser`, so they
share a common approach for section processing.

.. note::

    Since these parsers were designed to be used by the ``MissionParser``, which
    is a one-pass parser, they can parse only one line at a time. It's just a
    side-effect that you can use them for your needs.

If you really need to parse some section, you need to prepare string lines
and tell parser the name of section. E.g.:

.. code-block:: python

    >>> lines = [
    ...     "MAP Moscow/sload.ini",
    ...     "TIME 11.75",
    ...     "TIMECONSTANT 1",
    ...     "WEAPONSCONSTANT 1",
    ...     "CloudType 1",
    ...     "CloudHeight 1500.0",
    ...     "player fiLLv24fi00",
    ...     "army 1",
    ...     "playerNum 0",
    ... ]
    >>> from il2fb.parsers.mission.sections import MainSectionParser
    >>> p = MainSectionParser()
    >>> p.start('MAIN')
    True
    >>> for line in lines:
    ...     p.parse_line(line)
    ...
    >>> p.stop()
    {
        'location_loader': 'Moscow/sload.ini',
        'time': {
            'is_fixed': True,
            'value': datetime.time(11, 45),
        },
        'cloud_base': 1500,
        'weather_conditions': <constant 'Conditions.good'>,
        'player': {
            'aircraft_index': 0,
            'belligerent': <constant 'Belligerents.red'>,
            'fixed_weapons': True,
            'flight_id': 'fiLLv24fi00',
        },
    }


As you can see, you need to import a desired parser and create it's instance.

Then you need to :meth:`~il2fb.parsers.mission.parsers.SectionParser.start`
parser and provide a name of section you are going to parse. Method will return
``True`` if parser can handle sections with the given name or ``False``
otherwise.

.. note::

    section names can contain prefixes and suffixes such as ``0_*`` or ``*_0``.
    They can have dynamic values and they can be used as a part of output
    result, so we cannot make strict mapping of section names to parsers.
    That's why each parser checks whether it can handle sections with a given
    name.

Now it's a time to feed the parser with some data. As it was mentioned above,
you can pass only one line at a time to
:meth:`~il2fb.parsers.mission.parsers.SectionParser.parse_line` method. You can
do it in any suitable manner.

When you have passed all the data, call
:meth:`~il2fb.parsers.mission.parsers.SectionParser.stop` method to stop
parsing. This method will return fully-parsed data which is a dictionary in
general.


.. _aadict: https://pypi.python.org/pypi/aadict
.. _t_dict: https://pypi.python.org/pypi/t_dict

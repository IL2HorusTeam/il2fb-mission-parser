Usage
=====

The most common usage
^^^^^^^^^^^^^^^^^^^^^

The main purpose of this library is to parse the whole mission file. So, let's
start::

    >>> import il2fb.parsers.mission
    >>> mission = il2fb.parsers.mission.parse('path/to/your/mission.mis')

This will put a big dictionary into a ``mission`` variable. That's it. You do
not need to do something else. Go formard to
:doc:`output format description <parsers/file_parser>` to know what is
contained inside ``mission`` or you can dig around next 2 sections.

Where it comes from
^^^^^^^^^^^^^^^^^^^

Let's talk about what's going on above. This library provides a Python module
called :mod:`il2fb.parsers.mission.parsers` which has a lot of parsers for each
kind of section in mission files (see :doc:`all of them <output_format>`).

The function :func:`~il2fb.parsers.mission.parse`, which was used above, is a
reference to :meth:`~il2fb.parsers.mission.parsers.FileParser.parse` method
which belongs to :class:`~il2fb.parsers.mission.parsers.FileParser`. This parser
as a swiss-knife combines all of the other parsers in itself, processes the
whole mission file and gives all you need in one time. Nevertheless you can use
any other parser for your needs.

Manual parsing
^^^^^^^^^^^^^^

Each parser listed above (except ``FileParser``) extends an abstract class
:class:`~il2fb.parsers.mission.parsers.SectionParser`, so they share a common
approach of section processing.

.. note::

    Since these parsers were designed to be used by the ``FileParser``, which
    is a one-pass parser, they can parse only one line at a time. It's just a
    side-effect that you can use them for your needs.

If you really need to parse some section, you need to prepare string lines
and tell parser the name of section. E.g.::

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
    >>> from il2fb.parsers.mission.parsers import MainParser
    >>> p = MainParser()
    >>> p.start('MAIN')
    True
    >>> for line in lines:
    ...     p.parse_line(line)
    ...
    >>> p.stop()
    {
        'fixed_time': True,
        'clouds_height': 1500.0,
        'army': 'red',
        'time': datetime.time(11, 45),
        'player_num': '0',
        'fixed_weapon': True,
        'weather_type': 'clear',
        'player_regiment': 'fiLLv24fi00',
        'loader': 'Moscow/sload.ini'
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
:meth:`~il2fb.parsers.mission.parsers.SectionParser.parse_line` method. you can
do it in any suitable manner.

When you have passed all the data, call
:meth:`~il2fb.parsers.mission.parsers.SectionParser.stop` method to stop
parsing. This method will return fully-parsed data which is a dictionary in
general.

# coding: utf-8

import six

from abc import ABCMeta, abstractmethod


class SectionParser(six.with_metaclass(ABCMeta)):
    """
    Abstract base parser of a single section in a mission file.

    A common approach to parse a section can be described in the following way:

    #. Pass a section name (e.g. 'MAIN') to :meth:`start` method. If parser can
       process a section with such name, it will return `True` and then you can
       proceed.
    #. Pass section lines one-by-one to :meth:`parse_line`.
    #. When you are done, get your parsed data by calling :meth:`stop`. This
       will tell the parser that no more data will be given and the parsing can
       be finished.

    |
    **Example**:

    .. code-block:: python

       section_name = "Test section"
       lines = ["foo", "bar", "baz", "qux", ]
       parser = SomeParser()

       if parser.start(section_name):
           for line in lines:
              parser.parse_line(line)
           result = parser.stop()

    """
    #: Tells whether a parser was started.
    running = False

    #: An internal buffer which can be redefined.
    data = None

    def start(self, section_name):
        """
        Try to start a parser. If a section with given name can be parsed, the
        parser will initialize it's internal data structures and set
        :attr:`running` to `True`.

        :param str section_name: a name of section which is going to be parsed

        :returns: `True` if section with a given name can be parsed by parser,
                  `False` otherwise
        :rtype: :class:`bool`
        """
        result = self.check_section_name(section_name)
        if result:
            self.running = True
            self.init_parser(section_name)
        return result

    @abstractmethod
    def check_section_name(self, section_name):
        """
        Check whether a section with a given name can be parsed.

        :param str section_name: a name of section which is going to be parsed

        :returns: `True` if section with a given name can be parsed by parser,
                  `False` otherwise
        :rtype: :class:`bool`
        """

    @abstractmethod
    def init_parser(self, section_name):
        """
        Abstract method which is called by :meth:`start` to initialize
        internal data structures.

        :param str section_name: a name of section which is going to be parsed

        :returns: ``None``
        """

    @abstractmethod
    def parse_line(self, line):
        """
        Abstract method which is called manually to parse a line from mission
        section.

        :param str line: a single line to parse

        :returns: ``None``
        """

    def stop(self):
        """
        Stops parser and returns fully processed data.

        :returns: a data structure returned by :meth:`clean` method

        :raises RuntimeError: if parser was not started
        """
        if not self.running:
            raise RuntimeError("Cannot stop parser which is not running")

        self.running = False
        return self.clean()

    def clean(self):
        """
        Returns fully parsed data. Is called by :meth:`stop` method.

        :returns: a data structure which is specific for every subclass
        """
        return self.data


class ValuesParser(six.with_metaclass(ABCMeta, SectionParser)):
    """
    This is a base class for parsers which assume that a section, which is
    going to be parsed, consists of key-value pairs with unique keys, one pair
    per line.

    **Section definition example**::

       [section name]
       key1 value1
       key2 value2
       key3 value3
    """

    def init_parser(self, section_name):
        """
        Implements abstract method. See :meth:`SectionParser.init_parser` for
        semantics.

        Initializes a dictionary to store raw keys and their values.
        """
        self.data = {}

    def parse_line(self, line):
        """
        Implements abstract method. See :meth:`SectionParser.parse_line` for
        semantics.

        Splits line into key-value pair and puts it into internal dictionary.
        """
        key, value = line.strip().split(' ', 1)
        self.data.update({key: value})


class CollectingParser(six.with_metaclass(ABCMeta, SectionParser)):
    """
    This is a base class for parsers which assume that a section, which is
    going to be parsed, consists of homogeneous lines which describe different
    objects with one set of attributes.

    **Section definition example**::

       [section name]
       object1_attr1 object1_attr2 object1_attr3 object1_attr4
       object2_attr1 object2_attr2 object2_attr3 object2_attr4
       object3_attr1 object3_attr2 object3_attr3 object3_attr4
    """

    def init_parser(self, section_name):
        """
        Implements abstract method. See :meth:`SectionParser.init_parser` for
        semantics.

        Initializes a list for storing collection of objects.
        """
        self.data = []

    def parse_line(self, line):
        """
        Implements abstract method. See :meth:`SectionParser.parse_line` for
        semantics.

        Just puts entire line to internal buffer. You probably will want to
        redefine this method to do some extra job on each line.
        """
        self.data.append(line.strip())

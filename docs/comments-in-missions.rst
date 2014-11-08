Comments in missions
====================

.. note::

    `Russian version <https://github.com/IL2HorusTeam/il2fb-mission-parser/wiki/%D0%9A%D0%BE%D0%BC%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%80%D0%B8%D0%B8-%D0%B2-%D1%84%D0%B0%D0%B9%D0%BB%D0%B5-%D0%BC%D0%B8%D1%81%D1%81%D0%B8%D0%B8>`_

As it is known, many creators of missions put some comments and notes for
themselves directly inside mission file.

``il2fb-mission-parser`` treats as comments everything that stands to the right
from the following delimiters including delimiters themselves:

#. ``;``
#. ``#``
#. ``//``
#. ``--``

Example::

  [Target]
    1 2 0 0 750 19750 4275 500 ;0
    1 2 0 0 750 21096 14030 500 #1
    1 2 0 0 750 21971 19014 500 //2
    1 2 0 0 750 17744 27538 500 --3

Comment blocks are not supported.

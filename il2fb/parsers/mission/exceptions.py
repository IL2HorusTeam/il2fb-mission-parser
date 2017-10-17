# coding: utf-8

from il2fb.commons.exceptions import IL2FBParsingException


class MissionParsingError(IL2FBParsingException):
    """
    Raised when parsing of mission file meets unexpected condition.

    """

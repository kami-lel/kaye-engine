"""
abbr_tags.py

define ``AbbrTags``
"""

from enum import Flag, auto


class AbbrTags(Flag):
    """
    represent **abbreviation tags** as a *bit flag*
    """

    # pylint: disable=invalid-name

    # flag instances  ==========================================================

    NONE = 0
    common = auto()
    always_understand = auto()

    # character set  -----------------------------------------------------------

    single_character = auto()
    letters_only = auto()
    word_character_only = auto()
    ascii_only = auto()
    emoji = auto()

    WORD_CHARACTER = letters_only | word_character_only
    ASCII = WORD_CHARACTER | ascii_only

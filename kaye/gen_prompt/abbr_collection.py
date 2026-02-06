"""
define various data structure supporting **abbreviation nodes**
"""

from enum import Flag, auto

__all__ = ("AbbrTags",)


class AbbrTags(Flag):  #########################################################
    """
    represent **abbreviation tags** as a *bit flag*
    """

    # pylint: disable=invalid-name

    # classmethods  ============================================================

    @classmethod
    def parse(cls, tags_list):
        """
        parse **tags** as they appeared in ``abbrs.json``,
        which occurs under each entry of ``"abbrs"`` and ``"alt"``
        with key of ``"tags"``, e.g::


        :param tags_list: v.s.
        :type tags_list: list[str]
        :raises ValueError:
        :return: parsed tags
        :rtype: AbbrEntry
        """
        instance = cls.NONE  # start
        for tag in tags_list:
            try:
                instance |= AbbrTags[tag]  # may raise KeyError
            except KeyError as err:
                raise ValueError(
                    "fail to parse {} as an abbr tag".format(repr(tag))
                ) from err

        return instance

    # flag instances  ==========================================================

    NONE = 0
    common = auto()
    programming_language = auto()

    # contains only letter with no other types of characters
    letters_only = auto()

    # contains only word character with no punctuations etc.
    word_character_only = auto()

    # contains only ASCII characters
    ascii_only = auto()
    emoji = auto()

    WORD_CHARACTER = letters_only | word_character_only
    ASCII = WORD_CHARACTER | ascii_only

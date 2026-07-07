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
        if not isinstance(tags_list, list):
            raise ValueError(
                "tags value must be Array: {}".format(repr(tags_list))
            )

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

    # usage cases  -------------------------------------------------------------

    always_understand = auto()
    usable_in_brief = auto()
    coding = auto()

    # specialized groups  ------------------------------------------------------

    programming_language_code = auto()
    language_code = auto()
    unity_engine_abbr = auto()
    log_level = auto()
    unit_of_measure = auto()
    currency_symbol = auto()

    # character set  -----------------------------------------------------------

    single_character = auto()
    letters_only = auto()
    word_character_only = auto()
    ascii_only = auto()
    emoji = auto()

    WORD_CHARACTER = letters_only | word_character_only
    ASCII = WORD_CHARACTER | ascii_only

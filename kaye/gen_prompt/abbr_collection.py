"""
define various data structure supporting **abbreviation nodes**
"""

import re

from enum import Enum, Flag, auto

__all__ = ("AbbrTags", "AbbrWrap")


class AbbrData:  ###############################################################
    """
    represents collections of all abbreviation read from ``abbrs.json`


    :example:
    >>> instance = AbbrData()
    """

    # singleton pattern  =======================================================

    _instance = None  # singleton

    def __new__(cls, *, abbrs_json_override=None):
        if cls._instance is None or abbrs_json_override:
            cls._instance = super().__new__(cls)
            cls._instance._load_abbrs_json(
                abbrs_json_override=abbrs_json_override
            )
        return cls._instance

    def _load_abbrs_json(self, *, abbrs_json_override=None):
        """
        load from ``abbrs.json`` to create

        - ``self.meanings``
        - ``self.abbrs``
        - ``self.automation``


        :raises json.JSONDecodeError:
        :raises ValueError:
        """
        # pylint: disable=attribute-defined-outside-init


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


class AbbrWrap(Enum):  #########################################################
    """
    represent an abbr wrap type as ``Enum``
    """

    # enum instances  ==========================================================

    WORD = "word"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    SYMBOL = "symbol"

    # instance methods  ========================================================

    def is_satisfied_wrap_rule(self, char_before, char_after):
        """
        :param char_before: single character immediately before the found;
                `""` if start of text
        :type char_before: str
        :param char_after: single character immediately after the found;
                `""` if end of text
        :type char_after: str
        """

        if self == AbbrWrap.WORD:
            return WORD_BOUNDARY_PATTERN.fullmatch(
                char_before
            ) and WORD_BOUNDARY_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.PREFIX:
            return WORD_BOUNDARY_PATTERN.fullmatch(
                char_before
            ) and WORD_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.SUFFIX:
            return WORD_PATTERN.fullmatch(
                char_before
            ) and WORD_BOUNDARY_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.SYMBOL:
            return True

        raise NotImplementedError


# patterns  --------------------------------------------------------------------
WORD_BOUNDARY_PATTERN = re.compile(r"\s|[^\w\s]?")
WORD_PATTERN = re.compile(r"\w")


class AbbrMeaning:
    """
    represent a single meaning (of possible different spellings)


    :param mean:
    :type mean: str
    """

    __slots__ = ("mean",)

    def __init__(self, mean):
        self.mean = mean

    # magic methods  ===========================================================

    def __hash__(self):
        return hash(self.mean)


class AbbrEntry:  # TODO
    pass

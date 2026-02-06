"""
define various data structure supporting **abbreviation nodes**
"""

import re
import json
from pathlib import Path
from enum import Enum, Flag, auto

__all__ = ("AbbrTags", "AbbrWrap", "AbbrData")


ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"


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

    # load from abbrs.json  ====================================================
    def _load_abbrs_json(self, *, abbrs_json_override=None):
        """
        load from ``abbrs.json`` to create

        - ``self.meanings``
        - ``self.abbrs``
        - ``self.automaton``


        :raises json.JSONDecodeError:
        :raises ValueError:
        """
        # pylint: disable=attribute-defined-outside-init

        # read abbrs.json  -----------------------------------------------------
        if abbrs_json_override:
            json_data = abbrs_json_override

        else:
            with open(
                ABBRS_JSON_FILE_PATH, "r", encoding="utf-8"
            ) as f:  # read only
                try:
                    json_data = json.load(f)
                except json.JSONDecodeError as err:
                    raise json.JSONDecodeError(
                        "fail to parse abbrs.json: " + err.msg,
                        err.doc,
                        err.pos,
                    ) from err

        # fill .meanings & .abbrs  ---------------------------------------------
        self.meanings = []
        self.abbrs = []
        for mean_key, mean_obj in json_data.items():
            mean = AbbrMeaning(mean_key)
            self.meanings.append(mean)

            for abbr, abbr_obj in mean_obj.items():
                self.abbrs.append(AbbrEntry(mean, abbr, abbr_obj))

        # create automaton  ----------------------------------------------------
        # TODO


class AbbrMeaning:  # **********************************************************
    """
    represent a single meaning (of possible different spellings)


    :param mean:
    :type mean: str
    :raises ValueError:
    """

    __slots__ = ("mean",)

    def __init__(self, mean):
        if not isinstance(mean, str):
            raise ValueError(
                "meaning key must be String: {}".format(repr(mean))
            )

        self.mean = mean

    # magic methods  ===========================================================

    def __hash__(self):
        return hash(self.mean)


class AbbrEntry:  # ************************************************************

    __slots__ = ("abbr", "mean", "wrap", "tags")

    def __init__(self, mean, abbr, abbr_obj):
        self.mean = mean  # referenced to meaning

        # test shapes  ---------------------------------------------------------
        if not isinstance(abbr, str):
            raise ValueError("abbr key must be String: {}".format(repr(abbr)))

        if not isinstance(abbr_obj, dict):
            raise ValueError(
                "abbr value must be Object: {}".format(repr(abbr_obj))
            )

        missing_keys = [
            key for key in ("priority", "tags", "wrap") if key not in abbr_obj
        ]
        if missing_keys:
            raise ValueError(
                "abbr value must contains key: {}".format(missing_keys)
            )

        # TODO TODO create

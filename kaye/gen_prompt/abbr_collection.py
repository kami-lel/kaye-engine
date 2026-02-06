"""
define various data structure supporting **abbreviation nodes**
"""

import re
import json
from pathlib import Path
from enum import Enum, Flag, auto

import ahocorasick

__all__ = ("AbbrTags", "AbbrWrap", "AbbrData")


# abbrs.json constants  ########################################################
ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"
ABBRS_JSON_PRIORITY_KEY = "priority"
ABBRS_JSON_TAGS_KEY = "tags"
ABBRS_JSON_WRAP_KEY = "wrap"


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

        if abbrs_json_override:
            json_data = abbrs_json_override

        else:
            # read abbrs.json  -------------------------------------------------
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
        # todo use pickle.loads/dumps to save an local automaton, with hash
        # pylint: disable=c-extension-no-member
        self.automaton = ahocorasick.Automaton()
        for entry in self.abbrs:
            self.automaton.add_word(entry.abbr, entry)
        self.automaton.make_automaton()


class AbbrMeaning:  # **********************************************************
    """
    represent a single meaning (of possible different spellings)


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

    def __eq__(self, other):
        if not isinstance(other, AbbrEntry):
            return NotImplemented

        return self.mean == other.mean

    def __str__(self):
        return self.mean


class AbbrEntry:  # ============================================================
    """
    represent an abbr => meaning structure


    :raises ValueError:
    """

    # instance structure  ******************************************************

    __slots__ = ("abbr", "mean", "priority", "tags", "wrap")

    def __init__(self, mean, abbr, abbr_obj):
        self.mean = mean  # referenced to meaning

        # set .abbr  -----------------------------------------------------------
        if not isinstance(abbr, str):
            raise ValueError("abbr key must be String: {}".format(repr(abbr)))
        self.abbr = abbr

        # test abbr_obj shapes  ------------------------------------------------
        if not isinstance(abbr_obj, dict):
            raise ValueError(
                "abbr value must be Object: {}".format(repr(abbr_obj))
            )
        missing_keys = [
            key
            for key in (
                ABBRS_JSON_PRIORITY_KEY,
                ABBRS_JSON_TAGS_KEY,
                ABBRS_JSON_WRAP_KEY,
            )
            if key not in abbr_obj
        ]
        if missing_keys:
            raise ValueError(
                "abbr value must contains key: {}".format(missing_keys)
            )

        # set .priority  -------------------------------------------------------
        priority = abbr_obj[ABBRS_JSON_PRIORITY_KEY]
        if not isinstance(priority, int):
            raise ValueError(
                "priority must be Integer: {}".format(repr(priority))
            )
        self.priority = priority

        # set .tags  -----------------------------------------------------------
        self.tags = AbbrTags.parse(abbr_obj[ABBRS_JSON_TAGS_KEY])

        # set .wrap  -----------------------------------------------------------
        # may raise ValueError
        self.wrap = AbbrWrap(abbr_obj[ABBRS_JSON_WRAP_KEY])

    # instance method  *********************************************************

    def verify_found(self, found, char_before, char_after):
        """
        :param found:
        :type found: str
        :param char_before: single character immediately before the found;
                `""` if start of text
        :type char_before: str
        :param char_after: single character immediately after the found;
                `""` if end of text
        :type char_after: str
        :return: whether ``found`` satisfies additional rules of:

        - case sensitivity
        - wrapping

        :rtype: bool
        """
        return (
            self.abbr.islower() or found == self.abbr  # verify case sensitivity
        ) and self.wrap.is_satisfied_wrap_rule(char_before, char_after)

    # magic methods  ***********************************************************

    def __hash__(self):
        key = (self.abbr, self.mean)
        return hash(key)

    def __eq__(self, other):
        if not isinstance(other, AbbrEntry):
            return NotImplemented

        return self.abbr == other.abbr and self.mean == other.mean

    def __repr__(self):
        return "{}:{}".format(self.abbr, self.mean)

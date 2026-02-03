# pylint: disable=c-extension-no-member

from pathlib import Path
from enum import Flag, Enum, auto
from itertools import chain
import json

import ahocorasick

from .prompt_blueprint import PromptBlueprint

ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"

__all__ = ("DynamicAbbrBlueprint",)


# constants  ###################################################################
ABBRS_KEY = "abbrs"
ALT_KEY = "alts"
MEAN_KEY = "mean"
ABBR_KEY = "abbr"
WRAP_KEY = "wrap"
TAGS_KEY = "tags"


class DynamicAbbrBlueprint(PromptBlueprint):  #################################

    _automaton = None
    _entries = None

    # load abbrs  ==============================================================
    @classmethod
    def load_abbrs_json(cls, *, abbrs_json_file_path_override=None):
        if cls._entries is not None:
            return  # load once, thus skip loading

        # read abbrs.json  -----------------------------------------------------
        file_path = abbrs_json_file_path_override or ABBRS_JSON_FILE_PATH
        with open(file_path, "r", encoding="utf-8") as f:  # read only
            try:
                data = json.load(f)
            except json.JSONDecodeError as err:
                raise json.JSONDecodeError(
                    "fail to parse abbrs.json: " + err.msg,
                    err.doc,
                    err.pos,
                ) from err

        if not all(key in data for key in (ABBRS_KEY, ALT_KEY)):
            raise ValueError("abbrs.json must contains 'abbrs' and 'alt'")

        abbrs_obj = data[ABBRS_KEY]
        alts_obj = data[ALT_KEY]

        # create entries  ------------------------------------------------------
        cls._entries = []
        # add all abbr entries
        for k, v in abbrs_obj.items():
            cls._entries.append(AbbrEntry.parse_from_abbr(k, v))
        # add all alt entries
        for k, v in alts_obj.items():
            cls._entries.append(AbbrEntry.parse_from_alt(k, v, abbrs_obj))

        # create automation  ---------------------------------------------------
        # init Aho–Corasick automation
        cls._automaton = ahocorasick.Automaton()

        for key, _ in chain(data[ABBRS_KEY].items(), data[ALT_KEY].items()):
            try:
                cls._automaton.add_word(key, key)
            except KeyError as err:
                raise err  # TODO

    # instance method  =========================================================
    def generate_prompt(
        self, *, hide_comment=False, query=None, add_usable_abbr=False
    ):
        self.__class__.load_abbrs_json()

        content, comment = self._generate_prompt_split_content_and_comment(
            hide_comment
        )

        # TODO query based generation
        if query:
            abbr_content = ""
        else:
            abbr_content = ""

        return content + abbr_content + comment


class AbbrEntry:  ##############################################################
    """
    present a *unified* data structure to represent
    either ``"abbr"`` or ``"alt"`` object in ``abbrs.json``

    for ``"alt"`` object, its meaning must be dereferenced
    and store directly w/i the AbbrEntry


    :param key:
    :type key: str
    :param mean:
    :type mean: str
    :param wrap: raw wrap string stored in ``abbrs.json``
    :type wrap: str
    :param tags_list: raw tags list stored in ``abbrs.json``
    :type tags_list: list[str]
    :raises ValueError:
    :raises TypeError:
    """

    @classmethod
    def parse_from_abbr(cls, key, abbr_obj):
        """
        parsing an **abbr** object read from ``abbrs.json``


        :param key:
        :type key: str
        :param abbr_obj:
        :type abbr_obj: dict{str: str}
        :raises ValueError:
        :raises TypeError:
        :return: parsed legal ``AbbrEntry``
        :rtype: AbbrEntry
        """
        try:
            mean = abbr_obj[MEAN_KEY]
            wrap = abbr_obj[WRAP_KEY]
            tags_list = abbr_obj[TAGS_KEY]
            # may raise ValueError/TypeError
            return AbbrEntry(key, mean, wrap, tags_list)

        except KeyError as err:
            raise ValueError(
                "abbr_obj missing key {}: {}".format(
                    repr(err.args[0]), repr(abbr_obj)
                )
            ) from err

    @classmethod
    def parse_from_alt(cls, key, alt_obj, abbrs_obj):
        # BUG req unit test
        try:
            wrap = alt_obj["wrap"]
            tags_list = alt_obj["tags"]

            abbr = alt_obj["abbr"]

        except KeyError as err:
            raise ValueError(
                "alt {} is malformed: {}\n{}".format(
                    repr(key), err.args[0], alt_obj
                )
            ) from err

        try:
            # find mean based on abbr entry
            mean = abbrs_obj[abbr]["mean"]
        except KeyError as err:
            raise ValueError(
                "fail to find alt {}'s corresponding abbr {}".format(
                    repr(key), repr(abbr)
                )
            ) from err

        return AbbrEntry(key, mean, wrap, tags_list)

    __slots__ = ("key", "mean", "wrap", "tags")

    def __init__(self, key, mean, wrap, tags_list):
        if not isinstance(key, str):
            raise TypeError("arg key must be str: {}".format(repr(key)))
        self.key = key

        if not isinstance(mean, str):
            raise TypeError("arg mean must be str: {}".format(repr(mean)))
        self.mean = mean

        self.wrap = AbbrWrap(wrap)  # may raise ValueError
        self.tags = AbbrTags.parse(tags_list)  # may raise ValueError/TypeError


class AbbrWrap(Enum):  ########################################################
    """
    represent an abbr wrap type as ``Enum``
    """

    WORD = "word"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    SYMBOL = "symbol"

    def check(self):
        pass  # TODO


class AbbrTags(Flag):  ########################################################
    """
    represent **abbreviation tags** as a *bit flag*
    """

    # pylint: disable=invalid-name

    NONE = auto()
    ascii = auto()
    usable = auto()
    emoji = auto()
    programming_language = auto()

    @classmethod
    def parse(cls, tags_list):
        """
        parse **tags** as they appeared in ``abbrs.json``,
        which occurs under each entry of ``"abbrs"`` and ``"alt"``
        with key of ``"tags"``, e.g::


        :param tags_list: v.s.
        :type tags_list: list[str]
        :raises TypeError:
        :raises ValueError:
        :return: parsed tags
        :rtype: AbbrEntry
        """

        # type guard
        if not (
            isinstance(tags_list, list)
            and all(isinstance(v, str) for v in tags_list)
        ):
            raise TypeError(
                "arg tags_list must list of str: {}".format(repr(tags_list))
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

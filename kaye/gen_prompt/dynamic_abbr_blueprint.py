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
JSON_ABBRS_KEY = "abbrs"
JSON_ALT_KEY = "alt"


class DynamicAbbrBlueprint(PromptBlueprint):

    _automaton = None
    _entries = None

    # load abbrs  ==============================================================
    @classmethod
    def load_abbrs_json(cls, *, abbrs_json_file_path_override=None):
        if cls._entries is not None:
            return  # load once, thus skip loading

        # read abbrs.json  *****************************************************
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

        if not all(key in data for key in (JSON_ABBRS_KEY, JSON_ALT_KEY)):
            raise ValueError("abbrs.json must contains 'abbrs' and 'alt'")

        abbrs_obj = data[JSON_ABBRS_KEY]
        alts_obj = data[JSON_ALT_KEY]

        # create entries  ******************************************************
        cls._entries = []
        # add all abbr entries
        for k, v in abbrs_obj.items():
            cls._entries.append(_AbbrEntry.parse_from_abbr(k, v))
        # add all alt entries
        for k, v in alts_obj.items():
            cls._entries.append(_AbbrEntry.parse_from_alt(k, v, abbrs_obj))

        # create automation  ***************************************************
        # init Aho–Corasick automation
        cls._automaton = ahocorasick.Automaton()

        for key, _ in chain(
            data[JSON_ABBRS_KEY].items(), data[JSON_ALT_KEY].items()
        ):
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


class _AbbrEntry:

    __slots__ = ("key", "mean", "wrap", "tags")

    @classmethod
    def parse_from_abbr(cls, key, abbr_obj):
        """
        :param key: _description_
        :type key: _type_
        :param abbr_obj: _description_
        :type abbr_obj: _type_
        :raises ValueError:
        :return: _description_
        :rtype: _type_
        """
        try:
            mean = abbr_obj["mean"]
            wrap = abbr_obj["wrap"]
            tags_list = abbr_obj["tags"]
            return _AbbrEntry(key, mean, wrap, tags_list)

        except KeyError as err:
            raise ValueError(
                "abbr {} is malformed: {}\n{}".format(
                    repr(key), err.args[0], abbr_obj
                )
            ) from err

    @classmethod
    def parse_from_alt(cls, key, alt_obj, abbrs_obj):
        """
        :param key: _description_
        :type key: _type_
        :param alt_obj: _description_
        :type alt_obj: _type_
        :param abbrs_obj: _description_
        :type abbrs_obj: _type_
        :raises ValueError:
        :return: _description_
        :rtype: _type_
        """
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

        return _AbbrEntry(key, mean, wrap, tags_list)

    def __init__(self, key, mean, wrap, tags_list):
        self.key = key
        self.mean = mean
        self.wrap = _AbbrWrap(wrap)  # TODO error handling
        self.tags = AbbrTags.parse(tags_list)


class _AbbrWrap(Enum):

    WORD = "word"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    SYMBOL = "symbol"

    def check(self):
        pass  # TODO


class AbbrTags(Flag):
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
        :raises KeyError:
        :return: parsed tags
        :rtype: _AbbrEntry
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

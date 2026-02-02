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

        # create entries  ******************************************************

        # TODO load data

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

        # TODO mpl add usable abbr
        content, comment = self._generate_prompt_split_content_and_comment(
            hide_comment
        )

        if query:
            # TODO TODO abbr type (how to interpret the abbr)
            abbr_content = ""
        else:
            abbr_content = ""

        return content + abbr_content + comment


class _AbbrEntry:

    def __init__(self, key, mean, wrap, tags_raw):
        self.key = key
        self.mean = mean
        self.wrap = _AbbrWrap(wrap)  # TODO error handling
        self.tags = _AbbrTags.parse(tags_raw)


class _AbbrWrap(Enum):

    WORD = "word"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    SYMBOL = "symbol"


class _AbbrTags(Flag):

    @classmethod
    def parse(cls, tags_raw):
        return cls.none  # TODO

    none = auto()

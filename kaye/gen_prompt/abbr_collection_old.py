# pylint: disable=c-extension-no-member

from pathlib import Path
from enum import Flag, Enum, auto
import json
import re

import ahocorasick

__all__ = ("AbbrCollection", "AbbrEntry", "AbbrWrap", "AbbrTags")
# BUG new structure


# constants  ###################################################################
# top level key-value
ABBRS_KEY = "abbrs"
ALT_KEY = "alts"
# under "abbrs" object
MEAN_KEY = "mean"
# under "alts" object
ABBR_KEY = "abbr"
# under "abbrs"or "alts" object
WRAP_KEY = "wrap"
TAGS_KEY = "tags"


class AbbrCollection:
    # public API  ==============================================================

    def generate_programming_languages_code(self):
        """
        :yield: all programming language codes entries
        :rtype: AbbrEntry
        """
        for entry in self.entries:
            if AbbrTags.programming_language in entry.tags:
                yield entry

    # TODO more public methods

    # singleton pattern  =======================================================

    _instance = None  # singleton

    # load abbrs from file  ====================================================
    def _load_abbrs_json(self, *, abbrs_json_override=None):
        # read abbrs.json  -----------------------------------------------------
        # create entries  ------------------------------------------------------
        self.entries = []
        # add all abbr entries
        for k, v in abbrs_obj.items():
            entry = AbbrEntry(k, v[MEAN_KEY], v[WRAP_KEY], v[TAGS_KEY])
            self.entries.append(entry)
        # add all alt entries
        for k, v in alts_obj.items():
            self.entries.append(AbbrEntry.parse_from_alt(k, v, abbrs_obj))

        # create automation  ---------------------------------------------------
        self.automaton = ahocorasick.Automaton()
        for entry in self.entries:
            self.automaton.add_word(entry.key, entry)
        # todo use pickle.loads/dumps to save an local automaton, with hash
        self.automaton.make_automaton()

    # helper methods  **********************************************************
    @classmethod
    def _validate_json_data(cls, data):
        if not all(key in data for key in (ABBRS_KEY, ALT_KEY)):
            raise ValueError("abbrs.json must contains 'abbrs' and 'alt'")

        abbrs_obj = data[ABBRS_KEY]
        alts_obj = data[ALT_KEY]

        if not isinstance(abbrs_obj, dict):
            raise ValueError(repr(ABBRS_KEY) + " value must be object")
        if not isinstance(alts_obj, dict):
            raise ValueError(repr(ALT_KEY) + " value must be object")

        # validate entries of abbrs  -------------------------------------------
        for k, v in abbrs_obj.items():
            if not isinstance(k, str):
                raise ValueError(
                    "key must be string within {} object: {}".format(
                        repr(ABBRS_KEY), repr(k)
                    )
                )

            if not isinstance(v, dict):
                raise ValueError(
                    "value must be object within {} object: {}".format(
                        repr(ABBRS_KEY), repr(v)
                    )
                )

            # validate 'mean'
            cls._validate_string_entry(v, MEAN_KEY, ABBRS_KEY)
            # validate 'wrap'
            cls._validate_string_entry(v, WRAP_KEY, ABBRS_KEY)

            cls._validate_tags(v, ABBRS_KEY)

        # validate entries of alts  --------------------------------------------
        for k, v in alts_obj.items():
            if not isinstance(k, str):
                raise ValueError(
                    "key must be string within {} object: {}".format(
                        repr(ALT_KEY), repr(k)
                    )
                )

            if not isinstance(v, dict):
                raise ValueError(
                    "value must be object within {} object: {}".format(
                        repr(ALT_KEY), repr(v)
                    )
                )

            # validate 'abbr'
            cls._validate_string_entry(v, ABBR_KEY, ALT_KEY)
            # validate 'wrap'
            cls._validate_string_entry(v, WRAP_KEY, ALT_KEY)

            cls._validate_tags(v, ALT_KEY)

    @staticmethod
    def _validate_string_entry(entry, key, parent_key):
        if key not in entry:
            raise ValueError(
                "{} object must contains {}".format(parent_key, key)
            )

        if not isinstance(entry[key], str):
            raise ValueError(
                "{} in {} object must be string: {}".format(
                    key, parent_key, repr(entry[key])
                )
            )

    @staticmethod
    def _validate_tags(entry, parent_key):
        if TAGS_KEY not in entry:
            raise ValueError(
                "{} object must contains {}".format(parent_key, TAGS_KEY)
            )

        tags_list = entry[TAGS_KEY]
        if not isinstance(tags_list, list):
            raise ValueError(
                "{} in {} object must be array: {}".format(
                    TAGS_KEY, parent_key, repr(tags_list)
                )
            )

        if not all(isinstance(v, str) for v in tags_list):
            raise ValueError(
                "{} in {} object must contains only string: {}".format(
                    TAGS_KEY, parent_key, repr(tags_list)
                )
            )


class OAbbrEntry:  ##############################################################
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

    # classmethods  ============================================================

    @classmethod
    def parse_from_alt(cls, key, alt_obj, abbrs_obj):
        """
        parsing an *alt* object read from ``abbrs.json``,
        with dereferencing by finding its corresponding abbr from ``abbrs_obj``


        :param key:
        :type key: str
        :param alt_obj:
        :type abbr_obj: dict{str: str}
        :param abbrs_obj:
        :type abbr_obj: dict{str: dict}
        :raises ValueError:
        :return: parsed legal ``AbbrEntry``
        :rtype: AbbrEntry
        """
        abbr = alt_obj[ABBR_KEY]
        wrap = alt_obj[WRAP_KEY]
        tags_list = alt_obj[TAGS_KEY]

        try:
            # find mean based on abbr entry
            referenced_abbr = abbrs_obj[abbr]
        except KeyError as err:
            raise ValueError(
                "fail to find referenced abbr {} of alt {} in abbrs.json"
                .format(repr(abbr), repr(key))
            ) from err

        mean = referenced_abbr[MEAN_KEY]
        return AbbrEntry(key, mean, wrap, tags_list)

    # instance structure  ======================================================

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

    # instance method  =========================================================

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
            self.key.islower() or found == self.key  # verify case sensitivity
        ) and self.wrap.is_satisfied_wrap_rule(char_before, char_after)

    # magic methods  ===========================================================
    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if not isinstance(other, AbbrEntry):
            return NotImplemented
        return self.key == other.key

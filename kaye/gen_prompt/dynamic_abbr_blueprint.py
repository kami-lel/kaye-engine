# pylint: disable=c-extension-no-member

from pathlib import Path
from enum import Flag, Enum, auto
import json

import ahocorasick

from .prompt_blueprint import PromptBlueprint

ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"

__all__ = ("DynamicAbbrBlueprint", "AbbrEntry", "AbbrWrap", "AbbrTags")


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


class DynamicAbbrBlueprint(PromptBlueprint):  #################################

    _automaton = None
    _entries = None

    # load abbrs  ==============================================================
    @classmethod
    def load_abbrs_json(cls, *, abbrs_json_file_path_override=None):
        """
        load class properties ``_automaton`` and ``_entries``
        from file ``abbrs.json``


        :param abbrs_json_file_path_override:
        :type abbrs_json_file_path_override: bool, optional
        :raises json.JSONDecodeError:
        :raises ValueError:
        """
        if not (cls._entries is None or cls._automaton is None):
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
        cls._automaton = ahocorasick.Automaton()
        for i, entry in enumerate(cls._entries):
            cls._automaton.add_word(entry.key, i)
        # todo use pickle.loads/dumps to save an local automaton, with hash
        cls._automaton.make_automaton()

    # instance method  =========================================================
    def generate_prompt(
        self, *, hide_comment=False, query=None, add_usable_abbr=False
    ):
        # Todo add usable abbr
        self.__class__.load_abbrs_json()

        content, comment = self._generate_prompt_split_content_and_comment(
            hide_comment
        )
        abbr_content = self._generate_abbr_content(query)

        return content + abbr_content + comment

    def _generate_abbr_content(self, query):
        if not query:
            return ""

        return ""


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
        try:
            abbr = alt_obj[ABBR_KEY]
            wrap = alt_obj[WRAP_KEY]
            tags_list = alt_obj[TAGS_KEY]

        except KeyError as err:
            raise ValueError(
                "alt_obj missing key {}: {}".format(
                    repr(err.args[0]), repr(alt_obj)
                )
            ) from err

        try:
            # find mean based on abbr entry
            referenced_abbr = abbrs_obj[abbr]
        except KeyError as err:
            raise ValueError(
                "fail to find referenced abbr {} of alt {} in arg abbrs_obj"
                .format(repr(abbr), repr(key))
            ) from err

        mean = referenced_abbr[MEAN_KEY]
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

    NONE = 0
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

"""
exportable_abbr.py

group abbreviations for export
"""

import re

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import (
    AbbrTags,
    AbbrWrap,
    abbr_glossary_registry,
    get_abbr_data,
)
from kaye_engine.exportable import (
    Exportable,
    exportable_registry,
    register_exportable_entry,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# auxiliaries  #################################################################


def _to_skill_name(display_name):
    """
    convert a display name to a kebab-case skill name matching
    Anthropic's skill-name grammar, e.g. ``Abbr Starts with Digits 0~9``
    -> ``abbr-starts-with-digits-0-9``
    """
    return re.sub(r"[^a-z0-9]+", "-", display_name.lower()).strip("-")


# constants  ###################################################################


_ABBR_TEMPLATE = "Abbr "
_GLOSSARY_TEMPLATE = "Glossary "
_START_WITH_TEMPLATE = _ABBR_TEMPLATE + "Starts with "
_START_WITH_DIGIT = _START_WITH_TEMPLATE + "Digits 0~9"
_START_WITH_OTHER = _START_WITH_TEMPLATE + "Non-Alphanumeric"

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LETTERS_SET = frozenset(_LETTERS)
_DIGITS_SET = frozenset("0123456789")

_TAG_NAMES = {
    AbbrTags.single_character: "Single Character",
    AbbrTags.emoji: "Emoji",
}

_WRAP_NAMES = {
    AbbrWrap.PREFIX: "Prefixes",
    AbbrWrap.SUFFIX: "Suffixes",
    AbbrWrap.SYMBOL: "Symbols",
}


class ExportableAbbr(list, Exportable):  #######################################
    """
    a named, iterable group of abbreviation entries; implements
    `Exportable` directly -- the group itself is the entry stored in
    `exportable_registry`, not a wrapper around it

    `Exportable` is a dataclass and `list` is not, so both parents'
    ``__init__`` are called explicitly rather than relying on
    cooperative ``super()``


    :param entries: abbreviation entries for this group
    :param canonical_name: kebab-case name, used directly as the
            exported skill name
    :type canonical_name: str, optional
    :param display_name: human-readable name
    :type display_name: str, optional
    """

    def __init__(
        self,
        entries=(),
        *,
        canonical_name="",
        display_name="",
        always_apply=False,
        user_invokable=False,
        llm_invokable=True,
    ):
        list.__init__(self, entries)
        Exportable.__init__(
            self,
            canonical_name=canonical_name,
            display_name=display_name,
            always_apply=always_apply,
            user_invokable=user_invokable,
            llm_invokable=llm_invokable,
        )

    def content(self):
        """
        :return: this group's markdown abbr list
        :rtype: str
        """
        return self.as_md_list()

    def as_md_list(self):
        """
        :return: a markdown list of all abbrs
        :rtype: str
        """
        return "\n".join(entry.as_md_list_entry() for entry in self)


def _sort_entries(entries):
    return sorted(entries, key=lambda e: e.abbr.lower())


def _make_group(display_name, entries, canonical_name=None):
    return ExportableAbbr(
        entries,
        canonical_name=canonical_name or _to_skill_name(display_name),
        display_name=display_name,
    )


def _get_abbrs_by_tags(abbrs):
    return [
        _make_group(
            _ABBR_TEMPLATE + name,
            _sort_entries([e for e in abbrs if tag in e.tags]),
        )
        for tag, name in _TAG_NAMES.items()
    ]


def _get_abbrs_by_glossaries(abbr_data):
    return [
        _make_group(
            _GLOSSARY_TEMPLATE + glossary_name,
            _sort_entries(
                e for e in abbr_data.abbrs if glossary_name in e.glossaries
            ),
            canonical_name="abbr-glossary-" + glossary_name,
        )
        for glossary_name in sorted(abbr_glossary_registry)
    ]


def _get_abbrs_by_wrap(abbrs):
    return [
        _make_group(
            _ABBR_TEMPLATE + name,
            _sort_entries([e for e in abbrs if e.wrap == wrap]),
        )
        for wrap, name in _WRAP_NAMES.items()
    ]


def _get_abbrs_by_first_char(abbrs):
    letter_buckets = {letter: [] for letter in _LETTERS}
    digits = []
    other = []

    for entry in abbrs:
        first = entry.abbr[0].upper()
        if first in _LETTERS_SET:
            letter_buckets[first].append(entry)
        elif entry.abbr[0] in _DIGITS_SET:
            digits.append(entry)
        else:
            other.append(entry)

    result = [_make_group(_START_WITH_DIGIT, _sort_entries(digits))]

    for letter in _LETTERS:
        result.append(
            _make_group(
                _START_WITH_TEMPLATE + letter,
                _sort_entries(letter_buckets[letter]),
            )
        )

    result.append(_make_group(_START_WITH_OTHER, _sort_entries(other)))

    return result


# Public API  ##################################################################
def get_exportable_abbrs():
    """
    build every exportable abbreviation group, computed fresh on each
    call rather than once at import time, so it always reflects the
    current state of :func:`get_abbr_data`


    :return: every group; empty when the abbr data singleton is still empty
    :rtype: list[ExportableAbbr]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.error("abbr data is empty, no exportable abbr groups")
        return []

    abbrs = abbr_data.abbrs
    return (
        _get_abbrs_by_tags(abbrs)
        + _get_abbrs_by_glossaries(abbr_data)
        + _get_abbrs_by_wrap(abbrs)
        + _get_abbrs_by_first_char(abbrs)
    )


def register_exportable_abbrs():
    """
    register every exportable abbreviation group (see
    :func:`get_exportable_abbrs`) into `exportable_registry`, replacing
    any previously-registered group under the same key -- unlike
    blueprints, which register once, abbr groups are recomputed fresh
    each call, so a stale entry from an earlier abbr data state must
    not linger
    """
    for group in get_exportable_abbrs():
        exportable_registry.pop(group.canonical_name, None)
        register_exportable_entry(group)

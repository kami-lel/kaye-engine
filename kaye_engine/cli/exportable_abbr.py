"""
exportable_abbr.py

group abbreviations for export
"""

from kaye_engine.abbr_collection import AbbrTags, AbbrWrap, get_abbr_data
from kaye_engine.prompt.blueprint.registry import to_skill_name

# constants  ###################################################################

_ABBR_TEMPLATE = "Abbr "
_START_WITH_TEMPLATE = _ABBR_TEMPLATE + "Starts with "
_START_WITH_DIGIT = _START_WITH_TEMPLATE + "Digits 0~9"
_START_WITH_OTHER = _START_WITH_TEMPLATE + "Non-Alphanumeric"

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LETTERS_SET = frozenset(_LETTERS)
_DIGITS_SET = frozenset("0123456789")

_TAG_NAMES = {
    AbbrTags.programming_language_code: "Programming Language Codes",
    AbbrTags.language_code: "Natural Language Codes",
    AbbrTags.unit_of_measure: "Units of Measure",
    AbbrTags.currency_symbol: "Currency Symbols",
    AbbrTags.single_character: "Single Character",
    AbbrTags.emoji: "Emoji",
}

_WRAP_NAMES = {
    AbbrWrap.PREFIX: "Prefixes",
    AbbrWrap.SUFFIX: "Suffixes",
    AbbrWrap.SYMBOL: "Symbols",
}


# auxiliaries  #################################################################


class ExportableAbbr(list):  ###################################################
    """
    a named, iterable group of abbreviation entries


    :param entries: abbreviation entries for this group
    """

    def __init__(self, entries=()):
        super().__init__(entries)

        self.display_name = ""
        self.description = ""

    @property
    def skill_name(self):
        """
        :return: canonical kebab-case skill name from ``display_name``
        :rtype: str
        """
        return to_skill_name(self)

    def as_md_list(self):
        """
        :return: a markdown list of all abbrs
        :rtype: str
        """
        return "\n".join(entry.as_md_list_entry() for entry in self)


def _sort_entries(entries):
    return sorted(entries, key=lambda e: e.abbr.lower())


def _make_group(display_name, entries):
    group = ExportableAbbr(entries)
    group.display_name = display_name
    group.description = display_name
    return group


def _get_abbrs_by_tags(abbrs):
    return [
        _make_group(
            _ABBR_TEMPLATE + name,
            _sort_entries([e for e in abbrs if tag in e.tags]),
        )
        for tag, name in _TAG_NAMES.items()
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


    :return: every tag, wrap, and first-character abbreviation group
    :rtype: list[ExportableAbbr]
    """
    abbrs = get_abbr_data().abbrs
    return (
        _get_abbrs_by_tags(abbrs)
        + _get_abbrs_by_wrap(abbrs)
        + _get_abbrs_by_first_char(abbrs)
    )

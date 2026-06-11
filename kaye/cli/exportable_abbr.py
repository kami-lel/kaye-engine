"""
exportable_abbr.py

group abbreviations for export
"""

from kaye.abbr_collection import AbbrTags, AbbrWrap

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


# helpers  #####################################################################


def _sort_entries(entries):
    return sorted(entries, key=lambda e: e.abbr.lower())


# public  ######################################################################


def get_abbrs_by_tags(abbrs):
    """
    group abbreviations by tag

    :param abbrs: abbreviation entries
    :returns: list of ``(rule_name, entries)`` pairs, one per tag group
    :rtype: list[tuple[str, list]]
    """
    result = []
    for tag, display_name in _TAG_NAMES.items():
        entries = _sort_entries([e for e in abbrs if tag in e.tags])
        result.append((_ABBR_TEMPLATE + display_name, entries))
    return result


def get_abbrs_by_wrap(abbrs):
    """
    group abbreviations by wrap type

    :param abbrs: abbreviation entries
    :returns: list of ``(rule_name, entries)`` pairs, one per wrap type
    :rtype: list[tuple[str, list]]
    """
    result = []
    for wrap, display_name in _WRAP_NAMES.items():
        entries = _sort_entries([e for e in abbrs if e.wrap == wrap])
        result.append((_ABBR_TEMPLATE + display_name, entries))
    return result


def get_abbrs_by_first_char(abbrs):
    """
    group abbreviations by first character

    one group per letter (A–Z), one for digits (0–9), one catch-all for
    everything else; builds all buckets in a single pass over ``abbrs``

    :param abbrs: abbreviation entries
    :returns: list of ``(rule_name, entries)`` pairs
    :rtype: list[tuple[str, list]]
    """
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

    result = [(_START_WITH_DIGIT, _sort_entries(digits))]

    for letter in _LETTERS:
        result.append((
            _START_WITH_TEMPLATE + letter,
            _sort_entries(letter_buckets[letter]),
        ))

    result.append((_START_WITH_OTHER, _sort_entries(other)))

    return result

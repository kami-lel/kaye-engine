"""
abbr_rule.py

define ``export_abbr_rules``
"""

from pathlib import Path

from kaye.abbr_collection import AbbrData, AbbrTags, AbbrWrap
from kaye.cli.cli_continue.rule_file import RuleFile

# constants  ###################################################################

_ABBR_TEMPLATE = "Abbr "
_START_WITH_TEMPLATE = _ABBR_TEMPLATE + "Starts with "
_START_WITH_DIGIT = _START_WITH_TEMPLATE + "Digits 0~9"
_START_WITH_OTHER = _START_WITH_TEMPLATE + "Non-Alphanumeric"


_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LETTERS_SET = frozenset(_LETTERS)
_DIGITS_SET = frozenset("0123456789")


# display names for rule generation: enum/key -> display name
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


def _write_rule_file(file_path, name, entries, description=""):
    if not entries:
        return  # skip empty groups

    print("update abbr rule: {}".format(file_path))
    with RuleFile(file_path) as rule:
        rule.name = name
        rule.description = description
        rule.write_frontmatter()
        rule.writelines(entry.as_md_list_entry() for entry in entries)


# export  ======================================================================


def _export_by_tags(folder, abbrs):
    """
    export one rule file per tag group into ``folder``
    """
    for tag, display_name in _TAG_NAMES.items():
        entries = _sort_entries([e for e in abbrs if tag in e.tags])
        rule_name = _ABBR_TEMPLATE + display_name
        _write_rule_file(folder / "{}.md".format(rule_name), rule_name, entries)


def _export_by_wrap(folder, abbrs):
    """
    export one rule file per wrap type into ``folder``
    """
    for wrap, display_name in _WRAP_NAMES.items():
        entries = _sort_entries([e for e in abbrs if e.wrap == wrap])
        rule_name = _ABBR_TEMPLATE + display_name
        _write_rule_file(folder / "{}.md".format(rule_name), rule_name, entries)


def _export_by_first_char(folder, abbrs):
    """
    export rule files grouped by first character of each abbreviation
    into ``folder``: one file per letter (A–Z), one for digits (0–9),
    and one catch-all for everything else;
    builds all buckets in a single pass over ``abbrs``
    """
    # single pass  -------------------------------------------------------------
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

    # digits  ------------------------------------------------------------------
    rule_name = _START_WITH_DIGIT
    _write_rule_file(
        folder / "{}.md".format(rule_name),
        rule_name,
        _sort_entries(digits),
    )

    # letters  -----------------------------------------------------------------
    for letter in _LETTERS:
        rule_name = _START_WITH_TEMPLATE + letter
        _write_rule_file(
            folder / "{}.md".format(rule_name),
            rule_name,
            _sort_entries(letter_buckets[letter]),
        )

    # other  -------------------------------------------------------------------
    rule_name = _START_WITH_OTHER
    _write_rule_file(
        folder / "{}.md".format(rule_name),
        rule_name,
        _sort_entries(other),
    )


# Entry Point  #################################################################


def export_abbr_rules(folder):
    """
    export rule files into ``folder``

    which reads all abbreviations from ``AbbrData`` and exports rule files
    grouped by: tag (programming language, natural language, unit, currency,
    single-character, emoji), wrap (prefix, suffix, symbol), and first
    character (0–9, A–Z, other); an abbreviation may appear in multiple
    rule files


    :param folder: destination folder for rule files
    :type folder: Path-like
    """
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    abbrs = AbbrData().abbrs

    _export_by_tags(folder, abbrs)
    _export_by_wrap(folder, abbrs)
    _export_by_first_char(folder, abbrs)

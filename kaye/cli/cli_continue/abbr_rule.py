"""
abbr_rule.py

define ``export_abbr_rules``
"""

from pathlib import Path


from kaye.abbr_collection import AbbrData, AbbrTags, AbbrWrap


from .rule_file import RuleFile

# TODO standardize file name


# constants  ###################################################################

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_DIGITS = "0123456789"


_TAG_GROUPS = [
    (
        AbbrTags.programming_language_code,
        "abbr-programming_language_code.md",
        "Abbreviations Programming Language Codes",
    ),
    (
        AbbrTags.language_code,
        "abbr-language_code.md",
        "Abbreviations Natural Language Codes",
    ),
    (
        AbbrTags.unit_of_measure,
        "abbr-unit_of_measure.md",
        "Abbreviations Units of Measure",
    ),
    (
        AbbrTags.currency_symbol,
        "abbr-currency_symbol.md",
        "Abbreviations Currency Symbols",
    ),
    (
        AbbrTags.single_character,
        "abbr-single_character.md",
        "Abbreviations Single Character",
    ),
    (
        "emoji",
        "abbr-emoji.md",
        "Abbreviations Emoji",
    ),
]

_WRAP_GROUPS = [
    (AbbrWrap.SYMBOL, "abbr-symbol.md", "Abbreviations Symbols"),
    (AbbrWrap.SUFFIX, "abbr-suffix.md", "Abbreviations Suffixes"),
    (AbbrWrap.PREFIX, "abbr-prefix.md", "Abbreviations Prefixes"),
]


# helpers  #####################################################################


def _sort_entries(entries):
    return sorted(entries, key=lambda e: e.abbr.lower())


def _generate_abbr_content(entries):
    lines = [entry.as_md_list_entry() for entry in entries]
    return "\n".join(lines) + "\n"


def _write_rule_file(file_path, name, entries, description=""):
    if not entries:
        return  # skip empty groups

    print("update abbr rule: {}".format(file_path))
    with RuleFile(file_path, encoding="utf-8") as rule:
        rule.name = name
        rule.description = description
        rule.write_prefix()
        lines = "\n".join(entry.as_md_list_entry() for entry in entries) + "\n"
        rule.write(lines)


# export  ======================================================================


def _export_by_tags(folder, abbrs):
    """
    export one rule file per tag group into ``folder``
    """
    for tag, filename, name in _TAG_GROUPS:
        entries = _sort_entries([e for e in abbrs if tag in e.tags])
        _write_rule_file(folder / filename, name, entries)


def _export_by_wrap(folder, abbrs):
    """
    export one rule file per wrap type into ``folder``
    """
    for wrap, filename, name in _WRAP_GROUPS:
        entries = _sort_entries([e for e in abbrs if e.wrap == wrap])
        _write_rule_file(folder / filename, name, entries)


def _export_by_first_char(folder, abbrs):
    """
    export rule files grouped by first character of each abbreviation
    into ``folder``: one file per letter (A–Z), one for digits (0–9),
    and one catch-all for everything else
    """
    # digits  ------------------------------------------------------------------
    digits = _sort_entries([e for e in abbrs if e.abbr[0] in _DIGITS])
    _write_rule_file(
        folder / "abbr-starts_with-digits.md",
        "Abbreviations Starts with Digits (0–9)",
        digits,
    )

    # letters  -----------------------------------------------------------------
    for letter in _LETTERS:
        entries = _sort_entries(
            [e for e in abbrs if e.abbr[0].upper() == letter]
        )
        _write_rule_file(
            folder / "abbr-starts_with-{}.md".format(letter.lower()),
            "Abbreviations Starts with {}".format(letter),
            entries,
        )

    # other  -------------------------------------------------------------------
    other = _sort_entries([
        e
        for e in abbrs
        if e.abbr[0] not in _DIGITS and e.abbr[0].upper() not in _LETTERS
    ])
    _write_rule_file(
        folder / "abbr-starts_with-other.md",
        "Abbreviations Starts with Other",
        other,
    )


# Entry Point  #################################################################


def export_abbr_rules(folder):
    """
    export rule files into ``folder``

    which reads all abbreviations from
    ``AbbrData`` and exports rule files grouped by tag, wrap
    (prefix, suffix, symbol), and first character (0–9, A–Z, other);
    an abbreviation may appear in multiple rule files


    :param folder: destination folder for rule files
    :type folder: Path-like
    """
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    abbrs = AbbrData().abbrs

    _export_by_tags(folder, abbrs)
    _export_by_wrap(folder, abbrs)
    _export_by_first_char(folder, abbrs)

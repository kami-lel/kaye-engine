"""
abbr_rule.py

define ``export_abbr_rules``, which reads all abbreviations from
``AbbrData`` and exports rule files grouped by tag, prefix/suffix,
digits, letters (A–Z), and a misc catch-all
"""

from pathlib import Path

from kaye.continue_export.rule_file import RuleFile
from kaye.abbr_collection import AbbrData, AbbrTags, AbbrWrap

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_DIGITS = "0123456789"

# tag-based groups exported before letter/misc splitting  ######################

_TAG_GROUPS = [
    (
        AbbrTags.programming_language_code,
        "abbr-programming_language_code.md",
        "Abbreviations: Programming Language Codes",
        "programming language code abbreviations and their meanings",
    ),
    (
        AbbrTags.language_code,
        "abbr-language_code.md",
        "Abbreviations: Natural Language Codes",
        "natural language code abbreviations and their meanings",
    ),
    (
        AbbrTags.unit_of_measure,
        "abbr-unit_of_measure.md",
        "Abbreviations: Units of Measure",
        "unit-of-measure abbreviations and their meanings",
    ),
    (
        AbbrTags.currency_symbol,
        "abbr-currency_symbol.md",
        "Abbreviations: Currency Symbols",
        "currency symbol abbreviations and their meanings",
    ),
]


# helpers  #####################################################################


def _sort_entries(entries):
    return sorted(entries, key=lambda e: e.abbr.lower())


def _generate_abbr_content(entries):
    lines = [entry.as_md_list_entry() for entry in entries]
    return "\n".join(lines) + "\n"


def _write_rule_file(file_path, name, description, entries):
    """
    write a single rule file for ``entries`` when non-empty

    :param file_path: destination path
    :type file_path: Path
    :param name: rule name
    :type name: str
    :param description: rule description
    :type description: str
    :param entries: abbreviation entries to write
    :type entries: list[AbbrEntry]
    :return: ``True`` if the file was written, ``False`` if skipped
    :rtype: bool
    """
    if not entries:
        return False  # skip empty groups

    print("update rule: {}".format(file_path))
    with RuleFile(file_path, encoding="utf-8") as rule:
        rule.name = name
        rule.description = description
        rule.write_prefix()
        rule.write(_generate_abbr_content(entries))

    return True


# grouping  ####################################################################


def _build_groups(abbr_data):
    """
    partition ``abbr_data.abbrs`` into mutually exclusive buckets

    priority order (first match wins):

    1. tag: ``programming_language_code``
    2. tag: ``language_code``
    3. tag: ``unit_of_measure``
    4. tag: ``currency_symbol``
    5. wrap: ``AbbrWrap.SUFFIX``
    6. wrap: ``AbbrWrap.PREFIX``
    7. first char is 0–9
    8. first char is A–Z
    9. misc — everything else


    :param abbr_data: loaded abbreviation data
    :type abbr_data: AbbrData
    :return: ``(plc, lc, unit, currency, suffix, prefix, digits,
             letters, misc)``
    :rtype: tuple
    """
    plc = []
    lc = []
    unit = []
    currency = []
    suffix = []
    prefix = []
    digits = []
    letters = {ch: [] for ch in _LETTERS}
    misc = []

    for entry in abbr_data.abbrs:
        tags = entry.tags

        if AbbrTags.programming_language_code in tags:
            plc.append(entry)
        elif AbbrTags.language_code in tags:
            lc.append(entry)
        elif AbbrTags.unit_of_measure in tags:
            unit.append(entry)
        elif AbbrTags.currency_symbol in tags:
            currency.append(entry)
        elif entry.wrap == AbbrWrap.SUFFIX:
            suffix.append(entry)
        elif entry.wrap == AbbrWrap.PREFIX:
            prefix.append(entry)
        elif entry.abbr[0] in _DIGITS:
            digits.append(entry)
        elif entry.abbr[0].upper() in letters:
            letters[entry.abbr[0].upper()].append(entry)
        else:
            misc.append(entry)

    # sort all buckets  --------------------------------------------------------
    plc = _sort_entries(plc)
    lc = _sort_entries(lc)
    unit = _sort_entries(unit)
    currency = _sort_entries(currency)
    suffix = _sort_entries(suffix)
    prefix = _sort_entries(prefix)
    digits = _sort_entries(digits)

    for ch in _LETTERS:
        letters[ch] = _sort_entries(letters[ch])

    misc = _sort_entries(misc)

    return plc, lc, unit, currency, suffix, prefix, digits, letters, misc


# export  ######################################################################


def export_abbr_rules(rules_folder):
    """
    export rule files into ``rules_folder``

    groups exported, in order:

    - one file per tag group (plc, lc, unit_of_measure, currency_symbol)
    - ``abbr-suffix.md``
    - ``abbr-prefix.md``
    - ``abbr-digits.md``
    - ``abbr-{letter}.md`` for each A–Z letter with entries
    - ``abbr-misc.md`` for anything remaining

    :param rules_folder: destination folder for rule files
    :type rules_folder: Path-like
    """
    folder = Path(rules_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    plc, lc, unit, currency, suffix, prefix, digits, letters, misc = (
        _build_groups(AbbrData())
    )

    # tag-based files  ---------------------------------------------------------
    tag_entries = [plc, lc, unit, currency]
    for (_, filename, name, description), entries in zip(
        _TAG_GROUPS, tag_entries
    ):
        _write_rule_file(folder / filename, name, description, entries)

    # suffix  ------------------------------------------------------------------
    _write_rule_file(
        folder / "abbr-suffix.md",
        "Abbreviations: Suffixes",
        "suffix-style abbreviations and their meanings",
        suffix,
    )

    # prefix  ------------------------------------------------------------------
    _write_rule_file(
        folder / "abbr-prefix.md",
        "Abbreviations: Prefixes",
        "prefix-style abbreviations and their meanings",
        prefix,
    )

    # digits  ------------------------------------------------------------------
    _write_rule_file(
        folder / "abbr-starts_with-digits.md",
        "Abbreviations: Starts with Digits (0–9)",
        "abbreviations starting with a digit and their meanings",
        digits,
    )

    # letter groups  -----------------------------------------------------------
    for letter in _LETTERS:
        entries = letters[letter]
        _write_rule_file(
            folder / "abbr-starts_with-{}.md".format(letter.lower()),
            "Abbreviations: Starts with {}".format(letter),
            "abbreviations starting with {} and their meanings".format(letter),
            entries,
        )

    # misc  --------------------------------------------------------------------
    _write_rule_file(
        folder / "abbr-misc.md",
        "Abbreviations: Miscellaneous",
        "miscellaneous abbreviations and their meanings",
        misc,
    )

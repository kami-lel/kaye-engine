"""
abbr_rule.py

define ``export_abbr_rules``, which reads all abbreviations from
``AbbrData`` and exports rule files grouped by tag, prefix/suffix,
digits, letters (A–Z), and a misc catch-all
"""

from pathlib import Path

from kaye.continue_export.rule_file import RuleFile
from kaye.abbr_collection import AbbrData, AbbrTags

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
        "Abbreviations: Language Codes",
        "language code abbreviations and their meanings",
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


def _is_suffix(abbr):
    """
    return ``True`` when ``abbr`` starts with a non-alphanumeric character,
    indicating a suffix-style abbreviation (e.g. ``.g``, ``'s``)

    :param abbr: abbreviation string
    :type abbr: str
    :rtype: bool
    """
    return len(abbr) > 0 and not abbr[0].isalnum()


def _is_prefix(abbr):
    """
    return ``True`` when ``abbr`` ends with a non-alphanumeric character
    and starts with an alphanumeric character,
    indicating a prefix-style abbreviation (e.g. ``o.``)

    :param abbr: abbreviation string
    :type abbr: str
    :rtype: bool
    """
    return len(abbr) > 0 and abbr[0].isalnum() and not abbr[-1].isalnum()


def _sort_entries(entries):
    """
    return ``entries`` sorted case-insensitively by abbreviation

    :param entries: abbreviation entries
    :type entries: list[AbbrEntry]
    :rtype: list[AbbrEntry]
    """
    return sorted(entries, key=lambda e: e.abbr.lower())


def _generate_abbr_content(entries):
    """
    render ``entries`` as a markdown list of ``abbr:meaning`` pairs

    :param entries: abbreviation entries for a single group
    :type entries: list[AbbrEntry]
    :return: rendered markdown content
    :rtype: str
    """
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

    1. tag-based groups (plc, lc, unit_of_measure, currency_symbol)
    2. suffix abbreviations  (first char is non-alphanumeric)
    3. prefix abbreviations  (last char is non-alphanumeric)
    4. digit group           (first char is 0–9)
    5. letter groups         (first char is A–Z, case-insensitive)
    6. misc                  (everything else)

    :param abbr_data: loaded abbreviation data
    :type abbr_data: AbbrData
    :return: tuple of
             ``(tag_buckets, suffix, prefix, digits, letters, misc)``

             - ``tag_buckets``: list parallel to ``_TAG_GROUPS``,
               each element is a ``list[AbbrEntry]``
             - ``suffix``: list[AbbrEntry]
             - ``prefix``: list[AbbrEntry]
             - ``digits``:  list[AbbrEntry]
             - ``letters``: dict[str, list[AbbrEntry]]  (keys A–Z)
             - ``misc``:    list[AbbrEntry]
    :rtype: tuple
    """
    tag_buckets = [[] for _ in _TAG_GROUPS]
    suffix = []
    prefix = []
    digits = []
    letters = {ch: [] for ch in _LETTERS}
    misc = []

    claimed = set()  # track entry ids already placed

    # pass 1: tag-based groups  ------------------------------------------------
    for i, (tag, *_) in enumerate(_TAG_GROUPS):
        for entry in abbr_data.abbrs:
            if entry in claimed:
                continue
            if tag in entry.tags:
                tag_buckets[i].append(entry)
                claimed.add(entry)

    # pass 2: suffix / prefix / digit / letter / misc  -------------------------
    for entry in abbr_data.abbrs:
        if entry in claimed:
            continue

        abbr = entry.abbr
        first = abbr[0]

        if _is_suffix(abbr):
            suffix.append(entry)
        elif _is_prefix(abbr):
            prefix.append(entry)
        elif first in _DIGITS:
            digits.append(entry)
        elif first.upper() in letters:
            letters[first.upper()].append(entry)
        else:
            misc.append(entry)

    # sort all buckets  --------------------------------------------------------
    for i in range(len(tag_buckets)):
        tag_buckets[i] = _sort_entries(tag_buckets[i])

    suffix = _sort_entries(suffix)
    prefix = _sort_entries(prefix)
    digits = _sort_entries(digits)

    for ch in _LETTERS:
        letters[ch] = _sort_entries(letters[ch])

    misc = _sort_entries(misc)

    return tag_buckets, suffix, prefix, digits, letters, misc


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

    tag_buckets, suffix, prefix, digits, letters, misc = _build_groups(
        AbbrData()
    )

    # tag-based files  ---------------------------------------------------------
    for (_, filename, name, description), entries in zip(
        _TAG_GROUPS, tag_buckets
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
        folder / "abbr-digits.md",
        "Abbreviations: Starting with Digits (0–9)",
        "abbreviations starting with a digit and their meanings",
        digits,
    )

    # letter groups  -----------------------------------------------------------
    for letter in _LETTERS:
        entries = letters[letter]
        _write_rule_file(
            folder / "abbr-{}.md".format(letter),
            "Abbreviations: {}".format(letter),
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

"""
abbr_rule.py

define ``export_abbr_rules``, which reads all abbreviations from
``AbbrData`` and exports one Continue AI rule file per letter (A–Z)
"""

from pathlib import Path

from kaye.continue_export.rule_file import RuleFile
from kaye.abbr_collection import AbbrData

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_letter_groups(abbr_data):
    """
    group ``abbr_data.abbrs`` by the first character of each abbreviation

    entries whose first character is not A–Z are silently skipped

    :param abbr_data: loaded abbreviation data
    :type abbr_data: AbbrData
    :return: mapping of uppercase letter to sorted list of ``AbbrEntry``
    :rtype: dict[str, list[AbbrEntry]]
    """
    groups = {letter: [] for letter in _LETTERS}

    for entry in abbr_data.abbrs:
        first = entry.abbr[0].upper()
        if first in groups:
            groups[first].append(entry)

    for letter in _LETTERS:
        groups[letter].sort(key=lambda e: e.abbr.lower())

    return groups


def _generate_abbr_content(entries):
    """
    render ``entries`` as a markdown list of ``abbr`` — ``meaning`` pairs

    :param entries: abbreviation entries for a single letter group
    :type entries: list[AbbrEntry]
    :return: rendered markdown content
    :rtype: str
    """
    lines = [entry.as_md_list_entry() for entry in entries]
    return "\n".join(lines) + "\n"


def export_abbr_rules(rules_folder):
    """
    export one rule file per letter (A–Z) into ``rules_folder``

    each file is named ``abbreviation starting with {letter}.md`` and
    lists all abbreviations from ``abbrs.json`` whose first character
    matches that letter; letters with no entries are skipped

    :param rules_folder: destination folder for rule files
    :type rules_folder: Path-like
    """
    folder = Path(rules_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    groups = _build_letter_groups(AbbrData())

    for letter in _LETTERS:
        entries = groups[letter]
        if not entries:
            continue  # skip empty letters

        file_path = folder / "abbreviation starting with {}.md".format(letter)
        print("update rule: {}".format(file_path))

        with RuleFile(file_path, encoding="utf-8") as rule:
            rule.name = "Abbreviations: {}".format(letter)
            rule.description = (
                "abbreviations and their meanings starting with {}".format(
                    letter
                )
            )
            rule.write_prefix()
            rule.write(_generate_abbr_content(entries))


# TODO split as grouping, not just letters

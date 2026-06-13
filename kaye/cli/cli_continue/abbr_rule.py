"""
abbr_rule.py

define ``export_abbr_rules``
"""

from pathlib import Path

from kaye.abbr_collection import AbbrData
from kaye.cli.cli_continue.rule_file import RuleFile
from kaye.cli.exportable_abbr import (
    get_abbrs_by_tags,
    get_abbrs_by_wrap,
    get_abbrs_by_first_char,
)

# helpers  #####################################################################


def _write_rule_file(file_path, name, entries, description=""):
    if not entries:
        return  # skip empty groups

    print("update abbr rule: {}".format(file_path))
    with RuleFile(file_path) as rule:
        rule.name = name
        rule.description = description
        rule.write_frontmatter_part()
        rule.writelines(entry.as_md_list_entry() for entry in entries)


# export  ======================================================================


def _export_groups(folder, groups):
    for name, entries in groups:
        _write_rule_file(folder / "{}.md".format(name), name, entries)


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

    _export_groups(folder, get_abbrs_by_tags(abbrs))
    _export_groups(folder, get_abbrs_by_wrap(abbrs))
    _export_groups(folder, get_abbrs_by_first_char(abbrs))

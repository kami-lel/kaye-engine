"""
abbr_rule.py

define ``export_abbr_rules``
"""

from pathlib import Path

from kaye import logger
from kaye.cli.cli_continue.rule_file import RuleFile
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS

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

    for group in EXPORTABLE_ABBRS:
        file_path = folder / "{}.md".format(group.display_name)

        with RuleFile(file_path) as rule:
            rule.name = group.display_name
            rule.description = group.description
            rule.write_frontmatter_part()
            rule.write(group.as_md_list())

        logger.succ("abbr rule:\t{}".format(file_path))

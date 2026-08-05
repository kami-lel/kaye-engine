# hack hack Continue support is deprecated
"""
abbr_rule.py

define ``export_abbr_rules``
"""

from pathlib import Path

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.cli.cli_continue.rule_file import ContinueRule
from kaye_engine.cli.exportable_abbr import get_exportable_abbrs

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# Main Entry Point  ############################################################
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

    for group in get_exportable_abbrs():
        file_path = folder / "{}.md".format(group.display_name)

        ContinueRule(
            name=group.display_name,
            description=group.description,
            body=group.as_md_list(),
        ).write(file_path)

        logger.succ("abbr rule:\t{}".format(file_path))

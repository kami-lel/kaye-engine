"""
export_vs_code_extension.py

define ``export_vs_code_extension``
"""

from pathlib import Path

from kaye import logger
from kaye.cli.cli_claude.claude_marketplace.export_marketplace import export_marketplace
from kaye.cli.cli_claude.user_prompt.cli_claude_user_prompt import (
    find_user_system_prompt_file,
)
from kaye.cli.cli_claude.user_prompt.export_user_file import export_user_system_prompt_file

# constants  ===================================================================

MARKETPLACE_NAME = "kaye_marketplace"

# entry point  #################################################################


def export_vs_code_extension(claude_folder):
    """
    export CLAUDE.md and a kaye_marketplace/ into the given Claude folder

    writes CLAUDE.md (Chat + Coder blueprint) at ``claude_folder/CLAUDE.md``
    and a marketplace at ``claude_folder/kaye_marketplace/``

    :param claude_folder: destination .claude/ folder
    :type claude_folder: Path-like
    """
    claude_folder = Path(claude_folder)

    logger.debug("export user system prompt file")
    prompt_file = find_user_system_prompt_file(claude_folder)
    export_user_system_prompt_file(prompt_file, use_coder=True)
    logger.succ("export user system prompt file:\t" + str(prompt_file))

    logger.debug("export marketplace")
    marketplace_folder = claude_folder / MARKETPLACE_NAME
    export_marketplace(marketplace_folder)
    logger.succ("export marketplace:\t" + str(marketplace_folder))

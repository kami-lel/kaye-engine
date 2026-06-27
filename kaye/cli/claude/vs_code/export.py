"""
export_vs_code_extension.py

define ``export_vs_code_extension``
"""

from pathlib import Path

from kaye import logger
from kaye.cli.claude.marketplace.export import export_marketplace
from kaye.cli.claude.user_prompt.parser import (
    find_user_system_prompt_file,
)
from kaye.cli.claude.user_prompt.export import export_user_system_prompt_file
from .settings import update_settings_json_for_pre_compact_hook

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
    :return: path to the written marketplace.json
    :rtype: Path
    """
    claude_folder = Path(claude_folder)

    logger.debug("export user system prompt file")
    prompt_file = find_user_system_prompt_file(claude_folder)
    export_user_system_prompt_file(prompt_file, use_coder=True)
    logger.succ("export user system prompt file:\t" + str(prompt_file))

    logger.debug("export marketplace")
    marketplace_folder = claude_folder / MARKETPLACE_NAME
    marketplace_path = export_marketplace(marketplace_folder)
    logger.succ("export marketplace:\t" + str(marketplace_folder))

    logger.debug("update settings for pre-compact hook")
    update_settings_json_for_pre_compact_hook(claude_folder)
    logger.succ("update settings for pre-compact hook")

    return marketplace_path

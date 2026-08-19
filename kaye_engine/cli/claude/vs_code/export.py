"""
export_vs_code_extension.py

define ``export_vs_code_extension``
"""

from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.marketplace.export import export_marketplace
from kaye_engine.cli.claude.setup import get_marketplace_folder_name
from kaye_engine.cli.claude.user_prompt.parser import (
    find_user_system_prompt_file,
)
from kaye_engine.cli.claude.user_prompt.export import (
    export_user_system_prompt_file,
)
from .settings import update_settings_json

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def export_vs_code_extension(claude_folder, *, render_profile=None):
    """
    export CLAUDE.md and a marketplace folder into the given Claude folder

    writes CLAUDE.md (Chat + Coder blueprint) at ``claude_folder/CLAUDE.md``
    and a marketplace at ``claude_folder/<marketplace folder name>/``

    :param claude_folder: destination .claude/ folder
    :type claude_folder: Path-like
    :param render_profile: render options forwarded to both
            :func:`export_user_system_prompt_file` and
            :func:`export_marketplace`
    :type render_profile: RenderProfile, optional
    :return: path to the written marketplace.json
    :rtype: Path
    """
    claude_folder = Path(claude_folder)

    logger.debug("export user system prompt file")
    prompt_file = find_user_system_prompt_file(claude_folder)
    export_user_system_prompt_file(
        prompt_file,
        use_coder=True,
        render_profile=render_profile,
    )
    logger.succ("export user system prompt file:\t" + str(prompt_file))

    logger.debug("export marketplace")
    marketplace_folder = claude_folder / get_marketplace_folder_name()
    marketplace_path = export_marketplace(
        marketplace_folder, render_profile=render_profile
    )
    logger.succ("export marketplace:\t" + str(marketplace_folder))

    logger.debug("update settings for git command permissions")
    settings_path = update_settings_json(claude_folder)
    logger.succ(
        "update settings for git command permissions:\t" + str(settings_path)
    )

    return marketplace_path

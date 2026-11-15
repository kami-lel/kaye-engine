"""
payload.py

define ``generate_vs_code_payload`` -- stage 1 of the VS Code extension
export: write ``CLAUDE.md`` and the marketplace folder into any folder,
knowing nothing of ``~/.claude``
"""

from pathlib import Path

import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.marketplace.export import export_marketplace
from kaye_engine.cli.claude.setup import get_marketplace_folder_name
from kaye_engine.cli.claude.user_prompt.export import (
    export_user_system_prompt_file,
)
from kaye_engine.cli.claude.user_prompt.parser import (
    find_user_system_prompt_file,
)

__all__ = ("generate_vs_code_payload",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


# Public API  ##################################################################
def generate_vs_code_payload(payload_folder, *, render_profile=None):
    """
    write the payload into ``payload_folder``

    writes CLAUDE.md (Chat + Coder blueprint) at
    ``payload_folder/CLAUDE.md`` and a marketplace at
    ``payload_folder/<marketplace folder name>/``; places nothing in any
    Claude folder, see :func:`place_vs_code_payload`


    :param payload_folder: folder to fill; created when missing
    :type payload_folder: Path-like
    :param render_profile: render options forwarded to both
            :func:`export_user_system_prompt_file` and
            :func:`export_marketplace`
    :type render_profile: RenderProfile, optional
    :return: path to the written marketplace.json
    :rtype: Path
    """
    payload_folder = Path(payload_folder)

    logger.debug("export user system prompt file")
    export_user_system_prompt_file(
        find_user_system_prompt_file(payload_folder),
        use_coder=True,
        render_profile=render_profile,
    )

    logger.debug("export marketplace")
    return export_marketplace(
        payload_folder / get_marketplace_folder_name(),
        render_profile=render_profile,
    )

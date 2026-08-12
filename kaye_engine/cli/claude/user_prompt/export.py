"""
export_user_file.py

define ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.blueprint_name import (
    get_claude_chat_blueprint,
    get_claude_coder_blueprint,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


# Hack kaye a usp: dont take file path, to allow > pattern
# Fixme kaye a usp: claude setup take a blueprint that merge into chat
# Todo kaye a usp: need include version


# Main Entry Point  ############################################################
def export_user_system_prompt_file(
    file_path,
    *,
    use_coder=False,
    sparseness=1,
    surface=None,
):
    """
    export the Chat blueprint as Claude user/system prompt to CLAUDE.md

    renders the configured Chat blueprint and writes the prompt to the given
    file path; optionally appends the configured Coder blueprint

    :param file_path: destination file path for CLAUDE.md
    :type file_path: Path-like
    :param use_coder: append the Coder blueprint after the main blueprint
    :type use_coder: bool
    :param sparseness: blank-line policy forwarded to
            ``generate_prompt()``; defaults to 1
    :type sparseness: int, optional
    :param surface: Claude surface(s) to checkmark affordances for;
            ``None`` leaves affordance checkmarking disabled
    :type surface: ClaudeSurface, optional
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    blueprint = get_claude_chat_blueprint()

    agentic = blueprint.corpus["Agentic"]
    blueprint.checkmark(agentic["Claude Behavior"])

    if use_coder:
        blueprint = blueprint | get_claude_coder_blueprint()

    file_path.write_text(
        blueprint.generate_prompt(
            affordances=(
                surface.as_affordances() if surface is not None else None
            ),
            contains_sidecars=(
                surface.as_contained_sidecars()
                if surface is not None else ()
            ),
            sparseness=sparseness,
        ),
        encoding="utf-8",
    )

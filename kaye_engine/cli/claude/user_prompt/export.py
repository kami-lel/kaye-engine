"""
export_user_file.py

define ``generate_user_system_prompt``, ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.blueprint_name import (
    get_claude_chat_blueprint,
    get_claude_coder_blueprint,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


# Main Entry Point  ############################################################
def generate_user_system_prompt(
    *,
    use_coder=False,
    sparseness=DEFAULT_SPARSENESS,
    surface=None,
    show_comment=False,
):
    """
    render the Chat blueprint as the Claude user/system prompt

    renders the configured Chat blueprint; optionally appends the
    configured Coder blueprint

    :param use_coder: append the Coder blueprint after the main blueprint
    :type use_coder: bool
    :param sparseness: blank-line policy forwarded to
            ``generate_prompt()``; defaults to 1
    :type sparseness: int, optional
    :param surface: Claude surface(s) to checkmark affordances for;
            ``None`` leaves affordance checkmarking disabled
    :type surface: ClaudeSurface, optional
    :param show_comment: include the trailing generated-by comment
    :type show_comment: bool
    :return: rendered prompt
    :rtype: str
    """
    blueprint = get_claude_chat_blueprint()

    if use_coder:
        blueprint = blueprint | get_claude_coder_blueprint()

    return blueprint.generate_prompt(
        affordances=(surface.as_affordances() if surface is not None else None),
        conditional_sidecars=(
            surface.as_contained_sidecars() if surface is not None else ()
        ),
        sparseness=sparseness,
        show_comment=show_comment,
    )


def export_user_system_prompt_file(
    file_path,
    *,
    use_coder=False,
    sparseness=DEFAULT_SPARSENESS,
    surface=None,
    show_comment=False,
):
    """
    export the Chat blueprint as Claude user/system prompt to CLAUDE.md

    renders the configured Chat blueprint via
    :func:`generate_user_system_prompt` and writes the prompt to the given
    file path

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
    :param show_comment: include the trailing generated-by comment
    :type show_comment: bool
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        generate_user_system_prompt(
            use_coder=use_coder,
            sparseness=sparseness,
            surface=surface,
            show_comment=show_comment,
        ),
        encoding="utf-8",
    )

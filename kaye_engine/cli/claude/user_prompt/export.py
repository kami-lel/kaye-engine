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
    affordances=None,
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
    :param affordances: forwarded to ``generate_prompt()``; see its
            ``affordances`` param; defaults to ``None`` (auto-checkmark
            pass off)
    :type affordances: collections.abc.Iterable[str] or None, optional
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
            affordances=affordances, sparseness=sparseness
        ),
        encoding="utf-8",
    )

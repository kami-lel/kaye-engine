"""
export_user_file.py

define ``generate_user_system_prompt``, ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.exportable_name import (
    get_claude_chat_coder_exportable,
    get_claude_chat_exportable,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


# Main Entry Point  ############################################################
def generate_user_system_prompt(*, use_coder=False, render_kwargs=None):
    """
    render the Chat exportable as the Claude user/system prompt

    renders the configured Chat exportable; when ``use_coder``, renders
    the configured Chat Coder exportable instead -- the precomputed
    merge of Chat and Coder

    :param use_coder: render the precomputed Chat+Coder exportable
            instead of the plain Chat exportable
    :type use_coder: bool
    :param render_kwargs: kwargs forwarded to ``generate_prompt()``, v.s.
            ``resolve_render_options()``; ``None`` renders with
            ``generate_prompt()``'s own defaults
    :type render_kwargs: dict, optional
    :return: rendered prompt
    :rtype: str
    """
    exportable = (
        get_claude_chat_coder_exportable()
        if use_coder
        else get_claude_chat_exportable()
    )

    return exportable.content(**(render_kwargs or {}))


def export_user_system_prompt_file(
    file_path,
    *,
    use_coder=False,
    render_kwargs=None,
):
    """
    export the Chat exportable as Claude user/system prompt to CLAUDE.md

    renders the configured Chat (or Chat Coder) exportable via
    :func:`generate_user_system_prompt` and writes the prompt to the given
    file path

    :param file_path: destination file path for CLAUDE.md
    :type file_path: Path-like
    :param use_coder: render the precomputed Chat+Coder exportable
            instead of the plain Chat exportable
    :type use_coder: bool
    :param render_kwargs: kwargs forwarded to ``generate_prompt()``, v.s.
            ``resolve_render_options()``; ``None`` renders with
            ``generate_prompt()``'s own defaults
    :type render_kwargs: dict, optional
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        generate_user_system_prompt(
            use_coder=use_coder,
            render_kwargs=render_kwargs,
        ),
        encoding="utf-8",
    )

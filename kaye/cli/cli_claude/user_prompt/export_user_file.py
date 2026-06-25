"""
export_user_file.py

define ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye.prompt.embedded_blueprints import (
    chat_blueprint,
    coder_blueprint,
    rapid_blueprint,
)
from kaye.api.dify_app.kaye_chat_task import _user_scope_blueprint


def export_user_system_prompt_file(file_path, rapid=False, coder=False):
    """
    export Chat or Rapid blueprint as Claude user/system prompt to CLAUDE.md

    renders the selected blueprint and writes the prompt to the given file path;
    optionally appends the Kaye Peer Coder blueprint

    :param file_path: destination file path for CLAUDE.md
    :type file_path: Path-like
    :param rapid: use Rapid blueprint instead of Chat
    :type rapid: bool
    :param coder: append Kaye Peer Coder content after the main blueprint
    :type coder: bool
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    blueprint = (rapid_blueprint if rapid else chat_blueprint) | _user_scope_blueprint

    if coder:
        blueprint = blueprint | coder_blueprint

    file_path.write_text(blueprint.generate_prompt(), encoding="utf-8")

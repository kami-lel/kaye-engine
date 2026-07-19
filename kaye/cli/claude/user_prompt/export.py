"""
export_user_file.py

define ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye.prompt.blueprint.embedded_blueprints import (
    chat_blueprint,
    coder_blueprint,
    rapid_blueprint,
)
from kaye.cli.claude import CONTAINING_SIDECAR_NODES


def export_user_system_prompt_file(
    file_path, *, use_rapid=False, use_coder=False
):
    """
    export Chat or Rapid blueprint as Claude user/system prompt to CLAUDE.md

    renders the selected blueprint and writes the prompt to the given file path;
    optionally appends the Kaye Peer Coder blueprint

    :param file_path: destination file path for CLAUDE.md
    :type file_path: Path-like
    :param use_rapid: use Rapid blueprint instead of Chat
    :type use_rapid: bool
    :param use_coder: append Kaye Peer Coder content after the main blueprint
    :type use_coder: bool
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    blueprint = rapid_blueprint if use_rapid else chat_blueprint

    agent_behavior = blueprint.corpus["Agent Behavior"]
    blueprint.checkmark(agent_behavior)
    blueprint.checkmark(agent_behavior["Claude Behavior"])

    if use_coder:
        blueprint = blueprint | coder_blueprint

    file_path.write_text(
        blueprint.generate_prompt(
            contains_sidecar_nodes=CONTAINING_SIDECAR_NODES
        ),
        encoding="utf-8",
    )

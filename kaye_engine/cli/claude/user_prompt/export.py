"""
export_user_file.py

define ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.cli.claude import CONTAINING_SIDECARS


# FIXME utilize kamilog here
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

    base_name = "rapid" if use_rapid else "chat"
    # Fixme unguarded lookup; on a corpus-less install this raises a raw
    # KeyError traceback and aborts claude code / vs-code-extension midway
    blueprint = blueprint_registry[base_name].blueprint

    agent_behavior = blueprint.corpus["Agent Behavior"]
    blueprint.checkmark(agent_behavior)
    blueprint.checkmark(agent_behavior["Claude Behavior"])

    if use_coder:
        blueprint = blueprint | blueprint_registry["coder"].blueprint

    file_path.write_text(
        blueprint.generate_prompt(contains_sidecars=CONTAINING_SIDECARS),
        encoding="utf-8",
    )

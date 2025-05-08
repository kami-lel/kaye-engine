"""
define ``load_current_full_prompt_tree``
"""

from pathlib import Path
from .full_prompt_parser import FullPromptParserNode

__all__ = ("load_current_full_prompt_tree",)


# BUG full should be a special case


def _get_full_prompt_file_path():
    """
    :return: absolute path to the ``prompt_full.md`` file.
    :rtype: Path
    """
    # find path of prompt_full.md based by relative path from this script
    return (
        Path(__file__).resolve().parent.parent / "prompt_full.md"
    ).absolute()


def load_current_full_prompt_tree():
    """
    Read the content of the full prompt file and parse it into a tree structure.

    This function retrieves the full prompt from the ``prompt_full.md`` file,
    parses its content using the `FullPromptParserNode`, and returns an instance
    representing the full prompt's tree structure.

    :return: root of Full Prompt Tree
    :rtype: FullPromptParserNode
    :raises FileNotFoundError: If the full prompt file cannot be found.
    :raises IOError: If an error occurs while reading the file.
    """
    full_prompt_file_path = _get_full_prompt_file_path()
    with open(
        full_prompt_file_path, "r", encoding="utf-8", newline=""
    ) as file:
        file_content = file.read()
        return FullPromptParserNode.parse(file_content)

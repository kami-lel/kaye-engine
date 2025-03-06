"""
The `gen_prompt` module manages prompts for Kaye.
It generates contextually relevant prompts from a
structured prompt tree, enhancing user interactions
with flexibility and responsiveness for improved
communication quality.
"""

from pathlib import Path
from .prompt_tree_node import *


def _get_full_prompt_file_path():
    """
    :return: absolute path to the "prompt_full.md" file.
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_full.md"
    ).absolute()


def get_full_prompt_tree_root():
    """
    reads the content of the full prompt file and
    initializes a `FullPromptTreeNode` with it.

    :return: root node of the structured prompt tree.
    :rtype: FullPromptTreeNode
    """
    full_prompt_file_path = _get_full_prompt_file_path()
    with open(
        full_prompt_file_path, "r", encoding="utf-8", newline=""
    ) as file:
        file_content = file.read()
        return FullPromptTreeNode(file_content)

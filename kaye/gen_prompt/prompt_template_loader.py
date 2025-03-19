"""
define ``get_prompt_templates_names``, ``load_prompt_template``
"""

import os
from pathlib import Path

from .full_prompt_tree_loader import load_current_full_prompt_tree

__all__ = ("get_prompt_templates_names", "load_prompt_template")


def get_prompt_templates_names():
    """
    :return: names of all available existing prompt templates
    :rtype: list[str]
    :raises FileNotFoundError: If the ``prompt_templates`` folder does not exist.
    :raises OSError: If there is an error accessing the files in the folder.
    """
    folder_path = _get_prompt_templates_folder_path()
    files_paths = os.listdir(folder_path)
    # Filter out directories, keeping only files and removing extensions
    return [
        os.path.splitext(file)[0]
        for file in files_paths
        if os.path.isfile(os.path.join(folder_path, file))
    ]


def load_prompt_template(prompt_name):
    pass  # TODO


def _get_prompt_templates_folder_path():
    """
    :return: absolute path to ``prompt_templates`` folder
    :rtype: Path
    """
    # find folder path by relative path from this script
    return (Path(__file__).resolve().parent / "prompt_templates").absolute()

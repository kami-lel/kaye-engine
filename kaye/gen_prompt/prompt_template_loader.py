"""
define ``get_prompt_templates_names``, ``load_prompt_template``
"""

import os
from pathlib import Path

from .full_prompt_tree_loader import load_current_full_prompt_tree
from .prompt_template import PromptTemplate

__all__ = ("get_prompt_templates_names", "load_prompt_template")


# Bug full should be a special case


def get_prompt_templates_names():
    """
    :return: names of all available existing prompt templates
    :rtype: dict{str: str}
    :raises FileNotFoundError: If the ``prompt_templates`` folder does not exist.
    :raises OSError: If there is an error accessing the files in the folder.
    """
    return list(_get_prompt_templates_names_and_paths().keys())


def load_prompt_template(prompt_name):
    """
    :param prompt_name:
    :type prompt_name: str
    :return: an exsiting PromptTemplate with name ``prompt_name``
    :rtype: PromptTemplate
    :raises FileNotFoundError:
    :raises OSError:
    """

    # assert prompt_name is an existing prompt file
    prompt_file_path = _get_prompt_templates_names_and_paths().get(
        prompt_name, ""
    )
    if not prompt_file_path:
        raise FileNotFoundError(
            "The prompt template '{}' does not exist in the "
            "available templates.".format(prompt_name)
        )

    # read content
    with open(prompt_file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return PromptTemplate(
            content, full_prompt_tree=load_current_full_prompt_tree()
        )


def _get_prompt_templates_names_and_paths():
    """
    :return: names and full paths of all available existing prompt templates
    :rtype: dict{str: str}
    """
    folder_path = _get_prompt_templates_folder_path()
    files_paths = os.listdir(folder_path)
    # Filter out directories, keeping only files and removing extensions
    return {
        os.path.splitext(file)[0]: os.path.join(folder_path, file)
        for file in files_paths
        if os.path.isfile(os.path.join(folder_path, file))
    }


def _get_prompt_templates_folder_path():
    """
    :return: absolute path to ``prompt_templates`` folder
    :rtype: Path
    """
    # find folder path by relative path from this script
    return (Path(__file__).resolve().parent / "prompt_templates").absolute()

"""
define ``get_prompt_templates_names``, ``load_prompt_template``
"""

import os
from pathlib import Path

from .prompt_corpus_loader import load_embedded_prompt_corpus
from .prompt_blueprint import PromptBlueprint

__all__ = (
    "get_embedded_prompt_blueprints_folder_path",
    "get_embedded_prompt_blueprints_names",
    "load_embedded_prompt_blueprint",
)


def get_embedded_prompt_blueprints_folder_path():
    """
    :return: absolute path to ``prompt_blueprints`` folder
            containing embedded prompt blueprints
    :rtype: Path
    """
    # find folder path by relative path from this script
    return (Path(__file__).resolve().parent / "prompt_blueprints").absolute()


def get_embedded_prompt_blueprints_names():
    """
    :return: names of all available embedded prompt blueprints
    :rtype: list(str)
    :raises FileNotFoundError:
    :raises OSError:
    """
    return list(_get_embedded_prompt_blueprints_names_and_paths().keys())


def load_embedded_prompt_blueprint(prompt_blueprint_name):
    """
    :param prompt_name:
    :type prompt_name: str
    :return: an exsiting PromptBlueprint with name ``prompt_name``
    :rtype: PromptBlueprint
    :raises FileNotFoundError:
    :raises OSError:
    """
    # HACK improve all docstring
    # BUG full should be a special case

    # assert prompt_name is an existing prompt file
    prompt_file_path = _get_embedded_prompt_blueprints_names_and_paths().get(
        prompt_blueprint_name, ""
    )
    if not prompt_file_path:
        raise FileNotFoundError(
            "The prompt template '{}' does not exist in the "
            "available templates.".format(prompt_blueprint_name)
        )

    # read content
    with open(prompt_file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return PromptBlueprint(
            content, full_prompt_tree=load_embedded_prompt_corpus()
        )


def _get_embedded_prompt_blueprints_names_and_paths():
    """
    :return: names and full paths of all available embedded prompt blueprints
    :rtype: dict{str: str}
    """
    folder_path = get_embedded_prompt_blueprints_folder_path()
    files_paths = os.listdir(folder_path)
    # Filter out directories, keeping only files and removing extensions
    return {
        os.path.splitext(file)[0]: os.path.join(folder_path, file)
        for file in files_paths
        if os.path.isfile(os.path.join(folder_path, file))
    }

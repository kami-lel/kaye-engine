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
    Load one of the prompt blueprints embedded with this Python package


    :param prompt_blueprint_name: name of an embedded prompt blueprints,
            must be from ``get_embedded_prompt_blueprints_names()``;
            if ``'full'``: special case blueprint with **all nodes enabled**
    :type prompt_blueprint_name: str
    :return: v.s.
    :rtype: PromptBlueprint
    :raises FileNotFoundError:
    :raises IOError:
    :raises ValueError: prompt_name is
            not a recognized embedded prompt blueprint
    """

    # assert prompt_name is an existing prompt file
    prompt_file_path = _get_embedded_prompt_blueprints_names_and_paths().get(
        prompt_blueprint_name, ""
    )
    if not prompt_file_path:
        raise ValueError(
            "'{}' is not a recognized embedded prompt blueprint.".format(
                prompt_blueprint_name
            )
        )

    # read content
    with open(prompt_file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return PromptBlueprint(load_embedded_prompt_corpus(), content)

    # TODO full special case


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

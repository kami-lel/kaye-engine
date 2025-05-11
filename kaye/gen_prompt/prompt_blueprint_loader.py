"""
define ``get_prompt_templates_names``, ``load_prompt_template``
"""

import os
from pathlib import Path

from .prompt_corpus_loader import load_embedded_prompt_corpus
from .prompt_blueprint import PromptBlueprint

TECHNICAL_BLUEPRINT = ["full", "empty"]

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


def get_embedded_prompt_blueprints_names(exclude_technical_blueprint=False):
    """
    :param exclude_technical_blueprint: exclude technical blueprints
            ("full", "empty") from the resulted list
    :type exclude_technical_blueprint: bool, optional
    :return: names of all available embedded prompt blueprints,
            including specal case "full"
    :rtype: list(str)
    :raises FileNotFoundError:
    :raises OSError:
    """
    # todo sort names
    # FIXME test need

    opt = list(_get_embedded_prompt_blueprints_names_and_paths().keys())

    # include technical blueprints if required
    if not exclude_technical_blueprint:
        opt.extend(TECHNICAL_BLUEPRINT)

    return opt


def load_embedded_prompt_blueprint(prompt_blueprint_name):
    """
    Load one of the prompt blueprints embedded with this Python package


    :param prompt_blueprint_name: name of an embedded prompt blueprints,
            must be from ``get_embedded_prompt_blueprints_names()``;
            if ``'full'``: blueprint with **all nodes enabled**;
            if ``'empty'``: blueprint with **all nodes disabled** (detached mode)
    :type prompt_blueprint_name: str
    :return: v.s.
    :rtype: PromptBlueprint
    :raises FileNotFoundError:
    :raises IOError:
    :raises ValueError: prompt_name is
            not a recognized embedded prompt blueprint
    """
    corpus = load_embedded_prompt_corpus()

    # deal with technical prompts
    # technical blueprints
    # FIXME need tests
    if prompt_blueprint_name == "full":
        return PromptBlueprint.create_full_prompt_blueprint(corpus)
    elif prompt_blueprint_name == "empty":
        return PromptBlueprint(corpus)

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
        return PromptBlueprint(corpus, content)


def _get_embedded_prompt_blueprints_names_and_paths():
    """
    :return: names and full paths of all available embedded prompt blueprints;
            does *not* include technical blueprints
    :rtype: dict{str: str}
    """
    folder_path = get_embedded_prompt_blueprints_folder_path()
    files_paths = os.listdir(folder_path)
    # Filter out directories, keeping only files and removing extensions
    opt = {
        os.path.splitext(file)[0]: os.path.join(folder_path, file)
        for file in files_paths
        if os.path.isfile(os.path.join(folder_path, file))
    }
    return opt

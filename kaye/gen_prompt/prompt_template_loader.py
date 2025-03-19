# TODO

from pathlib import Path


def _get_prompt_templates_folder_path():
    """
    :return: absolute path to ``prompt_templates`` folder
    :rtype: Path
    """
    # find folder path by relative path from this script
    return (Path(__file__).resolve().parent / "prompt_templates").absolute()

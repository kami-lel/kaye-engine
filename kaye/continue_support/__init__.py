"""
define ``update_continue_local_config_folder``
"""

from pathlib import Path


def update_continue_local_config_folder(continue_local_config_folder):
    """
    update the Continue local config folder with the updated kaye prompts


    :param continue_local_config_folder: path to folder containing
            continue local configs,
            i.e. the ``.continue/`` folder containing
            ``config.yaml``, ``sessions/``, ``rules/``, etc.
    :type continue_local_config_folder: Path-like
    """
    folder = Path(continue_local_config_folder)
    rules_folder = (folder / "rules").resolve()

    print(rules_folder)  # HACK

    # todo support prompts updating

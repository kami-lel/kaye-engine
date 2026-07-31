"""
settings.py

define ``update_settings_json`` — configure VS Code Extension settings
(git command permissions)
"""

import json
from pathlib import Path

import json5

# constants  ###################################################################

_SETTINGS_FILENAME = "settings.json"

_PERMISSION_CMDS_PATH = Path(__file__).parent.parent / "permission_cmds.jsonc"
_PERMISSION_FIELDS = ("ask", "deny", "allow")


# helpers  #####################################################################


def _build_settings(permission_cmds):
    return {
        "permissions": {
            field: permission_cmds[field] for field in _PERMISSION_FIELDS
        },
    }


def _set_permissions(data, permission_cmds):
    perms = data.setdefault("permissions", {})

    for field in _PERMISSION_FIELDS:
        perms[field] = permission_cmds[field]


# Public API  ##################################################################


def update_settings_json(claude_folder):
    """
    update settings.json for git command permissions


    :param claude_folder: path to .claude/ folder
    :type claude_folder: Path-like
    :return: path to the written settings.json
    :rtype: Path
    """
    with open(_PERMISSION_CMDS_PATH, encoding="utf-8") as f:
        permission_cmds = json5.load(f)

    settings_path = Path(claude_folder) / _SETTINGS_FILENAME
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        # Fixme utilize kamilog here
        with open(settings_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = _build_settings(permission_cmds)

    _set_permissions(data, permission_cmds)

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return settings_path

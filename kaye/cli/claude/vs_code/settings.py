"""
settings.py

define ``update_settings_json`` — configure VS Code Extension settings
(pre-compact hook and git command permissions)
"""

import json
from pathlib import Path

import json5

from kaye.prompt import REPLACEMENT_NEWLINE_SYMBOL, load_prompt_corpus_tree
from kaye.prompt.blueprint import PromptBlueprint, render
from kaye.cli.claude import CONTAINING_SIDECARS

# BUG not sure if pre compact hook is triggered

# constants  ###################################################################

_SETTINGS_FILENAME = "settings.json"
_HOOK_MATCHER = "*"
_HOOK_TYPE = "prompt"

_PERMISSION_CMDS_PATH = Path(__file__).parent.parent / "permission_cmds.jsonc"
_PERMISSION_FIELDS = ("ask", "deny", "allow")


# helpers  #####################################################################


def _build_settings(prompt, permission_cmds):
    return {
        "hooks": {
            "PreCompact": [{
                "matcher": _HOOK_MATCHER,
                "hooks": [{"type": _HOOK_TYPE, "prompt": prompt}],
            }]
        },
        "permissions": {
            field: permission_cmds[field] for field in _PERMISSION_FIELDS
        },
    }


def _set_pre_compact_prompt(data, prompt):
    hooks = data.setdefault("hooks", {})
    pre_compact = hooks.setdefault("PreCompact", [])

    for entry in pre_compact:
        if entry.get("matcher") == _HOOK_MATCHER:
            for hook in entry.get("hooks", []):
                if hook.get("type") == _HOOK_TYPE:
                    hook["prompt"] = prompt
                    return
            entry.setdefault("hooks", []).append(
                {"type": _HOOK_TYPE, "prompt": prompt}
            )
            return

    pre_compact.append({
        "matcher": _HOOK_MATCHER,
        "hooks": [{"type": _HOOK_TYPE, "prompt": prompt}],
    })


def _set_permissions(data, permission_cmds):
    perms = data.setdefault("permissions", {})

    for field in _PERMISSION_FIELDS:
        perms[field] = permission_cmds[field]


# Public API  ##################################################################


def update_settings_json(claude_folder):
    """
    update settings.json for pre-compact hook and git command permissions


    :param claude_folder: path to .claude/ folder
    :type claude_folder: Path-like
    :return: path to the written settings.json
    :rtype: Path
    """
    # create local blueprint with single node
    _node = load_prompt_corpus_tree()["Projects"]["Maintenance Before Compact"]
    bp = PromptBlueprint.create_from_node(_node)

    lines = render.render_prompt_lines(
        bp, contains_sidecars=CONTAINING_SIDECARS
    )

    # convert to single line compact format
    single_line = REPLACEMENT_NEWLINE_SYMBOL.join(lines)

    with open(_PERMISSION_CMDS_PATH, encoding="utf-8") as f:
        permission_cmds = json5.load(f)

    settings_path = Path(claude_folder) / _SETTINGS_FILENAME
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        with open(settings_path, encoding="utf-8") as f:
            data = json.load(f)
        _set_pre_compact_prompt(data, single_line)
    else:
        data = _build_settings(single_line, permission_cmds)

    _set_permissions(data, permission_cmds)

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return settings_path

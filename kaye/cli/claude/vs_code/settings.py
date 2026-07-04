"""
settings.py

define ``update_settings_json`` — configure VS Code Extension settings
(pre-compact hook and git command permissions)
"""

import json
import re
from pathlib import Path

from kaye.prompt import REPLACEMENT_NEWLINE_SYMBOL, load_prompt_corpus_tree
from kaye.prompt.prompt_blueprint import PromptBlueprint
from kaye.cli.claude import CONTAINING_META_NODES

# Bug not sure if pre compact hook is triggered

# constants  ###################################################################

_SETTINGS_FILENAME = "settings.json"
_HOOK_MATCHER = "*"
_HOOK_TYPE = "prompt"

_ASK_PERMISSION_CMDS_PATH = (
    Path(__file__).parent.parent / "ask_permission_cmds.jsonc"
)

_JSONC_COMMENT_RE = re.compile(
    r'"(?:\\.|[^"\\])*"|(//[^\n]*)', re.MULTILINE
)


# helpers  #####################################################################


def _strip_jsonc_comments(text):
    return _JSONC_COMMENT_RE.sub(
        lambda m: "" if m.group(1) else m.group(0), text
    )


def _load_ask_permission_cmds():
    raw = _ASK_PERMISSION_CMDS_PATH.read_text(encoding="utf-8")
    return json.loads(_strip_jsonc_comments(raw))


def _build_settings(prompt, permission_list):
    return {
        "hooks": {
            "PreCompact": [{
                "matcher": _HOOK_MATCHER,
                "hooks": [{"type": _HOOK_TYPE, "prompt": prompt}],
            }]
        },
        "permissions": {
            "ask": permission_list,
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


def _set_permissions(data, permission_list):
    perms = data.setdefault("permissions", {})
    ask_perms = perms.setdefault("ask", [])

    for cmd in permission_list:
        if cmd not in ask_perms:
            ask_perms.append(cmd)


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

    lines = bp.generate_prompt_lines(contains_meta_nodes=CONTAINING_META_NODES)

    # convert to single line compact format
    single_line = REPLACEMENT_NEWLINE_SYMBOL.join(lines)

    ask_permission_cmds = _load_ask_permission_cmds()

    settings_path = Path(claude_folder) / _SETTINGS_FILENAME
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        with open(settings_path, encoding="utf-8") as f:
            data = json.load(f)
        _set_pre_compact_prompt(data, single_line)
    else:
        data = _build_settings(single_line, ask_permission_cmds)

    _set_permissions(data, ask_permission_cmds)

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return settings_path

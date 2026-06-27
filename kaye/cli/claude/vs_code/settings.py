"""
settings.py

define ``update_settings_json_for_pre_compact_hook``
"""

from kaye.prompt import REPLACEMENT_NEWLINE_SYMBOL
from kaye.prompt.prompt_blueprint import PromptBlueprint
from kaye.cli.claude import CONTAINING_META_NODES


def update_settings_json_for_pre_compact_hook(claude_folder):
    """
    update settings.json for pre-compact hook configuration


    :param claude_folder: path to .claude/ folder
    :type claude_folder: Path-like
    """
    # create local blueprint with single node
    bp = PromptBlueprint.create_empty_blueprint()

    lines = bp.generate_prompt_lines(contains_meta_nodes=CONTAINING_META_NODES)

    # convert to single line compact format
    single_line = REPLACEMENT_NEWLINE_SYMBOL.join(lines)

    # TODO update settings.json with single_line

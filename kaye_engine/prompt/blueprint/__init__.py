"""
kaye_engine/prompt/blueprint/

`Blueprint`: the frozen selection of corpus nodes, its pure edit functions,
JSON codec, text parser, binding, and rendering; the blueprint registry
mechanism
"""

from .data import (
    Blueprint,
    BlueprintMeta,
    create_blueprint,
    decode_blueprint,
    dump_blueprint,
    encode_blueprint,
    load_blueprint,
    parse_blueprint_json,
    save_blueprint,
)
from .dependencies import resolve_dependencies, trace_dependencies
from .diff import BlueprintDiff, diff_blueprints
from .dynamic_substitution import *
from .edit import (
    checkmark_nodes,
    create_blueprint_from_node,
    is_checkmarked,
    merge_blueprints,
    replace_meta,
    uncheckmark_nodes,
)
from .index import (
    BlueprintSelection,
    CorpusIndex,
    NodePath,
    get_corpus_index,
    get_corpus_node,
)
from .parser import parse_blueprint_tree
from .registry import *
from .render import (
    preview_blueprint,
    preview_blueprint_without_dependencies,
    preview_selection,
    register_comment_line,
    render_prompt,
    render_prompt_without_dependencies,
    show_dependencies,
    show_description,
    show_description_and_when_to_use,
    show_display_name,
    show_globs,
    show_when_to_use,
)
from .selection import bind_selection, resolve_selection
from .summary import BlueprintSummary, show_blueprint
from .validate import validate_blueprint

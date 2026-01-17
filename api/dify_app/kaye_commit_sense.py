"""
define API to specific work with Dify App: Kaye Commit Sense
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, request

from kaye import PROGRAM_NAME
from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus

# Blueprints  ##################################################################
PRIMARY_MESSAGE_PROMPT_BLUEPRINT = """ ○
[ ] ├── Style
[ ] │   ├── Capitalization Style
[x] │   │   └── Commentary Case
[x] │   └── Briefness Style
[ ] └── Role
[x]     └── Kaye Commit Sense
[x]         └── Primary Message Task
"""

PER_FILE_LONG_PROMPT_BLUEPRINT = """ ○
[ ] ├── Elements
[x] │   └── Annotation Markers
[ ] ├── Style
[ ] │   ├── Capitalization Style
[x] │   │   └── Commentary Case
[x] │   └── Briefness Style
[ ] └── Role
[x]     └── Kaye Commit Sense
[x]         └── Per File Summary Task
[x]             └── Prefix Symbol
[x]                 └── Long
"""

PER_FILE_SHORT_PROMPT_BLUEPRINT = """ ○
[ ] ├── Elements
[x] │   └── Annotation Markers
[ ] ├── Style
[ ] │   ├── Capitalization Style
[x] │   │   └── Commentary Case
[x] │   └── Briefness Style
[ ] └── Role
[x]     └── Kaye Commit Sense
[x]         └── Per File Summary Task
[x]             └── Prefix Symbol
[x]                 └── Short
"""


# helper method  ###############################################################
def _checkmark_md_related_node(blueprint):
    """
    checkmark the correct markdown related node
    """
    md_arg = request.args.get("flags")

    if md_arg and bool(int(md_arg)):  # allows md
        node = blueprint.corpus["Format"]

    else:  # disallow md
        node = blueprint.corpus["Role"]["Kaye Commit Sense"][
            "no markdown syntax"
        ]

    blueprint.checkmark(node)


# Flask Routing  ###############################################################

# /kaye/dify-app/kaye-commit-sense
commit_sense_bp = Blueprint(
    "kaye-commit-sense", PROGRAM_NAME, url_prefix="/kaye-commit-sense"
)


# /kaye/dify-app/kaye-commit-sense/primary-message
@commit_sense_bp.route("/primary-message", methods=["GET"])
def kaye_commit_sense_primary_message():
    blueprint = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        PRIMARY_MESSAGE_PROMPT_BLUEPRINT,
    )
    _checkmark_md_related_node(blueprint)
    return blueprint.generate_prompt()


# /kaye/dify-app/kaye-commit-sense/per-file-long
@commit_sense_bp.route("/per-file-long", methods=["GET"])
def kaye_commit_sense_per_file_long():
    blueprint = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        PER_FILE_LONG_PROMPT_BLUEPRINT,
    )
    _checkmark_md_related_node(blueprint)
    return blueprint.generate_prompt()


# /kaye/dify-app/kaye-commit-sense/per-file-short
@commit_sense_bp.route("/per-file-short", methods=["GET"])
def kaye_commit_sense_per_file_short():
    blueprint = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        PER_FILE_SHORT_PROMPT_BLUEPRINT,
    )
    _checkmark_md_related_node(blueprint)
    return blueprint.generate_prompt()

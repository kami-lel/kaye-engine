"""
kaye_commit_sense.py

define API to specific work with Dify App: Kaye Commit Sense
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, request, abort, Response

from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint

# Blueprints  ##################################################################
PRIMARY_MESSAGE_PROMPT_BLUEPRINT = """    ○
[ ] ├── Style Guide
[ ] │   ├── Style Guide Capitalization
[x] │   │   └── Commentary Case
[x] │   └── Style Guide Briefness Style
[x] └── Kaye Commit Sense
[x]     └── Primary Message Task
"""

PER_FILE_LONG_PROMPT_BLUEPRINT = """ ○
[ ] ├── Elements
[x] │   └── Annotation Markers
[ ] ├── Style Guide
[ ] │   ├── Style Guide Capitalization
[x] │   │   └── Commentary Case
[x] │   └── Style Guide Briefness Style
[x] └── Kaye Commit Sense
[x]     └── Per File Summary Task
[x]         └── Prefix Symbol
[x]             └── Long
"""

PER_FILE_SHORT_PROMPT_BLUEPRINT = """ ○
[ ] ├── Elements
[x] │   └── Annotation Markers
[ ] ├── Style Guide
[ ] │   ├── Style Guide Capitalization
[x] │   │   └── Commentary Case
[x] │   └── Style Guide Briefness Style
[x] └── Kaye Commit Sense
[x]     └── Per File Summary Task
[x]         └── Prefix Symbol
[x]             └── Short
"""


# helper method  ###############################################################
def _checkmark_md_related_node(blueprint):
    """
    checkmark the correct markdown related node
    """
    md_arg = request.args.get("allows_md")

    node = blueprint.corpus["Kaye Commit Sense"]["no markdown syntax"]

    if md_arg:
        try:
            md_value = int(md_arg)
        except ValueError:
            abort(Response("bad param: ?allows_md={}".format(md_arg), 422))

        if md_value == 1:
            node = blueprint.corpus["Format"]
        elif md_value != 0:
            abort(
                Response(
                    "param ?allows_md must be 1/0: {}".format(md_value),
                    422,
                )
            )

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
        PRIMARY_MESSAGE_PROMPT_BLUEPRINT,
    )
    _checkmark_md_related_node(blueprint)
    return blueprint.generate_prompt()


# /kaye/dify-app/kaye-commit-sense/per-file-long
@commit_sense_bp.route("/per-file-long", methods=["GET"])
def kaye_commit_sense_per_file_long():
    blueprint = PromptBlueprint.parse(
        PER_FILE_LONG_PROMPT_BLUEPRINT,
    )
    _checkmark_md_related_node(blueprint)
    return blueprint.generate_prompt()


# /kaye/dify-app/kaye-commit-sense/per-file-short
@commit_sense_bp.route("/per-file-short", methods=["GET"])
def kaye_commit_sense_per_file_short():
    blueprint = PromptBlueprint.parse(
        PER_FILE_SHORT_PROMPT_BLUEPRINT,
    )
    _checkmark_md_related_node(blueprint)
    return blueprint.generate_prompt()

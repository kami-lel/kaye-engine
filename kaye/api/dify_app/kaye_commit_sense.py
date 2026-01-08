"""
define API to specific work with Dify App: Kaye Commit Sense
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

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

# Flask Routing  ###############################################################

# /kaye/dify-app/kaye-commit-sense
commit_sense_bp = Blueprint(
    "kaye-commit-sense", PROGRAM_NAME, url_prefix="/kaye-commit-sense"
)


# /kaye/dify-app/kaye-commit-sense/primary-message
@commit_sense_bp.route("/primary-message", methods=["GET"])
def kaye_commit_sense_primary_message():
    blueprint = PromptBlueprint(
        load_embedded_prompt_corpus(),
        PRIMARY_MESSAGE_PROMPT_BLUEPRINT,
    )
    return str(blueprint)


# /kaye/dify-app/kaye-commit-sense/per-file-long
@commit_sense_bp.route("/per-file-long", methods=["GET"])
def kaye_commit_sense_per_file_long():
    return "not implemented yet"  # TODO


# /kaye/dify-app/kaye-commit-sense/per-file-short
@commit_sense_bp.route("/per-file-short", methods=["GET"])
def kaye_commit_sense_per_file_short():
    return "not implemented yet"  # TODO

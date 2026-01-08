"""
define API to specific work with Dify App: Kaye Peer Coder
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, request, jsonify

from kaye import PROGRAM_NAME
from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus

# Blueprints  ##################################################################
PRE_SENSE_PROMPT_BLUEPRINT = """ ○
[x] ├── Role
[x] │   └── Kaye Peer Coder
[x] │       └── pre-sense
[x] └── Abbreviations
[x]     └── Programming Languages
"""


TASK_PROMPT_BASIC_BLUEPRINT = """ ○
[x] ├── Introduction
[x] ├── Style
[x] │   ├── Capitalization Style
[x] │   │   └── Commentary Case
[x] │   └── Briefness Style
[x] ├── Format
[x] └── Role
[x]     └── Peer Coder
[x]         └── Code Comment
"""


# Flask Routing  ###############################################################

# /kaye/dify-app/kaye-peer-coder
kyc_bp = Blueprint(
    "kaye-peer-coder", PROGRAM_NAME, url_prefix="/kaye-peer-coder"
)


# /kaye/dify-app/kaye-peer-coder/pre-sense
@kyc_bp.route("/pre-sense", methods=["GET"])
def kaye_peer_coder_pre_sense():
    blueprint = PromptBlueprint(
        load_embedded_prompt_corpus(),
        PRE_SENSE_PROMPT_BLUEPRINT,
    )
    return str(blueprint)


# /kaye/dify-app/kaye-peer-coder/task
@kyc_bp.route("/task", methods=["GET"])
def kaye_peer_coder_task():
    # BUG need test
    languages_arg = request.args.get("languages")

    result = {"abc": 1, "def": "ghi", "languages": languages_arg}
    return jsonify(result)

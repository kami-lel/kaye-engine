"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, request, abort, Response


from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint

# Blueprints  ##################################################################
PRE_SENSE_PROMPT_BLUEPRINT = """ ○
[x] └── Kaye Chat
[x]     └── sense
[ ]         ├── llm
[ ]         ├── role
[ ]         ├── leave empty
[ ]         └── for coder
[ ]             ├── programming_languages
[ ]             │   └── {Programming Languages Code}
[ ]             └── difficulty
"""


RAPID_PROMPT_BLUEPRINT = ""

CHAT_PROMPT_BLUEPRINT = ""

CODER_PROMPT_BLUEPRINT = """ ○
[x] ├── Introduction
[x] ├── Style
[x] │   ├── Capitalization Style
[x] │   │   └── Commentary Case
[x] │   └── Briefness Style
[x] ├── Format
[x] └── Role
[x]     └── Kaye Peer Coder
[x]         └── chat
"""


TASK_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Elements
[x] │   └── Date & Time Format
[ ] ├── Style
[x] │   └── Capitalization Style
[x] │       ├── Title Case
[x] │       └── Commentary Case
[x] ├── Format
[x] ├── Standards
[x] │   ├── Numerical Values with Units:
[x] │   ├── Language code
[x] │   └── International Phonetic Alphabet
[x] └── Role"""


# Flask Routing  ###############################################################
# /kaye/dify-app/ky
ky_bp = Blueprint("kaye-chat", PROGRAM_NAME, url_prefix="/ky")


# /kaye/dify-app/ky/sense  =====================================================
@ky_bp.route("/sense", methods=["GET"])
def kaye_chat_sense():
    role = request.args.get("role")

    blueprint = PromptBlueprint.parse(
        PRE_SENSE_PROMPT_BLUEPRINT, disable_prune=True
    )
    pre_sense_node = blueprint.corpus["Kaye Chat"]["sense"]

    # on role  -----------------------------------------------------------------
    if role:
        if role == "peer_coder":
            blueprint.checkmark(pre_sense_node["for coder"], recursively=True)
        else:
            # other role
            blueprint.checkmark(pre_sense_node["llm"])
            blueprint.checkmark(pre_sense_node["leave empty"])

    else:
        blueprint.checkmark(pre_sense_node["leave empty"])
        blueprint.checkmark(pre_sense_node["llm"])
        blueprint.checkmark(pre_sense_node["role"])

    # create concrete prompt  --------------------------------------------------
    return blueprint.generate_prompt()


# /kaye/dify-app/ky/task  ======================================================
@ky_bp.route("/task", methods=["GET"])
def kaye_chat_task():
    role = request.args.get("role")
    programming_languages = request.args.get("programming_languages")

    # TODO TODO

    # create blueprint based on role
    if role == "rapid":
        bp = _create_rapid_bp()

    if role == "chat":
        bp = _create_chat_bp()

    if role == "peer_coder":
        bp = PromptBlueprint.parse(CODER_PROMPT_BLUEPRINT, disable_prune=True)

    else:
        return abort(Response("bad param: ?role={}".format(role), 422))

    # TODO use AbbrNode for ky

    return bp.generate_prompt()


# helpers  #####################################################################


def _create_rapid_bp():
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT, disable_prune=True)


def _create_chat_bp():
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT, disable_prune=True)

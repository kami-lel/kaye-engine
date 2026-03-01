"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, request, abort, Response


from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint, load_embedded_blueprint

# constants  ###################################################################
PARAM_ROLE_KEY = "role"
PARAM_PROGRAMMING_LANGUAGES_KEY = "programming_languages"

# roles  -----------------------------------------------------------------------
ROLE_CHAT = "chat"
ROLE_CODER = "peer_coder"
ROLE_RAPID = "rapid"


# Blueprints  ##################################################################
# sense blueprint  -------------------------------------------------------------

SENSE_PROMPT_BLUEPRINT = """ ○
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


# task blueprints  -------------------------------------------------------------


# HACK rm these

CHAT_PROMPT_BLUEPRINT = """    ○
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


""" ○
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


# Flask Routing  ###############################################################
# /kaye/dify-app/ky
ky_bp = Blueprint("kaye-chat", PROGRAM_NAME, url_prefix="/ky")


# /kaye/dify-app/ky/sense  =====================================================
@ky_bp.route("/sense", methods=["GET"])
def kaye_chat_sense():
    role = request.args.get(PARAM_ROLE_KEY)

    blueprint = PromptBlueprint.parse(
        SENSE_PROMPT_BLUEPRINT, disable_prune=True
    )
    pre_sense_node = blueprint.corpus["Kaye Chat"]["sense"]

    # on role  -----------------------------------------------------------------
    if role:
        if role == ROLE_CODER:
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
    role = request.args.get(PARAM_ROLE_KEY) or ROLE_CHAT  # default to chat
    pls = request.args.get(PARAM_PROGRAMMING_LANGUAGES_KEY)

    if role == ROLE_RAPID:
        bp = load_embedded_blueprint("rapid")

    if role == ROLE_CHAT:
        bp = PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)

    else:
        return abort(Response("bad param: ?role={}".format(role), 422))

    # TODO use AbbrNode for ky
    return bp.generate_prompt()

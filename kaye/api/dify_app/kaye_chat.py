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


RAPID_PROMPT_BLUEPRINT = """"""

CHAT_PROMPT_BLUEPRINT = """"""

# HACK rm these
TASK_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[ ] ├── Language
[ ] ├── Elements
[ ] │   ├── Annotation Markers
[ ] │   │   └── Meaning
[ ] │   └── Date & Time Format
[ ] ├── Style
[ ] │   ├── Capitalization Style
[ ] │   │   ├── Title Case
[ ] │   │   └── Commentary Case
[ ] │   └── Briefness Style
[ ] ├── Format
[ ] │   └── Header Separation
[ ] │       ├── Long File
[ ] │       └── Medium File
[ ] ├── Standards
[ ] │   ├── Numerical Values with Units:
[ ] │   ├── Language code
[ ] │   └── International Phonetic Alphabet
[ ] ├── Kaye Chat
[ ] │   └── sense
[ ] │       ├── llm
[ ] │       ├── role
[ ] │       ├── leave empty
[ ] │       └── for coder
[ ] │           ├── programming_languages
[ ] │           └── difficulty
[ ] ├── Role
[ ] │   ├── Art Tutor
[ ] │   ├── Changelog Writer
[ ] │   ├── Conversation Follow Up Generation
[ ] │   ├── Conversation Tag Generation
[ ] │   ├── Conversation Title Generation
[ ] │   ├── Deutschlehrer
[ ] │   ├── Editor
[ ] │   ├── Email Secretary
[ ] │   ├── Encyclopedic
[ ] │   ├── Etiquette Coach
[ ] │   ├── Grammar Checker
[ ] │   ├── Kaye Peer Coder
[ ] │   │   ├── chat
[ ] │   │   ├── C
[ ] │   │   ├── C++
[ ] │   │   ├── Unreal Engine
[ ] │   │   ├── C Sharp
[ ] │   │   ├── Unity Engine
[ ] │   │   ├── GDScript
[ ] │   │   ├── HTML
[ ] │   │   ├── JavaScript & TypeScript
[ ] │   │   │   └── Documentation and Comments
[ ] │   │   ├── Qt
[ ] │   │   │   └── QML
[ ] │   │   ├── Python
[ ] │   │   └── Message Level
[ ] │   ├── Librarian
[ ] │   │   └── Bibliographer
[ ] │   ├── Prompt Writer
[ ] │   ├── Shelver
[ ] │   │   ├── label
[ ] │   │   │   ├── book title
[ ] │   │   │   ├── publish year
[ ] │   │   │   ├── authors, editors, translators
[ ] │   │   │   ├── publisher
[ ] │   │   │   ├── informational tags
[ ] │   │   │   └── label examples
[ ] │   │   ├── DDC part
[ ] │   │   └── DDC justification
[ ] │   ├── Chinese Shelver
[ ] │   │   ├── DDC 部分
[ ] │   │   └── DDC 說明
[ ] │   ├── Tarot Reader
[ ] │   │   ├── 1. Information Collection Stage
[ ] │   │   ├── 2. Card Drawing Stage
[ ] │   │   ├── 3. Interpretation Stage
[ ] │   │   └── Tarot Card Reference
[ ] │   └── Translator
[ ] ├── Kaye Cash Tracker
[ ] │   └── Extract
[ ] ├── Kaye Commit Sense
[ ] │   ├── no markdown syntax
[ ] │   ├── Primary Message Task
[ ] │   └── Per File Summary Task
[ ] │       └── Prefix Symbol
[ ] │           ├── Long
[ ] │           └── Short
[ ] └── Kaye Event Radar
[ ]     ├── parse events
[ ]     └── filter events"""


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
    return ""  # HACK
    role = request.args.get("role")
    programming_languages = request.args.get("programming_languages")

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

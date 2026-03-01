"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring


from sys import stderr

from flask import Blueprint, request, abort, Response


from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint, load_embedded_blueprint

# constants  ###################################################################
PARAM_ROLE_KEY = "role"
PARAM_PROGRAMMING_LANGUAGES_KEY = "programming_languages"

# roles  -----------------------------------------------------------------------
ROLE_CHAT = "chat"
ROLE_CODER = "coder"
ROLE_RAPID = "rapid"


# Blueprints  ##################################################################

# sense blueprints  ============================================================

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


# task blueprints  =============================================================

CHAT_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Elements
[x] │   └── Date & Time Format
[x] ├── Style
[x] │   └── Capitalization Style
[x] │       ├── Title Case
[x] │       └── Commentary Case
[x] ├── Format
[x] ├── Standards
[x] │   └── Numerical Values with Units
[x] └── Role"""


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
    pls = request.args.get(PARAM_PROGRAMMING_LANGUAGES_KEY) or ""

    if role == ROLE_CODER:
        bp = _create_peer_coder_blueprint(pls)

    elif role == ROLE_RAPID:
        bp = load_embedded_blueprint("rapid")

    elif role == ROLE_CHAT:
        bp = _create_chat_blueprint()

    else:
        return abort(Response("bad param: ?role={}".format(role), 422))

    # todo ky: use AbbrNode
    return bp.generate_prompt()


# helpers  *********************************************************************


def _create_chat_blueprint():
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)


def _create_peer_coder_blueprint(pls):
    # create base bp from chat
    bp = _create_chat_blueprint()

    # add Kaye Peer Coder node
    kyc_node = bp.corpus["Role"]["Kaye Peer Coder"]
    bp.checkmark(kyc_node)

    # adds PL nodes  -----------------------------------------------------------
    for plc in pls.split(","):
        if plc == "c":
            bp.checkmark(kyc_node["C"])

        elif plc == "cpp":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["C++"])

        elif plc == "ue":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["C++"])
            bp.checkmark(kyc_node["Unreal Engine"])

        elif plc == "csharp":
            bp.checkmark(kyc_node["C Sharp"])

        elif plc == "u3d":
            bp.checkmark(kyc_node["C Sharp"])
            bp.checkmark(kyc_node["Unity Engine"])

        elif plc == "gdscript":
            bp.checkmark(kyc_node["GDScript"])

        elif plc == "html":
            bp.checkmark(kyc_node["HTML"])

        elif plc in ("js", "ts"):
            bp.checkmark(kyc_node["JavaScript & TypeScript"], recursively=True)

        elif plc == "qt":
            bp.checkmark(kyc_node["Qt"])

        elif plc == "qml":
            bp.checkmark(kyc_node["Qt"])
            bp.checkmark(kyc_node["Qt"]["QML"])

        elif plc == "py":
            bp.checkmark(kyc_node["Python"], recursively=True)

        elif plc == "console":
            bp.checkmark(kyc_node["Message Level"])

        elif plc != "":
            print(
                "unrecognized PLC: {} in ?programming_languages={}".format(
                    plc, pls
                ),
                file=stderr,
            )

    return bp


PLC2CORPUS_HEADING = {
    "c": ("C",),
    "cpp": ("C++",),
    "ue": ("Unreal Engine",),
    "csharp": ("C Sharp",),
    "u3d": ("C Sharp", "Unity Engine"),
    "gdscript": ("GDSCript",),
    "html": ("HTML",),
    "js": ("JavaScript & TypeScript",),
    "ts": ("JavaScript & TypeScript",),
    "qt": ("Qt",),
    "qml": ("Qt", "QML"),
    "py": ("Python",),
}

"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring


from sys import stderr

from flask import Blueprint, request, abort, Response


from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint, load_embedded_blueprint

# constants  ###################################################################
BODY_ROLE_KEY = "role"
BODY_PROGRAMMING_LANGUAGES_KEY = "programming_languages"
BODY_QUERY_KEY = "query"


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
[x] ├── Format
[x] ├── Elements
[x] │   └── Numerical Values with Units
[x] ├── Role
[x] └── {Abbreviations}"""


RAPID_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Format
[x] └── {Abbreviations}"""


# Flask Routing  ###############################################################
# /kaye/dify-app/ky
ky_bp = Blueprint("kaye-chat", PROGRAM_NAME, url_prefix="/ky")


# /kaye/dify-app/ky/sense  =====================================================
@ky_bp.route("/sense", methods=["GET"])
def kaye_chat_sense():
    role = request.args.get(BODY_ROLE_KEY)

    blueprint = PromptBlueprint.parse(
        SENSE_PROMPT_BLUEPRINT, disable_prune=True
    )
    pre_sense_node = blueprint.corpus["Kaye Chat"]["sense"]

    # on role  -----------------------------------------------------------------
    if role:
        if role == "coder":
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
    body = request.get_json(silent=True) or {}

    # default to chat
    role = body.get(BODY_ROLE_KEY) or "chat"
    pls = body.get(BODY_PROGRAMMING_LANGUAGES_KEY) or ""
    query = body.get(BODY_QUERY_KEY) or ""

    # create bp  ---------------------------------------------------------------
    if role == "chat":
        bp = _create_chat_blueprint()

    elif role == "rapid":
        bp = _create_rapid_blueprint()

    elif role == "coder":
        bp = _create_peer_coder_blueprint(pls)

    elif role == "barista":
        bp = _create_barista_blueprint()

    elif role == "editor":
        bp = _create_editor_blueprint()

    elif role == "secretary":
        bp = _create_secretary_blueprint()

    else:
        return abort(
            Response("bad value of 'role' in body: {}".format(role), 422)
        )

    # query and abbr  ----------------------------------------------------------
    kwargs = {"query": query}

    return bp.generate_prompt(**kwargs)


# task blueprints  #############################################################


def _create_rapid_blueprint():
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT)


def _create_chat_blueprint():  # ===============================================
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)


def _create_peer_coder_blueprint(pls):  # ======================================
    # pylint: disable=too-many-branches
    # create base bp from chat
    bp = _create_chat_blueprint()

    # add styles
    bp.checkmark("Style", recursively=True)

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


def _create_barista_blueprint():  # ============================================
    bp = _create_rapid_blueprint()
    bp.checkmark("Date & Time Format")
    bp.checkmark("Assistant Barista", recursively=True)
    return bp


def _create_changelog_blueprint():  # ==========================================
    # fixme changelog blueprint not used
    bp = _create_chat_blueprint()
    bp.checkmark("Changelog Writer")
    return bp


def _create_editor_blueprint():  # =============================================
    bp = _create_chat_blueprint()
    bp.checkmark(bp.corpus["Style"]["Good Writing"])
    bp.checkmark(bp.corpus["Role"]["Editor"], recursively=True)
    return bp


def _create_secretary_blueprint():  # ==========================================
    bp = _create_chat_blueprint()
    bp.checkmark(bp.corpus["Style"]["Good Writing"])
    bp.checkmark(bp.corpus["Role"]["Secretary"])
    return bp

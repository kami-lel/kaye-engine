"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring

# FIXME refactor api


from flask import Blueprint, request, abort, Response


from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint
from kaye.api.dify_app.kaye_chat_sense import kaye_chat_sense
from kaye.api.dify_app.kaye_chat_merge import kaye_chat_merge

# constants  ###################################################################
BODY_PROGRAMMING_LANGUAGES_KEY = "programming_languages"
BODY_QUERY_KEY = "query"


# Blueprints  ##################################################################

# sense blueprints  ============================================================

# task blueprints  =============================================================

CHAT_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Elements
[x] │   ├── Date & Time Format
[x] │   └── Numerical Values with Units
[x] ├── Format
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
@ky_bp.route("/sense", methods=["POST"])
def kaye_chat_sense_endpoint():
    return kaye_chat_sense()


# /kaye/dify-app/ky/task  ======================================================
@ky_bp.route("/task", methods=["POST"])
def kaye_chat_task():
    body = request.get_json(silent=True) or {}

    # default to chat
    role = body.get("role") or "chat"
    pls = body.get(BODY_PROGRAMMING_LANGUAGES_KEY) or ""
    query = body.get(BODY_QUERY_KEY) or ""

    # create bp  ---------------------------------------------------------------
    if role == "art":
        bp = _create_art_blueprint()

    elif role == "barista":
        bp = _create_barista_blueprint()

    elif role == "changelog":
        bp = _create_changelog_blueprint()

    elif role == "chat":
        bp = _create_chat_blueprint()

    elif role == "coder":
        bp = _create_peer_coder_blueprint(pls)

    elif role == "deutschlehrer":
        bp = _create_deutschlehrer_blueprint()

    elif role == "editor":
        bp = _create_editor_blueprint()

    elif role == "librarian":
        bp = _create_librarian_blueprint()

    elif role == "prompt":
        bp = _create_prompt_blueprint()

    elif role == "rapid":
        bp = _create_rapid_blueprint()

    elif role == "secretary":
        bp = _create_secretary_blueprint()

    elif role == "tarot":
        bp = _create_tarot_blueprint()

    else:
        return abort(
            Response("bad value of 'role' in body: {}".format(role), 422)
        )

    # query and abbr  ----------------------------------------------------------
    kwargs = {"query": query}

    return bp.generate_prompt(**kwargs)


# /kaye/dify-app/ky/merge
@ky_bp.route("/merge", methods=["GET"])
def kaye_chat_merge_endpoint():
    return kaye_chat_merge()


# task blueprints  #############################################################


def _create_rapid_blueprint():  # ==============================================
    return PromptBlueprint.parse(RAPID_PROMPT_BLUEPRINT)


def _create_chat_blueprint():  # ===============================================
    return PromptBlueprint.parse(CHAT_PROMPT_BLUEPRINT)


def _create_peer_coder_blueprint(pls):  # ======================================
    # pylint: disable=too-many-branches
    # create base bp from chat
    bp = _create_chat_blueprint()

    # add styles
    bp.checkmark("Style", recursively=True)

    # add ams
    bp.checkmark(bp.corpus["Elements"]["Annotation Markers"], recursively=True)

    # add Kaye Peer Coder node
    kyc_node = bp.corpus["Role"]["Kaye Peer Coder"]
    bp.checkmark(kyc_node)

    # adds PL nodes  -----------------------------------------------------------
    for plc in pls.split(","):
        if plc == "bash":
            bp.checkmark(kyc_node["Bash"])

        elif plc == "c":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "cpp":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["C++"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "ue":
            bp.checkmark(kyc_node["C"])
            bp.checkmark(kyc_node["C++"])
            bp.checkmark(kyc_node["Unreal Engine"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "csharp":
            bp.checkmark(kyc_node["C Sharp"])
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "u3d":
            bp.checkmark(kyc_node["C Sharp"])
            bp.checkmark(kyc_node["Unity Engine"], recursively=True)
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "gdscript":
            bp.checkmark(kyc_node["GDScript"])

        elif plc == "html":
            bp.checkmark(kyc_node["HTML"])

        elif plc in ("js", "ts"):
            bp.checkmark(kyc_node["JavaScript & TypeScript"], recursively=True)
            bp.checkmark(kyc_node["Brace Style"])

        elif plc == "py":
            bp.checkmark(kyc_node["Python"], recursively=True)

    return bp


def _create_art_blueprint():  # ============================================
    bp = _create_rapid_blueprint()
    bp.checkmark("Art Tutor", recursively=True)
    return bp


def _create_barista_blueprint():  # ============================================
    bp = _create_rapid_blueprint()
    bp.checkmark("Date & Time Format")
    bp.checkmark("Assistant Barista", recursively=True)
    return bp


def _create_changelog_blueprint():  # ==========================================
    bp = _create_chat_blueprint()
    bp.checkmark("Changelog Writer", recursively=True)
    return bp


def _create_librarian_blueprint():  # ==========================================
    bp = _create_chat_blueprint()
    bp.checkmark("Librarian", recursively=True)
    return bp


def _create_prompt_blueprint():  # ==========================================
    bp = _create_rapid_blueprint()
    bp.checkmark("Prompt Writer")
    return bp


def _create_deutschlehrer_blueprint():  # ======================================
    bp = _create_chat_blueprint()
    bp.checkmark("Deutschlehrer")
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


def _create_tarot_blueprint():  # ==========================================
    bp = _create_rapid_blueprint()
    bp.checkmark("Tarot Reader", recursively=True)
    return bp

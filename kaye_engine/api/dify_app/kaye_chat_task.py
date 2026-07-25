"""
kaye_chat_task.py

define endpoint behavior of: /kaye/dify-app/ky/task
"""

# pylint: disable=missing-function-docstring


from flask import request, abort, Response

from kaye.prompt.blueprint import PromptBlueprint, BLUEPRINT_REGISTRIES

_BR = BLUEPRINT_REGISTRIES

rapid_blueprint = _BR["rapid"].blueprint
chat_blueprint = _BR["chat"].blueprint
date_time_blueprint = _BR["date-time"].blueprint
number_unit_blueprint = _BR["number-unit"].blueprint
style_blueprint = _BR["style"].blueprint
triage_tags_blueprint = _BR["triage-tags"].blueprint
coder_blueprint = _BR["coder"].blueprint
coder_bash_blueprint = _BR["coder-bash"].blueprint
project_changelog_blueprint = _BR["project-changelog"].blueprint
coder_c_blueprint = _BR["coder-c"].blueprint
coder_cpp_blueprint = _BR["coder-cpp"].blueprint
coder_ue_blueprint = _BR["coder-ue"].blueprint
coder_csharp_blueprint = _BR["coder-csharp"].blueprint
coder_u3d_blueprint = _BR["coder-u3d"].blueprint
coder_gdscript_blueprint = _BR["coder-gdscript"].blueprint
coder_html_blueprint = _BR["coder-html"].blueprint
coder_js_ts_blueprint = _BR["coder-js-ts"].blueprint
coder_py_blueprint = _BR["coder-py"].blueprint
coder_py_docstring_blueprint = _BR["coder-py-docstring"].blueprint
coder_py_testing_blueprint = _BR["coder-py-testing"].blueprint
prompt_writer_blueprint = _BR["prompt-writer"].blueprint

# constant  ####################################################################
BODY_PROGRAMMING_LANGUAGES_KEY = "programming_languages"
BODY_QUERY_KEY = "query"

_user_scope_blueprint = PromptBlueprint.parse("""    ○
[x] ├── Role
[x] └── (Abbreviations)""")


# Entry Point  #################################################################
def kaye_chat_task():
    body = request.get_json(silent=True) or {}

    # default to chat
    role = body.get("role") or "chat"
    plcs = body.get(BODY_PROGRAMMING_LANGUAGES_KEY) or ""
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
        bp = _create_coder_blueprint(plcs)

    elif role == "deutschlehrer":
        bp = _create_deutschlehrer_blueprint()

    elif role == "editor":
        bp = _create_editor_blueprint()

    elif role == "librarian":
        bp = _create_librarian_blueprint()

    elif role == "prompt":
        bp = rapid_blueprint | _user_scope_blueprint | prompt_writer_blueprint

    elif role == "rapid":
        bp = rapid_blueprint | _user_scope_blueprint

    elif role == "secretary":
        bp = _create_secretary_blueprint()

    elif role == "shelver":
        bp = _create_shelver_blueprint()

    elif role == "tarot":
        bp = _create_tarot_blueprint()

    else:
        return abort(
            Response("bad value of 'role' in body: {}".format(role), 422)
        )

    # query and abbr  ----------------------------------------------------------
    kwargs = {"query": query}

    return bp.generate_prompt(**kwargs)


# task blueprints  #############################################################


def _create_chat_blueprint():
    bp = (
        chat_blueprint
        | _user_scope_blueprint
        | date_time_blueprint
        | number_unit_blueprint
    )
    return bp


def _create_coder_blueprint(plcs):
    bp = (
        chat_blueprint
        | _user_scope_blueprint
        | coder_blueprint
        | date_time_blueprint
        | number_unit_blueprint
        | style_blueprint
        | triage_tags_blueprint
    )
    bp.checkmark("Kaye Peer Coder")

    for plc in plcs.split(","):
        if plc == "bash":
            bp = bp | coder_bash_blueprint

        elif plc == "c":
            bp = bp | coder_c_blueprint

        elif plc == "cpp":
            bp = bp | coder_cpp_blueprint

        elif plc == "ue":
            bp = bp | coder_ue_blueprint

        elif plc == "csharp":
            bp = bp | coder_csharp_blueprint

        elif plc == "u3d":
            bp = bp | coder_u3d_blueprint

        elif plc == "gdscript":
            bp = bp | coder_gdscript_blueprint

        elif plc == "html":
            bp = bp | coder_html_blueprint

        elif plc in ("js", "ts"):
            bp = bp | coder_js_ts_blueprint

        elif plc == "py":
            bp = (
                bp
                | coder_py_blueprint
                | coder_py_docstring_blueprint
                | coder_py_testing_blueprint
            )

    return bp


def _create_art_blueprint():
    bp = rapid_blueprint | _user_scope_blueprint
    bp.checkmark("Art Tutor", recursively=True)
    return bp


def _create_barista_blueprint():
    bp = rapid_blueprint | _user_scope_blueprint
    bp.checkmark("Date and Time Format")
    bp.checkmark("Assistant Barista", recursively=True)
    return bp


def _create_changelog_blueprint():
    bp = _create_chat_blueprint() | project_changelog_blueprint
    return bp


def _create_deutschlehrer_blueprint():
    bp = _create_chat_blueprint()
    bp.checkmark("Deutschlehrer")
    return bp


def _create_editor_blueprint():
    bp = _create_chat_blueprint()
    bp.checkmark(bp.corpus["Style Guide"]["Style Guide Good Writing"])
    bp.checkmark(bp.corpus["Role"]["Editor"], recursively=True)
    return bp


def _create_librarian_blueprint():
    bp = _create_chat_blueprint()
    bp.checkmark("Librarian", recursively=True)
    return bp


def _create_secretary_blueprint():
    bp = _create_chat_blueprint()
    bp.checkmark(bp.corpus["Style Guide"]["Style Guide Good Writing"])
    bp.checkmark(bp.corpus["Role"]["Secretary"])
    return bp


def _create_shelver_blueprint():
    bp = _create_chat_blueprint()
    bp.checkmark(bp.corpus["Role"]["Shelver"], recursively=True)
    return bp


def _create_tarot_blueprint():
    bp = rapid_blueprint | _user_scope_blueprint
    bp.checkmark("Tarot Reader", recursively=True)
    return bp

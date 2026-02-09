"""
define API to specific work with Dify App: Kaye Peer Coder
"""

# pylint: disable=missing-function-docstring

from enum import IntFlag, auto, STRICT

from flask import Blueprint, request, jsonify, abort, Response

from kaye import PROGRAM_NAME

# from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus

# Blueprints  ##################################################################
PRE_SENSE_PROMPT_BLUEPRINT = """ ○
[x] └── Role
[x]     └── Kaye Peer Coder
[x]         └── pre-sense
"""


CHAT_PROMPT_BASIC_BLUEPRINT = """ ○
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


# constants  ###################################################################
OUTPUT_PROMPT_KEY = "prompt"
OUTPUT_FLAGS_KEY = "flags"


# helpers  #####################################################################
class PL(IntFlag, boundary=STRICT):
    """
    represent a single programming language
    """

    NONE = 0

    # pylint: disable=invalid-name

    # abbreviations defined in prompt corpus
    c = auto()
    cpp = auto()
    ue = auto()
    csharp = auto()
    u3d = auto()
    gdscript = auto()
    html = auto()
    css = auto()
    js = auto()
    ts = auto()
    qt = auto()
    qml = auto()
    py = auto()
    console = auto()


def _create_flags_from_flags_arg(flags_arg):
    if not flags_arg:
        # empty or not provided
        return PL.NONE

    try:
        flags_value = int(flags_arg)
        if flags_value < 0:
            raise ValueError()

        return PL(flags_value)

    except ValueError:
        abort(Response("bad param: ?flags={}".format(flags_arg), 422))


def _parse_flags_from_languages_arg(languages_arg):
    flags = PL.NONE

    if not languages_arg:  # empty or not present
        return flags

    try:
        for lang in languages_arg.split(","):
            if lang:  # skip empty entry
                flags |= PL[lang]

    except KeyError:  # encounter unsupported languages
        pass

    return flags


def _generate_task_prompt_based_on_flags(flags):
    corpus = load_embedded_prompt_corpus()
    bp = PromptBlueprint.parse(
        corpus,
        CHAT_PROMPT_BASIC_BLUEPRINT,
    )

    # add language prompt fragments  -------------------------------------------
    # Bug use DynamicAbbrBlueprint for PL abbr

    # pylint: disable-next=unsubscriptable-object
    kyc_node = corpus["Role"]["Kaye Peer Coder"]

    if PL.c in flags:
        bp += kyc_node["C"]
    if PL.cpp in flags:
        bp += kyc_node["C++"]
    if PL.ue in flags:
        bp += kyc_node["Unreal Engine"]
    if PL.csharp in flags:
        bp += kyc_node["C Sharp"]
    if PL.u3d in flags:
        bp += kyc_node["Unity Engine"]
    if PL.gdscript in flags:
        bp += kyc_node["GDScript"]
    if PL.html in flags:
        bp += kyc_node["HTML"]
    if PL.ts in flags or PL.js in flags:
        bp += kyc_node["JavaScript & TypeScript"]
    if PL.qt in flags:
        bp += kyc_node["Qt"]
    if PL.qml in flags:
        bp += kyc_node["Qt"]["QML"]
    if PL.py in flags:
        py_node = kyc_node["Python"]
        bp += py_node
    if PL.console in flags:
        bp += kyc_node["Message Level"]

    return bp.generate_prompt()


# Flask Routing  ###############################################################
# /kaye/dify-app/kyc
kyc_bp = Blueprint("kaye-peer-coder", PROGRAM_NAME, url_prefix="/kyc")


# /kaye/dify-app/kyc/pre-sense
@kyc_bp.route("/pre-sense", methods=["GET"])
def kaye_peer_coder_pre_sense():
    # Todo utilize dynamic abbr
    blueprint = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        PRE_SENSE_PROMPT_BLUEPRINT,
    )
    return blueprint.generate_prompt()


# /kaye/dify-app/kyc/chat
@kyc_bp.route("/chat", methods=["GET"])
def kaye_peer_coder_task():
    flags = _create_flags_from_flags_arg(request.args.get("flags"))
    # merge language flags from languages list & provided flag number
    flags |= _parse_flags_from_languages_arg(request.args.get("languages"))

    prompt = _generate_task_prompt_based_on_flags(flags)

    opt = {OUTPUT_PROMPT_KEY: prompt, OUTPUT_FLAGS_KEY: int(flags)}
    return jsonify(opt)

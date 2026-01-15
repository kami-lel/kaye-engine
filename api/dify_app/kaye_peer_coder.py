"""
define API to specific work with Dify App: Kaye Peer Coder
"""

# pylint: disable=missing-function-docstring

from enum import IntFlag, auto, STRICT

from flask import Blueprint, request, jsonify, abort, Response

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
[x]     └── Kaye Peer Coder
[x]         └── task
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

    except KeyError:
        # FIXME, instead of abort, log it
        abort(
            Response(
                "bad param, contains unsupported language: "
                "?languages={}".format(languages_arg),
                422,
            )
        )

    return flags


def _generate_task_prompt_based_on_flags(flags):
    corpus = load_embedded_prompt_corpus()
    blueprint = PromptBlueprint.parse(
        corpus,
        TASK_PROMPT_BASIC_BLUEPRINT,
    )

    # add language prompt fragments  -------------------------------------------
    # TODO code dynamically add language fragment

    return str(blueprint)


# Flask Routing  ###############################################################
# /kaye/dify-app/kaye-peer-coder
kyc_bp = Blueprint(
    "kaye-peer-coder", PROGRAM_NAME, url_prefix="/kaye-peer-coder"
)


# /kaye/dify-app/kaye-peer-coder/pre-sense
@kyc_bp.route("/pre-sense", methods=["GET"])
def kaye_peer_coder_pre_sense():
    blueprint = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        PRE_SENSE_PROMPT_BLUEPRINT,
    )
    return str(blueprint)


# /kaye/dify-app/kaye-peer-coder/task
@kyc_bp.route("/task", methods=["GET"])
def kaye_peer_coder_task():
    flags = _create_flags_from_flags_arg(request.args.get("flags"))
    # merge language flags from languages list & provided flag number
    flags |= _parse_flags_from_languages_arg(request.args.get("languages"))

    prompt = _generate_task_prompt_based_on_flags(flags)

    opt = {OUTPUT_PROMPT_KEY: prompt, OUTPUT_FLAGS_KEY: int(flags)}
    return jsonify(opt)

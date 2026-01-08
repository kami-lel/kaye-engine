"""
define API to specific work with Dify App: Kaye Peer Coder
"""

# pylint: disable=missing-function-docstring

from enum import IntFlag, auto

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


# constants  ###################################################################
OUTPUT_PROMPT_KEY = "prompt"
OUTPUT_FLAGS_KEY = "flags"


# helpers  #####################################################################
class PL(IntFlag):
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
    console = auto()
    css = auto()
    html = auto()
    js = auto()
    ts = auto()
    py = auto()


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
    languages = request.args.get("languages")
    flags_arg = request.args.get("flags")

    flags = PL(flags_arg)

    try:
        if languages:  # when languages list is not empty
            for lang in languages.split(","):
                flags |= PL[lang]

    except ValueError as err:
        raise ValueError(
            "contains unsupported language: {}".format(languages)
        ) from err

    # BUG need test
    prompt = ""
    flags = 5

    opt = {OUTPUT_PROMPT_KEY: prompt, OUTPUT_FLAGS_KEY: int(flags)}
    return jsonify(opt)

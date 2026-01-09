"""
define API to specific work with Dify App: Kaye Peer Coder
"""

# pylint: disable=missing-function-docstring

from enum import IntFlag, auto

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


# helpers for /task endpoint  ==================================================
def _calc_flags_from_languages(languages_arg):
    """
    :param languages_arg: ',' separated programming language list
    :type languages_arg: str or NoneType
    :return: parsed languages flags
    :rtype: PL
    :raises: ValueError: languages_arg contains unsupported language
    """
    flags = PL.NONE

    if languages_arg:  # when languages list is not empty
        for lang in languages_arg.split(","):
            if lang:  # skip empty entry
                flags |= PL[lang]

    return flags


def _generate_task_prompt(flags):
    """
    :param flags:
    :type flags: PL
    :return: task prompt constructed based on language flags
    :rtype: str
    """
    # TODO
    return ""


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
    languages_arg = request.args.get("languages")
    flags_arg = request.args.get("flags")

    # create flags from provided args
    if flags_arg:
        try:
            flags_value = int(flags_arg)
            # TODO
            # if flags_value < 0:
            #     raise ValueError()
            flags = PL(flags_value)

        except ValueError:
            abort(Response("bad bad: {}".format(flags_arg), 422))  # TODO

        # TODO non value error

    else:
        flags = PL.NONE

    opt = {OUTPUT_PROMPT_KEY: "", OUTPUT_FLAGS_KEY: int(flags)}  # HACK
    return jsonify(opt)

    # merge language flags from languages list & provided flag number
    flags |= _calc_flags_from_languages(languages_arg)  # BUG err handling

    prompt = _generate_task_prompt(flags)

    opt = {OUTPUT_PROMPT_KEY: prompt, OUTPUT_FLAGS_KEY: int(flags)}
    return jsonify(opt)

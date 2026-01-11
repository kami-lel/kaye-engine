"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME
from kaye.gen_prompt import PromptBlueprint, load_embedded_prompt_corpus

# Blueprints  ##################################################################
PRE_SENSE_PROMPT_BLUEPRINT = """ ○
[x] └── Role
[x]     └── Kaye Chat
[x]         └── pre-sense
"""


# Flask Routing  ###############################################################
# /kaye/dify-app/kaye-peer-coder
ky_bp = Blueprint("kaye-chat", PROGRAM_NAME, url_prefix="/ky")


# /kaye/dify-app/kaye-peer-coder/pre-sense
@ky_bp.route("/pre-sense", methods=["GET"])
def kaye_chat_pre_sense():
    blueprint = PromptBlueprint(
        load_embedded_prompt_corpus(),
        PRE_SENSE_PROMPT_BLUEPRINT,
    )
    return str(blueprint)

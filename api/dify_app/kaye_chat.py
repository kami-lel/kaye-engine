"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME
from kaye.prompt import (
    PromptBlueprint,
    load_embedded_prompt_blueprint,
)

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
    blueprint = PromptBlueprint.parse(
        load_embedded_prompt_corpus(), PRE_SENSE_PROMPT_BLUEPRINT
    )
    return blueprint.generate_prompt()


# /kaye/dify-app/kaye-peer-coder/chat
@ky_bp.route("/chat", methods=["GET"])
def kaye_chat_chat():
    blueprint = load_embedded_prompt_blueprint("chat")

    return blueprint.generate_prompt()

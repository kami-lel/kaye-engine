"""
opus_tag_smith.py

define API to specific work with Dify App: Opus Tag Smith
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint

# Blueprints  ##################################################################
EXTRACT_PROMPT_BLUEPRINT = """    ○
[x] └── Opus Tag Smith
"""


# Flask Routing  ###############################################################

# /kaye/dify-app/opus-tag-smith
renamer_bp = Blueprint(
    "opus-tag-smith", PROGRAM_NAME, url_prefix="/opus-tag-smith"
)


# /kaye/dify-app/opus-tag-smith/opus
@renamer_bp.route("/opus", methods=["GET"])
def opus_tag_smith_opus():
    blueprint = PromptBlueprint.parse(
        EXTRACT_PROMPT_BLUEPRINT,
    )
    return blueprint.generate_prompt()

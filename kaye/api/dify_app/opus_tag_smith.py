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


# /kaye/dify-app/opus-tag-smith/extract
@renamer_bp.route("/extract", methods=["GET"])
def kaye_event_radar_filter():
    blueprint = PromptBlueprint.parse(
        EXTRACT_PROMPT_BLUEPRINT,
    )
    return blueprint.generate_prompt()

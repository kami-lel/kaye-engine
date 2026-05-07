"""
opus_tag_smith.py

define API to specific work with Dify App: Opus Tag Smith
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint

# Blueprints  ##################################################################
OPUS_PROMPT_BLUEPRINT = """    ○
[x] └── Opus Tag Smith
[x]     └── tags
[x]         └── tags for Opus
"""


SHELVER_PROMPT_BLUEPRINT = """    ○
[x] └── Opus Tag Smith
[x]     ├── extract for Shelver
[x]     └── tags
[x]         └── tags for Shelver
"""


# Flask Routing  ###############################################################

# /kaye/dify-app/opus-tag-smith
tag_smith_bp = Blueprint(
    "opus-tag-smith", PROGRAM_NAME, url_prefix="/opus-tag-smith"
)


# /kaye/dify-app/opus-tag-smith/opus
@tag_smith_bp.route("/opus", methods=["GET"])
def opus_tag_smith_opus():
    blueprint = PromptBlueprint.parse(
        OPUS_PROMPT_BLUEPRINT,
    )
    return blueprint.generate_prompt()


# /kaye/dify-app/opus-tag-smith/shelver
@tag_smith_bp.route("/shelver", methods=["GET"])
def opus_tag_smith_shelver():
    blueprint = PromptBlueprint.parse(SHELVER_PROMPT_BLUEPRINT)
    return blueprint.generate_prompt()

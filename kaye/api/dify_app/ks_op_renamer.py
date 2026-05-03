"""
ks_op_renamer.py

define API to specific work with Dify App: ks-op-renamer
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint

# Blueprints  ##################################################################
EXTRACT_PROMPT_BLUEPRINT = """"""  # TODO

# Flask Routing  ###############################################################

# /kaye/dify-app/ks-op-renamer
renamer_bp = Blueprint(
    "ks-op-renamer", PROGRAM_NAME, url_prefix="/ks-op-renamer"
)


# /kaye/dify-app/ks-op-renamer/extract
@renamer_bp.route("/extract", methods=["GET"])
def kaye_event_radar_filter():
    blueprint = PromptBlueprint.parse(
        EXTRACT_PROMPT_BLUEPRINT,
    )
    return blueprint.generate_prompt()

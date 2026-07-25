"""
kaye_cash_tracker.py

define API to specific work with Dify App: Kaye Cash Tracker
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye_engine import PROGRAM_NAME
from kaye_engine.prompt import PromptBlueprint

# Blueprints  ##################################################################
EXTRACT_PROMPT_BLUEPRINT = """    ○
[ ] ├── Kaye Cash Tracker
[x] │    └── Extract
[x] └── (Today)
"""


# Flask Routing  ###############################################################
# /kaye/dify-app/kaye-cash-tracker
cash_tracker_bp = Blueprint(
    "kaye-cash-tracker", PROGRAM_NAME, url_prefix="/kaye-cash-tracker"
)


# /kaye/dify-app/kaye-cash-tracker/extract
@cash_tracker_bp.route("/extract", methods=["GET"])
def kaye_cash_tracker_extract():
    blueprint = PromptBlueprint.parse(EXTRACT_PROMPT_BLUEPRINT)
    return blueprint.generate_prompt()

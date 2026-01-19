"""
define API to specific work with Dify App: Kaye_Cash_Tracker
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME

# Blueprints  ##################################################################
PROMPT_BLUEPRINT = """○
[ ] └── Role
[ ]     └── Kaye Cash Tracker
[x]         └── Extract Info
"""


# Flask Routing  ###############################################################
# /kaye/dify-app/kaye-cash-tracker
cash_tracker_bp = Blueprint(
    "kaye-cash-tracker", PROGRAM_NAME, url_prefix="/kaye-cash-tracker"
)


# /kaye/dify-app/kaye-cash-tracker/extract
@cash_tracker_bp.route("/track", methods=["GET"])
def kaye_cash_tracker_extract():
    return ""  # TODO

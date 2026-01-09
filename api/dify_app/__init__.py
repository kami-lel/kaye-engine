"""
define API to specific work with Dify Apps,
such that they can use Http Request Node to dynamically get newest prompt
"""

from flask import Blueprint

from kaye import PROGRAM_NAME

from api.dify_app.kaye_cash_tracker import call_kaye_cash_tracker
from api.dify_app.kaye_commit_sense import commit_sense_bp
from api.dify_app.kaye_event_radar import event_radar_bp
from api.dify_app.kaye_peer_coder import kyc_bp

# /kaye/dify-app
dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/dify-app")


# Kaye Cash Tracker  ###########################################################


# /kaye/dify-app/kaye-cash-tracker
@dify_bp.route("/kaye-cash-tracker", methods=["GET"])
def kaye_cash_tracker():  # pylint: disable=missing-function-docstring
    return call_kaye_cash_tracker()


# register per app bps  ########################################################

dify_bp.register_blueprint(commit_sense_bp)
dify_bp.register_blueprint(event_radar_bp)
dify_bp.register_blueprint(kyc_bp)

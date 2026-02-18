"""
define API to specific work with Dify Apps,
such that they can use Http Request Node to dynamically get newest prompt
"""

from flask import Blueprint

from kaye import PROGRAM_NAME

from kaye.api.dify_app.kaye_chat import ky_bp
from kaye.api.dify_app.kaye_commit_sense import commit_sense_bp
from kaye.api.dify_app.kaye_event_radar import event_radar_bp
from kaye.api.dify_app.kaye_peer_coder import kyc_bp
from kaye.api.dify_app.kaye_cash_tracker import cash_tracker_bp

# /kaye/dify-app
dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/dify-app")


# Kaye Cash Tracker  ###########################################################


# register per app bps  ########################################################

dify_bp.register_blueprint(commit_sense_bp)
dify_bp.register_blueprint(ky_bp)
dify_bp.register_blueprint(event_radar_bp)
dify_bp.register_blueprint(kyc_bp)
dify_bp.register_blueprint(cash_tracker_bp)

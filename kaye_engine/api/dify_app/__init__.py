"""
Kaye HTTP API: Dify App Support, endpoints /kaye/dify-app/*

specific work with Dify Apps,
such that they can use Http Request Node to dynamically get newest prompt
"""

from flask import Blueprint

from kaye_engine import PROGRAM_NAME

from kaye_engine.api.dify_app.kaye_chat import ky_bp
from kaye_engine.api.dify_app.kaye_commit_sense import commit_sense_bp
from kaye_engine.api.dify_app.kaye_event_radar import event_radar_bp
from kaye_engine.api.dify_app.kaye_cash_tracker import cash_tracker_bp
from kaye_engine.api.dify_app.opus_tag_smith import tag_smith_bp

# /kaye/dify-app
dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/dify-app")


# Kaye Cash Tracker  ###########################################################


# register per app bps  ########################################################

dify_bp.register_blueprint(commit_sense_bp)
dify_bp.register_blueprint(ky_bp)
dify_bp.register_blueprint(event_radar_bp)
dify_bp.register_blueprint(cash_tracker_bp)
dify_bp.register_blueprint(tag_smith_bp)

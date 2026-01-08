"""
define API to specific work with Dify Apps,
such that they can use Http Request Node to dynamically get newest prompt
"""

from flask import Blueprint

from kaye import PROGRAM_NAME

from kaye.api.dify_app.kaye_cash_tracker import call_kaye_cash_tracker
from kaye.api.dify_app.kaye_commit_sense import commit_sense_bp

# /kaye/dify-app
dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/dify-app")


# Kaye Cash Tracker  ###########################################################


# /kaye/dify-app/kaye-cash-tracker
@dify_bp.route("/kaye-cash-tracker", methods=["GET"])
def kaye_cash_tracker():  # pylint: disable=missing-function-docstring
    return call_kaye_cash_tracker()


# Kaye Event Radar  ############################################################

# /kaye/dify-app/kaye-event-radar
event_radar_bp = Blueprint(
    "kaye-event-radar", PROGRAM_NAME, url_prefix="/kaye-event-radar"
)


# /kaye/dify-app/kaye-event-radar/filter-events
@event_radar_bp.route("/filter-events", methods=["GET"])
def kaye_event_radar_filter():
    return "not implemented yet"  # Todo


# /kaye/dify-app/kaye-event-radar/parse-events
@event_radar_bp.route("/parse-events", methods=["GET"])
def kaye_event_radar_parse():
    return "not implemented yet"  # Todo


# Kaye Peer Coder  #############################################################

# /kaye/dify-app/kaye-peer-coder
kyc_bp = Blueprint(
    "kaye-peer-coder", PROGRAM_NAME, url_prefix="/kaye-peer-coder"
)


# /kaye/dify-app/kaye-peer-coder/pre-sense
@kyc_bp.route("/pre-sense", methods=["GET"])
def kaye_peer_coder_pre_sense():
    return "not implemented yet"  # Todo


# /kaye/dify-app/kaye-peer-coder/task
@kyc_bp.route("/task", methods=["GET"])
def kaye_peer_coder_task():
    return "not implemented yet"  # Todo


# register per app bps  ########################################################

dify_bp.register_blueprint(kyc_bp)
dify_bp.register_blueprint(event_radar_bp)
dify_bp.register_blueprint(commit_sense_bp)

# pylint: disable=missing-function-docstring

from pathlib import Path

from flask import Blueprint

from kaye import PROGRAM_NAME

from kaye.api.dify_app.kaye_cash_tracker import call_kaye_cash_tracker

DIR = Path(__file__).parent

# /kaye/dify-app
dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/dify-app")


# Kaye Cash Tracker  ###########################################################


# /kaye/dify-app/kaye-cash-tracker
@dify_bp.route("/kaye-cash-tracker", methods=["GET"])
def kaye_cash_tracker():
    return call_kaye_cash_tracker()


# Kaye Commit Sense  ###########################################################

# /kaye/dify-app/kaye-commit-sense
commit_sense_bp = Blueprint(
    "kaye-commit-sense", PROGRAM_NAME, url_prefix="/kaye-commit-sense"
)


# /kaye/dify-app/kaye-commit-sense/primary-message
@commit_sense_bp.route("/primary-message", methods=["GET"])
def kaye_commit_sense_primary_message():
    return "not implemented yet"  # Todo


# /kaye/dify-app/kaye-commit-sense/per-file-extract
@commit_sense_bp.route("/per-file-extract", methods=["GET"])
def kaye_commit_sense_per_file_extract():
    return "not implemented yet"  # Todo


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

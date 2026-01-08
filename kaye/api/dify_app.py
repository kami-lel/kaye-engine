from flask import Blueprint

from kaye import PROGRAM_NAME

# /kaye/dify-app/kaye-peer-coder
kyc_bp = Blueprint(
    "kaye-peer-coder", PROGRAM_NAME, url_prefix="/kaye-peer-coder"
)


@kyc_bp.route("/pre-sense", methods=["GET"])
def kaye_peer_coder_pre_sense():  # todo
    return "PRE SENSE"  # TODO


@kyc_bp.route("/task", methods=["GET"])
def kaye_peer_coder_task():  # todo
    return "TASK"  # TODO


# /kaye/dify-app
dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/dify-app")
dify_bp.register_blueprint(kyc_bp)

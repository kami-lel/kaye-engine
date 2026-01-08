from flask import Blueprint

from kaye import PROGRAM_NAME

dify_bp = Blueprint("dify-app", PROGRAM_NAME, url_prefix="/kaye/dify-app")


@dify_bp.route("/kaye-peer-coder/pre-sense", methods=["GET"])
def kaye_peer_coder_pre_sense():  # todo
    return "PRE SENSE"  # TODO


@dify_bp.route("/kaye-peer-coder/task", methods=["GET"])
def kaye_peer_coder_task():  # todo
    return "TASK"  # TODO

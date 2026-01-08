"""
define API to specific work with Dify App: Kaye Peer Coder
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME

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

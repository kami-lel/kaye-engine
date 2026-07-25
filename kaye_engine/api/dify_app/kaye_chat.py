"""
kaye_chat.py

define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring


from flask import Blueprint


from kaye_engine import PROGRAM_NAME
from kaye_engine.api.dify_app.kaye_chat_sense import kaye_chat_sense
from kaye_engine.api.dify_app.kaye_chat_task import kaye_chat_task
from kaye_engine.api.dify_app.kaye_chat_merge import kaye_chat_merge

# Flask Routing  ###############################################################
# /kaye/dify-app/ky
ky_bp = Blueprint("kaye-chat", PROGRAM_NAME, url_prefix="/ky")


# /kaye/dify-app/ky/sense
@ky_bp.route("/sense", methods=["POST"])
def kaye_chat_sense_endpoint():
    return kaye_chat_sense()


# /kaye/dify-app/ky/task
@ky_bp.route("/task", methods=["POST"])
def kaye_chat_task_endpoint():
    return kaye_chat_task()


# /kaye/dify-app/ky/merge
@ky_bp.route("/merge", methods=["GET"])
def kaye_chat_merge_endpoint():
    return kaye_chat_merge()

"""
define API to work with prompts
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, Response

from kaye import PROGRAM_NAME

# /kaye/prompt
prompt_bp = Blueprint("prompt", PROGRAM_NAME, url_prefix="/prompt")

# todo prompt API endpoints


@prompt_bp.route("/generate", methods=["GET"])
def prompt_generate():
    return Response("not implemented", status=501, mimetype="text/plain")


@prompt_bp.route("/show", methods=["GET"])
def prompt_show():
    return Response("not implemented", status=501, mimetype="text/plain")


@prompt_bp.route("/list", methods=["GET"])
def prompt_list():
    return Response("not implemented", status=501, mimetype="text/plain")

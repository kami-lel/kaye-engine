from flask import Blueprint, Response

from kaye import PROGRAM_NAME

prompt_bp = Blueprint("prompt", PROGRAM_NAME, url_prefix="/kaye/prompt")


@prompt_bp.route("/generate", methods=["GET"])
def prompt_generate():  # todo
    return Response("not implemented", status=501, mimetype="text/plain")


@prompt_bp.route("/show", methods=["GET"])
def prompt_show():  # todo
    return Response("not implemented", status=501, mimetype="text/plain")


@prompt_bp.route("/list", methods=["GET"])
def prompt_list():  # todo
    return Response("not implemented", status=501, mimetype="text/plain")

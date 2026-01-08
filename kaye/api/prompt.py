from requests import Response

from flask import Blueprint

from kaye import PROGRAM_NAME

prompt_bp = Blueprint("prompt", PROGRAM_NAME, url_prefix="/kaye/prompt")


@prompt_bp.route("/kaye/prompt/generate", methods=["GET"])
def prompt_generate():  # todo
    return Response("not implemented", status=501, mimetype="text/plain")


@prompt_bp.route("/kaye/prompt/generate", methods=["GET"])
def prompt_generate():  # todo
    return Response("not implemented", status=501, mimetype="text/plain")

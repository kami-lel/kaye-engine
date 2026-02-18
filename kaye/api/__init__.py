"""
define Kaye Flask HTTP API
"""

from flask import Flask, Blueprint

from kaye import PROGRAM_NAME

from kaye.api.prompt import prompt_bp
from kaye.api.dify_app import dify_bp


# flask app  ###################################################################
def create_app():
    """
    create a Flask App for: Kaye HTTP API
    """
    app_bp = Blueprint("kaye", PROGRAM_NAME, url_prefix="/kaye")
    app_bp.register_blueprint(prompt_bp)
    app_bp.register_blueprint(dify_bp)

    current_app = Flask(PROGRAM_NAME)
    current_app.register_blueprint(app_bp)

    return current_app

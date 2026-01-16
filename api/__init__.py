"""
define Kaye Flask HTTP API
"""

from flask import Flask, Blueprint

from kaye import PROGRAM_NAME
from api.prompt import prompt_bp
from api.dify_app import dify_bp

# constants  ###################################################################
HOST = "0.0.0.0"
PORT = 11255


def create_app():
    app_bp = Blueprint("kaye", PROGRAM_NAME, url_prefix="/kaye")
    app_bp.register_blueprint(prompt_bp)
    app_bp.register_blueprint(dify_bp)

    app = Flask(PROGRAM_NAME)
    app.register_blueprint(app_bp)
    app.run(host=HOST, port=PORT, debug=False)

    return app


if __name__ == "__main__":
    create_app()

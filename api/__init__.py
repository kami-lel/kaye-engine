"""
define Kaye Flask HTTP API
"""

# TODO think about move api folder to top level
# bug maybe write unit tests?

from flask import Flask, Blueprint

from kaye import PROGRAM_NAME
from kaye.api.prompt import prompt_bp
from kaye.api.dify_app import dify_bp

# constants  ###################################################################
HOST = "0.0.0.0"
PORT = 11255


if __name__ == "__main__":
    app_bp = Blueprint("kaye", PROGRAM_NAME, url_prefix="/kaye")
    app_bp.register_blueprint(prompt_bp)
    app_bp.register_blueprint(dify_bp)

    app = Flask(PROGRAM_NAME)
    app.register_blueprint(app_bp)
    app.run(host=HOST, port=PORT, debug=True)  # HACK turn off debug

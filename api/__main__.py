"""
define Kaye Flask HTTP API
"""

import argparse


from flask import Flask, Blueprint

from kaye import PROGRAM_NAME
from api.prompt import prompt_bp
from api.dify_app import dify_bp

# constants  ###################################################################
HOST = "0.0.0.0"
PORT = 11255
DEBUG_PORT = 11256


# argparse  ####################################################################
parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
parser.add_argument(
    "-x",
    "--debug",
    action="store_true",
    help="enable debug, port changed to {}".format(DEBUG_PORT),
)


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


# Entry Point  #################################################################
if __name__ == "__main__":
    args = parser.parse_args()

    app = create_app()
    app.run(
        host=HOST, port=DEBUG_PORT if args.debug else PORT, debug=args.debug
    )

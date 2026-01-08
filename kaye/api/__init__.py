from flask import Flask

from kaye import PROGRAM_NAME
from kaye.api.prompt import prompt_bp

# constants  ###################################################################
HOST = "127.0.0.1"
PORT = 5000


if __name__ == "__main__":
    app = Flask(PROGRAM_NAME)
    app.register_blueprint(prompt_bp)
    app.run(host=HOST, port=PORT)

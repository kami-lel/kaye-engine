from flask import Flask
from kaye import PROGRAM_NAME


def create_app():
    app = Flask(PROGRAM_NAME)

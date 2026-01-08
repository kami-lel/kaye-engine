"""
define API to specific work with Dify App: Kaye Commit Sense
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint

from kaye import PROGRAM_NAME

# Kaye Commit Sense  ###########################################################

# /kaye/dify-app/kaye-commit-sense
commit_sense_bp = Blueprint(
    "kaye-commit-sense", PROGRAM_NAME, url_prefix="/kaye-commit-sense"
)


# /kaye/dify-app/kaye-commit-sense/primary-message
@commit_sense_bp.route("/primary-message", methods=["GET"])
def kaye_commit_sense_primary_message():
    return "not implemented yet"  # TODO


# /kaye/dify-app/kaye-commit-sense/per-file-extract
@commit_sense_bp.route("/per-file-extract", methods=["GET"])
def kaye_commit_sense_per_file_extract():
    return "not implemented yet"  # TODO

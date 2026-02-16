"""
define API to specific work with Dify App: Kaye Chat
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, request


from kaye import PROGRAM_NAME
from kaye.prompt import PromptBlueprint

# Blueprints  ##################################################################
PRE_SENSE_PROMPT_BLUEPRINT = """ ○
[x] └── Role
[x]     └── Kaye Chat
[x]         └── pre-sense
"""


TASK_PROMPT_BLUEPRINT = """    ○
[x] ├── Introduction
[x] ├── Personality
[x] ├── Language
[x] ├── Elements
[x] │   └── Date & Time Format
[ ] ├── Style
[x] │   └── Capitalization Style
[x] │       ├── Title Case
[x] │       └── Commentary Case
[x] ├── Format
[x] ├── Standards
[x] │   ├── Numerical Values with Units:
[x] │   ├── Language code
[x] │   └── International Phonetic Alphabet
[x] └── Role"""


# Flask Routing  ###############################################################
# /kaye/dify-app/ky
ky_bp = Blueprint("kaye-chat", PROGRAM_NAME, url_prefix="/ky")


# /kaye/dify-app/ky/pre-sense
@ky_bp.route("/pre-sense", methods=["GET"])
def kaye_chat_pre_sense():
    # TODO
    role = request.args.get("role")

    blueprint = PromptBlueprint.parse(PRE_SENSE_PROMPT_BLUEPRINT)
    return blueprint.generate_prompt()


# /kaye/dify-app/ky/task
@ky_bp.route("/task", methods=["GET"])
def kaye_chat_task():
    blueprint = PromptBlueprint.parse(TASK_PROMPT_BLUEPRINT)

    return blueprint.generate_prompt()

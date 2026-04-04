"""
dify-ky-post_start_test.py

Unit Tests (using pytest) for:

post_start node of Kaye Chat Dify App
"""

import json


from dify_studio.kaye_chat.nodes import post_start
from dify_studio.kaye_chat.nodes.post_start import (
    OUTPUT_ROLE_KEY,
    OUTPUT_SKIP_KEY,
    OUTPUT_SENSE_BODY_KEY,
    BODY_ROLE_KEY,
    BODY_DIFF_KEY,
)

# constants  ###################################################################

DEFAULT_ROLE_OVERRIDE = ""
DEFAULT_DIFFICULTY_OVERRIDE = 0
DEFAULT_CURRENT_ROLE = ""


# Pytest unit tests  ###########################################################


class TestCombined:

    def test1(_):
        role_answer = ""

        # BUG BUG
        role_override = DEFAULT_ROLE_OVERRIDE
        difficulty_override = DEFAULT_DIFFICULTY_OVERRIDE
        current_role = DEFAULT_CURRENT_ROLE

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.load(opt[OUTPUT_SENSE_BODY_KEY]) == {}
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == ""


class TestCurrent:

    def test1(_):
        pass

"""
dify-ky-post_start_test.py

Unit Tests (using pytest) for:

``post_start`` node of Kaye Chat Dify App
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

# TODO check structure & type


class TestDft:  # ==============================================================

    def test_all_dft(_):
        role_answer = ""

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
        assert not opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0

    def test_dft_role(_):
        role_answer = ""

        role_override = DEFAULT_ROLE_OVERRIDE
        difficulty_override = 0.5
        current_role = DEFAULT_CURRENT_ROLE

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert not opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0.5


class TestStatic:  # ==============================================================

    def test_provided(_):
        role_override = "barista"
        difficulty_override = 0.5
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0.5

    def test2(_):
        role_override = "deutschlehrer"
        difficulty_override = 0.5
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0.5

    def test3(_):
        role_override = "tarot"
        difficulty_override = 0.5
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0.5

    def test_dft(_):
        role_override = "barista"
        difficulty_override = 0
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0


class TestCoder:  # ============================================================

    def test_provided(_):
        role_override = "coder"
        difficulty_override = 0.5
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0.5

    def test_dft(_):
        role_override = "coder"
        difficulty_override = 0
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert not opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0


class TestOthers:  # ===========================================================

    def test_provided(_):
        role_override = "art"
        difficulty_override = 0.5
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0.5

    def test_dft(_):
        role_override = "art"
        difficulty_override = 0
        current_role = DEFAULT_CURRENT_ROLE

        role_answer = role_override

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == role_answer
        assert not opt[OUTPUT_SKIP_KEY]

        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)
        assert body[BODY_ROLE_KEY] == role_answer
        assert body[BODY_DIFF_KEY] == 0


class TestCurrent:  # ==========================================================

    def test1(_):
        role_override = DEFAULT_ROLE_OVERRIDE
        difficulty_override = DEFAULT_DIFFICULTY_OVERRIDE
        current_role = "art"

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == "art"
        assert not opt[OUTPUT_SKIP_KEY]

    def test_override(_):
        role_override = "secretary"
        difficulty_override = DEFAULT_DIFFICULTY_OVERRIDE
        current_role = "art"

        opt = post_start.main(
            role_override=role_override,
            difficulty_override=difficulty_override,
            current_role=current_role,
        )

        print(opt)

        assert opt[OUTPUT_ROLE_KEY] == "secretary"
        assert not opt[OUTPUT_SKIP_KEY]

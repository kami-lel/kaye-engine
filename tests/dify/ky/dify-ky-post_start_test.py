"""
dify-ky-post_start_test.py

Unit Tests (using pytest) for:

``post_start`` node of Kaye Chat Dify App
"""

# FIXME FIXME update

import json


import pytest


from dify_studio.kaye_chat.nodes.sense import post_start
from dify_studio.kaye_chat.nodes.sense.post_start import (
    OUTPUT_SKIP_KEY,
    OUTPUT_ROLE_KEY,
    OUTPUT_DIFF_KEY,
    OUTPUT_SENSE_BODY_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_SKIP_KEY in opt
    assert isinstance(opt[OUTPUT_SKIP_KEY], bool)
    assert OUTPUT_ROLE_KEY in opt
    assert isinstance(opt[OUTPUT_SENSE_BODY_KEY], str)
    assert OUTPUT_DIFF_KEY in opt
    assert isinstance(opt[OUTPUT_DIFF_KEY], float)
    assert OUTPUT_SENSE_BODY_KEY in opt
    assert isinstance(opt[OUTPUT_SENSE_BODY_KEY], str)


# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def kwargs():
    return {"role_override": "", "difficulty_override": 0, "current_role": ""}


# opts  ========================================================================
# defaults  --------------------------------------------------------------------
@pytest.fixture(scope="class")
def opt_dft_all(kwargs):
    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_dft_role(kwargs):
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


# static  ----------------------------------------------------------------------
@pytest.fixture(scope="class")
def opt_static_provided(kwargs):
    kwargs["role_override"] = "barista"
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_static_de(kwargs):
    kwargs["role_override"] = "deutschlehrer"
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_static_tarot(kwargs):
    kwargs["role_override"] = "tarot"
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_static_barista(kwargs):
    kwargs["role_override"] = "barista"
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


# coder  -----------------------------------------------------------------------
@pytest.fixture(scope="class")
def opt_coder_provided(kwargs):
    kwargs["role_override"] = "coder"
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_coder_dft(kwargs):
    kwargs["role_override"] = "coder"
    kwargs["difficulty_override"] = 0.0

    return post_start.main(**kwargs)


# others  ----------------------------------------------------------------------
@pytest.fixture(scope="class")
def opt_others_provided(kwargs):
    kwargs["role_override"] = "art"
    kwargs["difficulty_override"] = 0.5

    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_others_default(kwargs):
    kwargs["role_override"] = "art"
    kwargs["difficulty_override"] = 0.0

    return post_start.main(**kwargs)


# current  ---------------------------------------------------------------------
@pytest.fixture(scope="class")
def opt_current_art(kwargs):
    kwargs["current_role"] = "art"

    return post_start.main(**kwargs)


@pytest.fixture(scope="class")
def opt_current_secretary(kwargs):
    kwargs["current_role"] = "secretary"

    return post_start.main(**kwargs)


# Pytest unit tests  ###########################################################


# defaults  ====================================================================
class TestDftAll:  # -----------------------------------------------------------

    def test_structure(_, opt_dft_all):
        opt = opt_dft_all
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_dft_all):
        opt = opt_dft_all
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == ""

    def test_skip(_, opt_dft_all):
        opt = opt_dft_all
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert not skip

    def test_diff(_, opt_dft_all):
        opt = opt_dft_all
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.0

    def test_body(_, opt_dft_all):
        opt = opt_dft_all
        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 0}


class TestDftRole:  # ----------------------------------------------------------
    pass


# static  ======================================================================
class TestStaticProvided:  # ---------------------------------------------------
    pass


class TestStaticDe:  # ---------------------------------------------------------
    pass


class TestStaticTarot:  # ------------------------------------------------------
    pass


class TestStaticBarista:  # ----------------------------------------------------
    pass


# coder  =======================================================================


class TestCoderProvided:  # ----------------------------------------------------
    pass


class TestCoderDft:  # ---------------------------------------------------------
    pass


# others  ======================================================================
class TestOthersProvided:  # ---------------------------------------------------
    pass


class TestOthersDefault:  # ---------------------------------------------------
    pass


# current  =====================================================================
class TestCurrentArt:  # -------------------------------------------------------
    pass


class TestCurrentSecretary:  # -------------------------------------------------
    pass


# TODO TODO


# class TestDft:  # ==============================================================

#     def test_dft_role(_):
#         role_answer = ""

#         role_override = DEFAULT_ROLE_OVERRIDE
#         difficulty_override = 0.5
#         current_role = DEFAULT_CURRENT_ROLE

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert not opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0.5


# class TestStatic:  # ==============================================================

#     def test_provided(_):
#         role_override = "barista"
#         difficulty_override = 0.5
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0.5

#     def test2(_):
#         role_override = "deutschlehrer"
#         difficulty_override = 0.5
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0.5

#     def test3(_):
#         role_override = "tarot"
#         difficulty_override = 0.5
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0.5

#     def test_dft(_):
#         role_override = "barista"
#         difficulty_override = 0
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0


# class TestCoder:  # ============================================================

#     def test_provided(_):
#         role_override = "coder"
#         difficulty_override = 0.5
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0.5

#     def test_dft(_):
#         role_override = "coder"
#         difficulty_override = 0
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert not opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0


# class TestOthers:  # ===========================================================

#     def test_provided(_):
#         role_override = "art"
#         difficulty_override = 0.5
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0.5

#     def test_dft(_):
#         role_override = "art"
#         difficulty_override = 0
#         current_role = DEFAULT_CURRENT_ROLE

#         role_answer = role_override

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == role_answer
#         assert not opt[OUTPUT_SKIP_KEY]

#         body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
#         print(body)
#         assert body[BODY_ROLE_KEY] == role_answer
#         assert body[BODY_DIFF_KEY] == 0


# class TestCurrent:  # ==========================================================

#     def test1(_):
#         role_override = DEFAULT_ROLE_OVERRIDE
#         difficulty_override = DEFAULT_DIFFICULTY_OVERRIDE
#         current_role = "art"

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == "art"
#         assert not opt[OUTPUT_SKIP_KEY]

#     def test_override(_):
#         role_override = "secretary"
#         difficulty_override = DEFAULT_DIFFICULTY_OVERRIDE
#         current_role = "art"

#         opt = post_start.main(
#             role_override=role_override,
#             difficulty_override=difficulty_override,
#             current_role=current_role,
#         )

#         print(opt)

#         _assert_structure(opt)
#         assert opt[OUTPUT_ROLE_KEY] == "secretary"
#         assert not opt[OUTPUT_SKIP_KEY]

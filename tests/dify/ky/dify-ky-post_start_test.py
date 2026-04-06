"""
dify-ky-post_start_test.py

Unit Tests (using pytest) for:

``post_start`` node of Kaye Chat Dify App
"""

# BUG BUG

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
    return {"role_override": "", "difficulty_override": 0.0, "current_role": ""}


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
def opt_static_dft(kwargs):
    kwargs["role_override"] = "barista"

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
def opt_others_dft(kwargs):
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

    def test_structure(_, opt_dft_role):
        opt = opt_dft_role
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_dft_role):
        opt = opt_dft_role
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == ""

    def test_skip(_, opt_dft_role):
        opt = opt_dft_role
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert not skip

    def test_diff(_, opt_dft_role):
        opt = opt_dft_role
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_dft_role):
        opt = opt_dft_role
        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 0.5}


# static  ======================================================================
class TestStaticProvided:  # ---------------------------------------------------

    def test_structure(_, opt_static_provided):
        opt = opt_static_provided
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_static_provided):
        opt = opt_static_provided
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "barista"

    def test_skip(_, opt_static_provided):
        opt = opt_static_provided
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert skip

    def test_diff(_, opt_static_provided):
        opt = opt_static_provided
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_static_provided):
        opt = opt_static_provided
        body = opt[OUTPUT_SENSE_BODY_KEY]
        print(body)
        assert body == ""


class TestStaticDe:  # ---------------------------------------------------------

    def test_structure(_, opt_static_de):
        opt = opt_static_de
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_static_de):
        opt = opt_static_de
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "deutschlehrer"

    def test_skip(_, opt_static_de):
        opt = opt_static_de
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert skip

    def test_diff(_, opt_static_de):
        opt = opt_static_de
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_static_provided):
        opt = opt_static_provided
        body = opt[OUTPUT_SENSE_BODY_KEY]
        print(body)
        assert body == ""


class TestStaticTarot:  # ------------------------------------------------------

    def test_structure(_, opt_static_tarot):
        opt = opt_static_tarot
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_static_tarot):
        opt = opt_static_tarot
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "tarot"

    def test_skip(_, opt_static_tarot):
        opt = opt_static_tarot
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert skip

    def test_diff(_, opt_static_tarot):
        opt = opt_static_tarot
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_static_provided):
        opt = opt_static_provided
        body = opt[OUTPUT_SENSE_BODY_KEY]
        print(body)
        assert body == ""


class TestStaticDft:  # --------------------------------------------------------

    def test_structure(_, opt_static_dft):
        opt = opt_static_dft
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_static_dft):
        opt = opt_static_dft
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "barista"

    def test_skip(_, opt_static_dft):
        opt = opt_static_dft
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert skip

    def test_diff(_, opt_static_dft):
        opt = opt_static_dft
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.0

    def test_body(_, opt_static_provided):
        opt = opt_static_provided
        body = opt[OUTPUT_SENSE_BODY_KEY]
        print(body)
        assert body == ""


# coder  =======================================================================


class TestCoderProvided:  # ----------------------------------------------------

    def test_structure(_, opt_coder_provided):
        opt = opt_coder_provided
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_coder_provided):
        opt = opt_coder_provided
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "coder"

    def test_skip(_, opt_coder_provided):
        opt = opt_coder_provided
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert skip

    def test_diff(_, opt_coder_provided):
        opt = opt_coder_provided
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_static_provided):
        opt = opt_static_provided
        body = opt[OUTPUT_SENSE_BODY_KEY]
        print(body)
        assert body == ""


class TestCoderDft:  # ---------------------------------------------------------

    def test_structure(_, opt_coder_dft):
        opt = opt_coder_dft
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_coder_dft):
        opt = opt_coder_dft
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "coder"

    def test_skip(_, opt_coder_dft):
        opt = opt_coder_dft
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert not skip

    def test_diff(_, opt_coder_dft):
        opt = opt_coder_dft
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.0

    def test_body(_, opt_coder_dft):
        opt = opt_coder_dft
        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 0.0}


# others  ======================================================================
class TestOthersProvided:  # ---------------------------------------------------

    def test_structure(_, opt_others_provided):
        opt = opt_others_provided
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_others_provided):
        opt = opt_others_provided
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "art"

    def test_skip(_, opt_others_provided):
        opt = opt_others_provided
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert skip

    def test_diff(_, opt_others_provided):
        opt = opt_others_provided
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_static_provided):
        opt = opt_static_provided
        body = opt[OUTPUT_SENSE_BODY_KEY]
        print(body)
        assert body == ""


class TestOthersDefault:  # ---------------------------------------------------

    def test_structure(_, opt_others_dft):
        opt = opt_others_dft
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_others_dft):
        opt = opt_others_dft
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "art"

    def test_skip(_, opt_others_dft):
        opt = opt_others_dft
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert not skip

    def test_diff(_, opt_others_dft):
        opt = opt_others_dft
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.0

    def test_body(_, opt_others_dft):
        opt = opt_others_dft
        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "art", "difficulty_override": 0.0}


# current  =====================================================================
class TestCurrentArt:  # -------------------------------------------------------

    def test_structure(_, opt_current_art):
        opt = opt_current_art
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_current_art):
        opt = opt_current_art
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "art"

    def test_skip(_, opt_current_art):
        opt = opt_current_art
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert not skip

    def test_diff(_, opt_current_art):
        opt = opt_current_art
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_current_art):
        opt = opt_current_art
        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "art", "difficulty_override": 0.5}


class TestCurrentSecretary:  # -------------------------------------------------

    def test_structure(_, opt_current_secretary):
        opt = opt_current_secretary
        print(opt)

        _assert_structure(opt)

    def test_role(_, opt_current_secretary):
        opt = opt_current_secretary
        role = opt[OUTPUT_ROLE_KEY]
        print(role)

        assert role == "secretary"

    def test_skip(_, opt_current_secretary):
        opt = opt_current_secretary
        skip = opt[OUTPUT_SKIP_KEY]
        print(skip)

        assert not skip

    def test_diff(_, opt_current_secretary):
        opt = opt_current_secretary
        diff = opt[OUTPUT_DIFF_KEY]
        print(diff)

        assert diff == 0.5

    def test_body(_, opt_current_secretary):
        opt = opt_current_secretary
        body = json.loads(opt[OUTPUT_SENSE_BODY_KEY])
        print(body)

        assert body == {
            "pre_sense_role": "secretary",
            "difficulty_override": 0.5,
        }

"""
api-dify-ky-sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense
"""

import pytest

# helpers  #####################################################################


def _assert_start(opt):
    assert opt.startswith("# Kaye Chat")
    assert "## sense" in opt


def _assert_empty_role(opt):
    assert """### empty role
`role` must be empty string""" in opt


def _assert_empty_pl(opt):
    assert """### empty programming_languages
`programming_languages` must be empty string""" in opt


def _assert_zero_diff(opt):
    assert """### zero difficulty
`difficulty` must be `0`""" in opt


def _assert_role1(opt):
    assert "### sense role" in opt


def _assert_role2(opt):
    assert "select exactly one role" in opt


def _assert_role3(opt):
    assert (
        """- `rapid`: when the user gives you content that needs a **simple mechanical change** with little judgment, such as reformatting, extracting, sorting, converting, cleaning, splitting, merging, or applying a narrow rule to existing text or data
- `chat`: when the user gives you a **general question or everyday request** and no more specific role clearly applies"""
        in opt
    )


def _assert_role4(opt):
    assert (
        """- `secretary`: when the user gives you **person-to-person communication**, or text clearly meant to be sent to someone, such as an email, reply, direct message, follow-up, request, apology, invitation, reminder, complaint, or outreach message
- `art`: when the user gives you **a visual idea for image generation**, such as a scene description, subject concept, style reference, composition idea, aesthetic direction, character design, or AI image prompt draft"""
        in opt
    )


def _assert_sense_diff1(opt):
    assert "### sense difficulty" in opt


def _assert_sense_diff2(opt):
    assert "Provide a number between `0.01` (very easy)" in opt


def _assert_sense_diff3(opt):
    assert (
        """- `0.03` Correct a single typo or awkward word choice in a short piece of text.
- `0.13` Fix basic grammar, punctuation, formatting, or style issues in a short passage.
- `0.25` Look up how to complete a common task and provide brief step-by-step instructions."""
        in opt
    )


def _assert_sense_diff4(opt):
    assert (
        """- `0.75` Choose and apply an appropriate common reasoning framework to organize, filter, or prioritize information.
- `0.88` Design a basic end-to-end workflow connecting user input, intermediate processing, and final output."""
        in opt
    )


# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_coder(flask_test_client, sense_endpoint):
    response = flask_test_client.post(
        sense_endpoint,
        json={"pre_sense_role": "coder", "difficulty_override": 0.0},
    )
    opt = response.get_data().decode("utf-8")

    return opt


@pytest.fixture(scope="class")
def testee_others(flask_test_client, sense_endpoint):
    response = flask_test_client.post(
        sense_endpoint,
        json={"pre_sense_role": "secretary", "difficulty_override": 0.0},
    )
    opt = response.get_data().decode("utf-8")

    return opt


@pytest.fixture(scope="class")
def testee_no_role_provided(flask_test_client, sense_endpoint):
    response = flask_test_client.post(
        sense_endpoint,
        json={"pre_sense_role": "", "difficulty_override": 0.5},
    )
    opt = response.get_data().decode("utf-8")

    return opt


@pytest.fixture(scope="class")
def testee_no_role_dft(flask_test_client, sense_endpoint):
    response = flask_test_client.post(
        sense_endpoint,
        json={"pre_sense_role": "", "difficulty_override": 0.0},
    )
    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestCoder:  # ============================================================

    def test_start(_, testee_coder):
        opt = testee_coder
        print(opt)
        _assert_start(opt)

    def test1(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert "### for coder" in opt

    def test2(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert (
            """#### programming_languages
Return a string containing the abbreviations of the programming languages"""
            in opt
        )

    def test_diff1(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert "#### difficulty" in opt

    def test_diff2(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert """Provide a number between `0.01` (very easy)""" in opt

    def test_diff3(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert """- `0.03` Rename a local variable for clarity; ensure no typos.
- `0.07` Change a single hardcoded configuration value or string.""" in opt

    def test_diff4(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert (
            "Use these tasks as your **anchor point** when evaluate difficulty:"
            in opt
        )

    def test_diff5(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert (
            """- `0.96` Integrate a standard third-party SDK for a straightforward feature; mock in tests.
- `0.98` Convert a sync flow to async/await (or equivalent) without behavior changes."""
            in opt
        )

    def test_empty_role(_, testee_coder):
        opt = testee_coder
        print(opt)

        _assert_empty_role(opt)

    def test_plc(_, testee_coder):
        opt = testee_coder
        print(opt)

        assert "# {Programming Languages Code}" in opt
        assert "-`cpp`:C++" in opt


class TestOthers:  # ===========================================================

    def test_start(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_start(opt)

    def test_diff1(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_sense_diff1(opt)

    def test_diff2(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_sense_diff2(opt)

    def test_diff3(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_sense_diff3(opt)

    def test_diff4(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_sense_diff4(opt)

    def test_empty_role(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_empty_role(opt)

    def test_empty_pl(_, testee_others):
        opt = testee_others
        print(opt)
        _assert_empty_pl(opt)


class TestNoRoleProvided:  # ===================================================

    def test_start(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_start(opt)

    def test_role1(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_role1(opt)

    def test_role2(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_role2(opt)

    def test_role3(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_role3(opt)

    def test_role4(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_role4(opt)

    def test_zero_diff(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_zero_diff(opt)

    def test_empty_pl(_, testee_no_role_provided):
        opt = testee_no_role_provided
        print(opt)
        _assert_empty_pl(opt)


class TestNoRoleDft:  # ========================================================

    def test_start(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_start(opt)

    def test_role1(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_role1(opt)

    def test_role2(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_role2(opt)

    def test_role3(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_role3(opt)

    def test_role4(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_role4(opt)

    def test_diff1(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_sense_diff1(opt)

    def test_diff2(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_sense_diff2(opt)

    def test_diff3(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_sense_diff3(opt)

    def test_diff4(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_sense_diff4(opt)

    def test_empty_pl(_, testee_no_role_dft):
        opt = testee_no_role_dft
        print(opt)
        _assert_empty_pl(opt)


class TestDefault:  # ==========================================================
    pass  # TODO TODO

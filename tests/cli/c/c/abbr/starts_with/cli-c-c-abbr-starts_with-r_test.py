"""
cli-c-c-abbr-starts_with-r_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-r``
"""

import pytest

from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "Abbr Starts with R.md") as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee):
    return split_rule_file_basic_format(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_rule_file_basic_format(testee)[1]


# Pytest unit tests  ###########################################################


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Abbr Starts with R" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_R(_, testee_content):
        assert "- R:are" in testee_content

    def test_rand(_, testee_content):
        assert "- rand:random,randomize" in testee_content

    def test_re(_, testee_content):
        assert "- re:in the matter of,concerning,regarding" in testee_content

    def test_rej(_, testee_content):
        assert "- rej:reject" in testee_content

    def test_req(_, testee_content):
        assert "- req:requirement" in testee_content

    def test_rls(_, testee_content):
        assert "- rls:release" in testee_content

    def test_rm(_, testee_content):
        assert "- rm:remove" in testee_content

    def test_rsch(_, testee_content):
        assert "- rsch:research" in testee_content

    def test_rsp(_, testee_content):
        assert "- rsp:respect,respective,respectively" in testee_content

    def test_rsrc(_, testee_content):
        assert "- rsrc:resource" in testee_content

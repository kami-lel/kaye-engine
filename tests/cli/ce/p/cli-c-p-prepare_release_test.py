"""
cli-c-p-prepare_release_test.py

Unit Tests (using pytest) for:

creation of ``prepare_for_release.md``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_prompts_folder):
    with open(testee_prompts_folder / "prepare_for_release.md") as f:
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
        assert "name: Prepare for Release" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_maintain_agents_heading(_, testee_content):
        assert "### Prepare for Release" in testee_content

    def test1(_, testee_content):
        assert "version number or release date not provided" in testee_content

    def test2(_, testee_content):
        assert " **update `CHANGELOG.md`**:" in testee_content

    def test3(_, testee_content):
        assert "ove all content under *Unreleased* into a new" in testee_content

    def test4(_, testee_content):
        assert (
            "reate a new empty *Unreleased* section above it" in testee_content
        )

    def test5(_, testee_content):
        assert " **update project version**:" in testee_content

    def test6(_, testee_content):
        assert "ind and update the version number in project" in testee_content

    def test7(_, testee_content):
        assert (
            "g `setup.cfg`, `pyproject.toml`, `package.json`, `Cargo.toml`"
            in testee_content
        )

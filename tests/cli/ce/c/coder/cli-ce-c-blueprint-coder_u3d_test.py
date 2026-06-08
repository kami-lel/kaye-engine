"""
cli-ce-c-blueprint-coder_u3d_test.py

Unit Tests (using pytest) for:

creation of ``coder_u3d_blueprint.md``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "coder_u3d_blueprint.md") as f:
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
        assert "name: Coder Unity Engine" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: C# code for Unity 6 (MonoBehaviour scripts,"
            " components, Inspector fields)"
            in testee_header
        )

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.cs"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_brace_style_heading(_, testee_content):
        assert "## Brace Style" in testee_content

    def test_csharp_heading(_, testee_content):
        assert "## Coder C Sharp" in testee_content

    def test_unity_engine_heading(_, testee_content):
        assert "## Coder Unity Engine" in testee_content

    def test_unity_version(_, testee_content):
        assert "Unity **6**" in testee_content

    def test_monobehaviour_heading(_, testee_content):
        assert "### MonoBehaviour" in testee_content

    def test_section_ordering(_, testee_content):
        assert "- **section order is fixed**" in testee_content

    def test_public_members(_, testee_content):
        assert "// Public Members" in testee_content

    def test_inspector_fields(_, testee_content):
        assert "// Inspector Fields" in testee_content

    def test_inspector_guard_heading(_, testee_content):
        assert "#### Inspector Assignment Guard" in testee_content

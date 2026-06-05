"""
cli-c-p-resolve_annotation_markers_test.py

Unit Tests (using pytest) for:

creation of ``resolve_annotation_markers.md``
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
    with open(testee_prompts_folder / "resolve_annotation_markers.md") as f:
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
        assert "name: Resolve Annotation Markers" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_resolve_annotation_markers_heading(_, testee_content):
        assert "### Resolve Annotation Markers" in testee_content

    def test_scan_for_primary_annotation_markers(_, testee_content):
        assert "scan for **primary Annotation Markers**" in testee_content

    def test_bug_marker(_, testee_content):
        assert "`BUG`" in testee_content

    def test_fixme_marker(_, testee_content):
        assert "`FIXME`" in testee_content

    def test_todo_marker(_, testee_content):
        assert "`TODO`" in testee_content

    def test_hack_marker(_, testee_content):
        assert "`HACK`" in testee_content

    def test_understand_task_and_context(_, testee_content):
        assert (
            "understand the required task and surrounding context"
            in testee_content
        )

    def test_implement_fix_or_feature(_, testee_content):
        assert "implement the fix or feature" in testee_content

    def test_remove_marker(_, testee_content):
        assert "then remove the marker" in testee_content

    def test_do_not_touch_secondary_tertiary(_, testee_content):
        assert "Do not touch secondary or tertiary markers" in testee_content

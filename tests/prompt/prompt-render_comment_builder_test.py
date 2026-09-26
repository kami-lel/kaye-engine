"""
prompt-render_comment_builder_test.py

Unit Tests (using pytest) for:

- render_comment_lines()
"""

import re

import pytest
from kaye_engine.prompt.blueprint.render.comment import (
    comment_line_registry,
    register_comment_line,
    render_comment_lines,
)


@pytest.fixture(autouse=True)
def restore_registry():
    snapshot = list(comment_line_registry)
    comment_line_registry.clear()
    yield
    comment_line_registry[:] = snapshot


# Pytest unit tests  ###########################################################
class TestRenderCommentLines:
    def test_block_with_name(_):
        lines = render_comment_lines("X")
        assert lines[:2] == ["<!--", "blueprint: X"]
        assert re.fullmatch("Kaye Engine v.+", lines[2])
        assert lines[3:] == ["-->"]

    def test_block_without_name(_):
        lines = render_comment_lines()
        assert lines[0] == "<!--"
        assert re.fullmatch("Kaye Engine v.+", lines[1])
        assert lines[2:] == ["-->"]

    def test_compact_is_one_line(_):
        lines = render_comment_lines("X", is_compact=True)
        assert len(lines) == 1
        assert re.fullmatch(
            "<!-- blueprint: X↵Kaye Engine v.+ -->", lines[0]
        )

    def test_registered_line_in_block(_):
        register_comment_line("Client v1")
        lines = render_comment_lines("X")
        assert lines[-2:] == ["Client v1", "-->"]

    def test_registered_line_in_compact(_):
        register_comment_line("Client v1")
        (line,) = render_comment_lines("X", is_compact=True)
        assert line.endswith("↵Client v1 -->")

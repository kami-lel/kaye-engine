"""
prompt-render_comment_registry_test.py

Unit Tests (using pytest) for:

- register_comment_line()
- comment_line_registry
"""

import pytest
from kaye_engine.prompt.blueprint.render.comment import (
    comment_line_registry,
    register_comment_line,
)


@pytest.fixture(autouse=True)
def restore_registry():
    snapshot = list(comment_line_registry)
    yield
    comment_line_registry[:] = snapshot


# Pytest unit tests  ###########################################################
class TestRegisterCommentLine:
    def test_appends_line(_):
        register_comment_line("Client v1")
        assert "Client v1" in comment_line_registry

    def test_keeps_first_seen_order(_):
        register_comment_line("B line")
        register_comment_line("A line")
        assert comment_line_registry[-2:] == ["B line", "A line"]

    def test_dedupes_repeated_line(_):
        register_comment_line("Client v1")
        register_comment_line("Client v1")
        assert comment_line_registry.count("Client v1") == 1

    def test_rejects_non_str(_):
        with pytest.raises(TypeError):
            register_comment_line(1)

    @pytest.mark.parametrize("line", ["a\nb", "a\rb", "a --> b"])
    def test_rejects_invalid_content(_, line):
        with pytest.raises(ValueError):
            register_comment_line(line)
        assert line not in comment_line_registry


class TestPublicExport:
    def test_top_level_import(_):
        from kaye_engine import register_comment_line as exported

        assert exported is register_comment_line

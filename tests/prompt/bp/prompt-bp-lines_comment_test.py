"""
prompt-bp-lines_comment_test.py

Unit Tests (using pytest) for the comment appended by:

- render_prompt_lines()
- render_negative_prompt_lines()
"""

import re

import pytest
from kaye_engine.prompt import PromptBlueprint
from kaye_engine.prompt.blueprint import render
from kaye_engine.prompt.blueprint.render.comment import (
    comment_line_registry,
    register_comment_line,
)
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


@pytest.fixture(autouse=True)
def restore_registry():
    snapshot = list(comment_line_registry)
    comment_line_registry.clear()
    yield
    comment_line_registry[:] = snapshot


def _build_bp():
    corpus = PromptCorpusNode.parse("○", None, ["# Prompt", "AAAA"])
    return PromptBlueprint.create_full_blueprint(corpus_tree=corpus)


# Pytest unit tests  ###########################################################
class TestCommentShape:
    def test_block_by_default(_):
        opt = render.render_prompt_lines(
            _build_bp(), profile=RenderProfile(show_comment=True, sparseness=1)
        )

        assert opt[-3] == "<!--"
        assert re.fullmatch("Kaye Engine v.+", opt[-2])
        assert opt[-1] == "-->"

    def test_single_line_at_sparseness_minus_one(_):
        opt = render.render_prompt_lines(
            _build_bp(), profile=RenderProfile(show_comment=True, sparseness=-1)
        )

        assert len(opt) == 1
        assert re.fullmatch(r".*<!-- Kaye Engine v.+ -->", opt[0])

    def test_explicit_flag_overrides_sparseness(_):
        opt = render.render_prompt_lines(
            _build_bp(),
            profile=RenderProfile(show_comment=True, sparseness=99),
            is_comment_compact=True,
        )

        assert re.fullmatch("<!-- Kaye Engine v.+ -->", opt[-1])

    def test_registered_line_follows_default_lines(_):
        register_comment_line("Client v1")

        opt = render.render_prompt_lines(
            _build_bp(), profile=RenderProfile(show_comment=True, sparseness=1)
        )

        assert opt[-2:] == ["Client v1", "-->"]


class TestImageMode:
    def test_registered_heading_like_line_is_not_flattened(_):
        register_comment_line("# Client")

        opt = render.render_prompt_lines(
            _build_bp(),
            profile=RenderProfile(
                show_comment=True, sparseness=1, mode=RenderMode._IMAGE
            ),
        )

        assert "# Client" in opt
        assert "Prompt:" in opt

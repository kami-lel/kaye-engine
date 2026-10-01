"""
prompt-bp-prompt_test.py

Unit Tests (using pytest) for:

render_prompt, render_prompt_without_dependencies, render_blueprint,
render_blueprint_without_dependencies
"""

import re
from types import SimpleNamespace

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint, create_blueprint
from kaye_engine.prompt.blueprint.dynamic_substitution import (
    dynamic_substitution_registry,
    register_dynamic_substitution,
    StringDynamicSubstitution,
)
from kaye_engine.prompt.blueprint.registry import blueprint_registry
from kaye_engine.prompt.blueprint.render import (
    render_blueprint,
    render_blueprint_without_dependencies,
    render_prompt,
    render_prompt_without_dependencies,
)
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Some
Intro line.
## Prompt
AAAA (((my-sub))) BBBB
### {avoid}
blurry
## Other
CCCC
"""

SOME = ("Some",)
PROMPT = ("Some", "Prompt")
OTHER = ("Some", "Other")


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


@pytest.fixture
def registry():
    added = []

    def add(name, blueprint):
        blueprint_registry[name] = SimpleNamespace(blueprint=blueprint)
        added.append(name)

    yield add

    for name in added:
        blueprint_registry.pop(name, None)


@pytest.fixture
def substitution():
    register_dynamic_substitution("my-sub", StringDynamicSubstitution("XX"))
    yield
    dynamic_substitution_registry.pop("my-sub", None)


def _bp(*paths, **kwargs):
    return Blueprint(nodes=frozenset(paths), **kwargs)


# pytest  ######################################################################
class TestRenderPrompt:

    def test_text_of_selected_nodes(_, substitution):
        out = render_prompt(_bp(SOME, PROMPT))

        assert out == "# Some\nIntro line.\n\n## Prompt\nAAAA XX BBBB"

    def test_returns_str(_, substitution):
        assert isinstance(render_prompt(_bp(PROMPT)), str)

    def test_empty_blueprint(_):
        assert render_prompt(Blueprint()) == ""

    def test_substitution_after_render(_, substitution):
        assert "(((my-sub)))" not in render_prompt(_bp(PROMPT))

    def test_unregistered_placeholder_kept(_):
        assert "(((my-sub)))" in render_prompt(_bp(PROMPT))

    def test_dependencies_merged(_, registry, substitution):
        registry("dep", _bp(OTHER))
        out = render_prompt(_bp(PROMPT, dependencies=("dep",)))

        assert "AAAA XX BBBB" in out
        assert "CCCC" in out

    def test_without_dependencies_ignores_them(_, registry):
        registry("dep", _bp(OTHER))
        out = render_prompt_without_dependencies(
            _bp(PROMPT, dependencies=("dep",))
        )

        assert "CCCC" not in out

    def test_dependency_cycle_raises(_, registry):
        registry("a", Blueprint(dependencies=("b",)))
        registry("b", Blueprint(dependencies=("a",)))

        with pytest.raises(ValueError, match="cycle"):
            render_prompt(Blueprint(dependencies=("a",)))

    def test_query_forwarded_to_dynamic_nodes(_):
        out = render_prompt(
            _bp(("(decode-only-abbr)",)), query="use an algo"
        )

        assert out.startswith("# (decode-only-abbr)")


class TestSparseness:

    def test_default_collapses_blank_runs(_, substitution):
        out = render_prompt(_bp(SOME, PROMPT))

        assert "\n\n\n" not in out

    def test_zero_removes_blank_lines(_, substitution):
        out = render_prompt(
            _bp(SOME, PROMPT), profile=RenderProfile(sparseness=0)
        )

        assert "\n\n" not in out

    def test_minus_one_is_one_line(_, substitution):
        out = render_prompt(
            _bp(SOME, PROMPT), profile=RenderProfile(sparseness=-1)
        )

        assert "\n" not in out
        assert "↵" in out

    def test_sparseness_applied_after_substitution(_):
        # a substitution that yields blank lines is trimmed too
        register_dynamic_substitution(
            "my-sub", StringDynamicSubstitution("\n\n\n\n")
        )
        try:
            out = render_prompt(_bp(PROMPT))
        finally:
            dynamic_substitution_registry.pop("my-sub", None)

        assert "\n\n\n" not in out


class TestModes:

    def test_negative_mode_renders_avoid_content(_):
        out = render_prompt(
            _bp(PROMPT), profile=RenderProfile(mode=RenderMode.NEGATIVE)
        )

        assert out == "## Prompt\nblurry"

    def test_image_mode_forces_sparseness_one(_):
        out = render_prompt(
            _bp(PROMPT, OTHER),
            profile=RenderProfile(mode=RenderMode.IMAGE, sparseness=-1),
        )

        assert "\n" in out
        assert "↵" not in out

    def test_image_mode_flattens_headings(_, substitution):
        out = render_prompt(
            _bp(PROMPT), profile=RenderProfile(mode=RenderMode.IMAGE)
        )

        assert out.startswith("Prompt:\n")

    def test_negative_image_mode_has_no_titles(_):
        out = render_prompt(
            _bp(PROMPT),
            profile=RenderProfile(mode=RenderMode.NEGATIVE | RenderMode.IMAGE),
        )

        assert out == "blurry"

    def test_comment_compact_follows_requested_sparseness(_):
        out = render_prompt(
            _bp(PROMPT),
            profile=RenderProfile(show_comment=True, sparseness=-1),
        )

        assert re.search(r"<!-- .*Kaye Engine v.+ -->", out)


class TestRenderBlueprint:

    def test_preview_of_merged_selection(_, registry):
        registry("dep", _bp(OTHER))
        out = render_blueprint(
            _bp(PROMPT, dependencies=("dep",)), content_preview_lines=0
        )

        assert "[x]     ├── Prompt" in out
        assert "[x]     └── Other" in out

    def test_without_dependencies(_, registry):
        registry("dep", _bp(OTHER))
        out = render_blueprint_without_dependencies(
            _bp(PROMPT, dependencies=("dep",)), content_preview_lines=0
        )

        assert "Other" not in out
        assert "[x]     └── Prompt" in out

    def test_full_tree_option_forwarded(_):
        out = render_blueprint(
            create_blueprint(), show_full_tree=True, content_preview_lines=0
        )

        assert "[ ] ├── Some" in out

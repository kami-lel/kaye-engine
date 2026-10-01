"""
prompt-bp-negative_prompt_test.py

Unit Tests (using pytest) for:

render_negative_prompt_lines
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.render.lines import (
    render_negative_prompt_lines,
)
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.selection import bind_selection
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# Scene
## Subject
### {avoid}
blurry
## Style
### {avoid}
cartoon
### {description}
not an avoid
## Plain
# Mood
## Light
### {avoid}
dark
### Deep
#### {avoid}
muddy
"""

SCENE = ("Scene",)
SUBJECT = ("Scene", "Subject")
STYLE = ("Scene", "Style")
PLAIN = ("Scene", "Plain")
MOOD = ("Mood",)
LIGHT = ("Mood", "Light")
DEEP = ("Mood", "Light", "Deep")
M = RenderMode


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


def _render(paths, mode=M.NEGATIVE, **profile_kwargs):
    selection = bind_selection(Blueprint(nodes=frozenset(paths)))
    return render_negative_prompt_lines(
        selection, profile=RenderProfile(mode=mode, **profile_kwargs)
    )


# pytest  ######################################################################
class TestNormalOrder:

    def test_selected_nodes_with_avoid(_):
        assert _render([SUBJECT, STYLE]) == [
            "## Subject", "blurry", "", "## Style", "cartoon",
        ]

    def test_unselected_node_contributes_no_own_avoid(_):
        assert _render([STYLE]) == ["## Style", "cartoon"]

    def test_non_avoid_sidecars_never_contribute(_):
        assert "not an avoid" not in _render([SCENE, STYLE, PLAIN])

    def test_node_without_avoid_is_omitted(_):
        assert _render([PLAIN]) == []

    def test_empty_selection(_):
        assert _render([]) == []

    def test_transparent_node_shows_descendant_only(_):
        # Mood and Light are selected but only Deep carries {avoid}
        # of a selected node: Light's own {avoid} needs Light selected
        assert _render([DEEP]) == ["### Deep", "muddy"]

    def test_parent_before_children_with_blank_line(_):
        assert _render([LIGHT, DEEP]) == [
            "## Light", "dark", "", "### Deep", "muddy",
        ]

    def test_descendants_walked_without_selected_ancestor(_):
        assert _render([DEEP, SUBJECT]) == [
            "## Subject", "blurry", "", "### Deep", "muddy",
        ]


class TestPostOrder:

    def test_child_blocks_before_own(_):
        assert _render([LIGHT, DEEP], M.NEGATIVE | M.POST_ORDER) == [
            "### Deep", "muddy", "", "## Light", "dark",
        ]

    def test_siblings_keep_order(_):
        assert _render([SUBJECT, STYLE], M.NEGATIVE | M.POST_ORDER) == [
            "## Subject", "blurry", "", "## Style", "cartoon",
        ]


class TestReverseOrder:

    def test_siblings_reversed(_):
        assert _render([SUBJECT, STYLE], M.NEGATIVE | M.REVERSE_ORDER) == [
            "## Style", "cartoon", "", "## Subject", "blurry",
        ]

    def test_top_level_reversed(_):
        out = _render([SUBJECT, LIGHT], M.NEGATIVE | M.REVERSE_ORDER)

        assert out == ["## Light", "dark", "", "## Subject", "blurry"]


class TestImage:

    def test_titles_dropped_in_negative_image(_):
        out = _render([SUBJECT, STYLE], M.NEGATIVE | M.IMAGE)

        assert out == ["cartoon", "", "blurry"]

    def test_image_without_negative_flag_keeps_titles_flattened(_):
        out = _render([SUBJECT, STYLE], M.IMAGE)

        assert out == ["Style:", "cartoon", "", "Subject:", "blurry"]


class TestComment:

    def test_comment_appended_last(_):
        out = _render([SUBJECT], show_comment=True, display_name="Demo")

        assert out[-1] == "-->"
        assert "blueprint: Demo" in out

    def test_compact_comment(_):
        out = _render([SUBJECT], show_comment=True, sparseness=-1)

        assert len(out) == 1


class TestSidecarSplice:

    def test_spliced_avoid_counts_once_parent_selected(_):
        # {avoid} is a sidecar: splicing it in does not change what the
        # negative walk prints, which keys on the parent being selected
        plain = _render([SUBJECT])
        spliced = _render([SUBJECT], conditional_sidecars=("avoid",))

        assert spliced == plain

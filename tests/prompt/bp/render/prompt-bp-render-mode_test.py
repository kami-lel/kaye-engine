"""
prompt-bp-render-mode_test.py

Unit Tests (using pytest) for:

render_prompt_lines, RenderMode.POST_ORDER / REVERSE_ORDER / IMAGE
"""

import pytest

from kaye_engine.prompt.blueprint.data import Blueprint
from kaye_engine.prompt.blueprint.render.lines import render_prompt_lines
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.blueprint.selection import bind_selection
from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree

_SOURCE = """# A
a
## B
b
## C
c
# D
d
"""

A = ("A",)
B = ("A", "B")
C = ("A", "C")
D = ("D",)


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def corpus():
    load_corpus_tree([_SOURCE])


def _render(paths, mode, **profile_kwargs):
    selection = bind_selection(Blueprint(nodes=frozenset(paths)))
    return render_prompt_lines(
        selection, profile=RenderProfile(mode=mode, **profile_kwargs)
    )


# pytest  ######################################################################
class TestNormalBaseline:

    def test_pre_order(_):
        assert _render([A, B, C, D], RenderMode.NORMAL) == [
            "# A", "a", "", "## B", "b", "", "## C", "c", "", "# D", "d",
        ]


class TestReverseOrder:

    def test_siblings_reversed_at_every_level(_):
        assert _render([A, B, C, D], RenderMode.REVERSE_ORDER) == [
            "# D", "d", "", "# A", "a", "", "## C", "c", "", "## B", "b",
        ]

    def test_last_node_walked_gets_no_blank_line(_):
        # B is last in the reversed walk, so nothing trails it even with
        # trimming off; it is not last in corpus order
        raw = _render([B], RenderMode.REVERSE_ORDER, sparseness=99)

        assert raw == ["## B", "b"]

    def test_node_last_in_corpus_order_still_gets_blank(_):
        raw = _render([C], RenderMode.REVERSE_ORDER, sparseness=99)

        assert raw == ["## C", "c", ""]

    def test_normal_mode_blank_rule_unchanged(_):
        assert _render([B], RenderMode.NORMAL, sparseness=99) == [
            "## B", "b", "",
        ]

    def test_disable_first_heading_skips_first_walked(_):
        assert _render(
            [A, D], RenderMode.REVERSE_ORDER, disable_first_heading=True
        ) == ["d", "", "# A", "a"]


class TestPostOrder:

    def test_children_before_parent(_):
        assert _render([A, B, C, D], RenderMode.POST_ORDER) == [
            "## B", "b", "", "## C", "c", "", "# A", "a", "", "# D", "d",
        ]

    def test_unselected_parent_is_skipped(_):
        assert _render([B, C], RenderMode.POST_ORDER) == [
            "## B", "b", "", "## C", "c",
        ]

    def test_unselected_subtree_contributes_nothing(_):
        assert _render([D], RenderMode.POST_ORDER) == ["# D", "d"]

    def test_empty_selection(_):
        assert _render([], RenderMode.POST_ORDER) == []

    def test_disable_first_heading_removes_first_heading_line(_):
        assert _render(
            [A, B], RenderMode.POST_ORDER, disable_first_heading=True
        ) == ["b", "", "# A", "a"]


class TestPostOrderReverse:

    def test_both_flags(_):
        mode = RenderMode.POST_ORDER | RenderMode.REVERSE_ORDER

        assert _render([A, B, C, D], mode) == [
            "# D", "d", "", "## C", "c", "", "## B", "b", "", "# A", "a",
        ]


class TestImage:

    def test_flattened_headings_post_order_reversed(_):
        assert _render([A, B, C, D], RenderMode.IMAGE) == [
            "D:", "d", "", "C:", "c", "", "B:", "b", "", "A:", "a",
        ]

    def test_comment_stays_untouched(_):
        out = _render([D], RenderMode.IMAGE, show_comment=True)

        assert out[-1] == "-->"
        assert "<!--" in out

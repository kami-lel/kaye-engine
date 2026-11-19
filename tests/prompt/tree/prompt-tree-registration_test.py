"""
prompt-tree-registration_test.py

Unit Tests (using pytest) for: register_corpus_under_node, building the
tree with load_corpus_tree from registrations alone, including a source
grafted under a conditional sidecar and how that graft renders
"""

import pytest

from kaye_engine.prompt.blueprint import (
    create_blueprint_from_node,
    get_corpus_node,
)
from kaye_engine.prompt.blueprint.render.prompt import render_prompt
from kaye_engine.prompt.blueprint.render_profile import RenderProfile
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
    register_corpus_under_node,
)


# pytest fixtures  #############################################################
@pytest.fixture(autouse=True)
def _clean_corpus():
    clear_corpus_tree()
    yield
    clear_corpus_tree()


def _static_names(node):
    return [c.name for c in node.children if not c.name.startswith("(")]


# pytest  ######################################################################
class TestStructure:

    def test_root_registrations_build_tree(_):
        register_corpus_under_node((), "# A\nContent A.\n")
        register_corpus_under_node((), "# B\nContent B.\n")

        tree = load_corpus_tree()

        assert _static_names(tree) == ["A", "B"]
        assert tree["A"].content_lines() == ["Content A.", ""]

    def test_source_under_node(_):
        register_corpus_under_node((), "# A\nContent A.\n## a1\n")
        register_corpus_under_node(("A",), "## a2\nContent a2.\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]) == ["a1", "a2"]
        assert tree["A"]["a2"].depth == 2

    def test_str_node_path_is_one_heading(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node("A", "## a1\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]) == ["a1"]

    def test_clear_drops_registrations(_):
        register_corpus_under_node((), "# A\n")
        load_corpus_tree()
        clear_corpus_tree()

        tree = load_corpus_tree()

        assert _static_names(tree) == []


class TestSidecarTarget:

    @pytest.fixture
    def grafted_blueprint(_):
        register_corpus_under_node((), "# A\nbody A\n## {a}\nrule a\n")
        register_corpus_under_node(
            ("A", "{a}"), "lead in\n### {for B}\nexample B\n"
        )
        load_corpus_tree()
        return create_blueprint_from_node(
            get_corpus_node("A"), is_recursive=True
        )

    def test_graft_lands_under_sidecar(_, grafted_blueprint):
        node = get_corpus_node("A", "{a}")

        assert [c.name for c in node.children] == ["{for B}"]
        assert "lead in" in node.content_lines()

    @pytest.mark.parametrize(
        "sidecars, has_rule, has_example",
        [
            ((), False, False),
            (("a",), True, False),
            (("for B",), False, False),
            (("a", "for B"), True, True),
        ],
    )
    def test_grafted_sidecar_spliced_only_under_its_parent(
        _, grafted_blueprint, sidecars, has_rule, has_example
    ):
        text = render_prompt(
            grafted_blueprint,
            profile=RenderProfile(
                conditional_sidecars=sidecars, show_comment=False
            ),
        )

        assert "body A" in text
        assert ("rule a" in text) is has_rule
        assert ("lead in" in text) is has_rule
        assert ("example B" in text) is has_example

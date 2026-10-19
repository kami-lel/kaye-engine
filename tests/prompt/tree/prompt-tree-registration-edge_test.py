"""
prompt-tree-registration-edge_test.py

Unit Tests (using pytest) for: edge cases of register_corpus_under_node
and load_corpus_tree -- order, unresolved and refused targets, heading
levels, duplicates, leading content, dynamic headings, leaks across
sources, and the registration lifecycle
"""

from pathlib import Path
from unittest.mock import patch

import pytest

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
class TestOrder:

    def test_two_contributors_keep_registration_order(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "## x\n")
        register_corpus_under_node(("A",), "## y\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]) == ["x", "y"]

    def test_child_registered_before_its_target(_):
        register_corpus_under_node(("A", "a1"), "### deep\n")
        register_corpus_under_node(("A",), "## a1\n")
        register_corpus_under_node((), "# A\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]["a1"]) == ["deep"]


class TestUnresolved:

    def test_unresolved_path_raises_naming_path(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("Missing",), "## x\n")

        with pytest.raises(ValueError, match="Missing"):
            load_corpus_tree()

    def test_unresolved_names_source(_):
        register_corpus_under_node(("Missing",), Path("vendor.md"))

        with pytest.raises(ValueError, match="vendor.md"):
            load_corpus_tree()


class TestHeadingLevel:

    def test_too_deep_under_root_raises(_):
        register_corpus_under_node((), "## A\n")

        with pytest.raises(ValueError, match="top headings"):
            load_corpus_tree()

    def test_too_shallow_under_node_raises(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "# B\n")

        with pytest.raises(ValueError, match="top headings"):
            load_corpus_tree()

    def test_too_deep_under_node_raises(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "### b\n")

        with pytest.raises(ValueError, match="top headings"):
            load_corpus_tree()

    def test_shallower_heading_later_raises(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "## b\n# C\n")

        with pytest.raises(ValueError, match="top headings"):
            load_corpus_tree()

    def test_fenced_heading_is_not_counted(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "## b\n```\n# not a heading\n```\n")

        tree = load_corpus_tree()

        assert _static_names(tree["A"]) == ["b"]

    def test_local_heading_deeper_is_content(_):
        register_corpus_under_node((), "# A\n#### local\ntext\n")

        tree = load_corpus_tree()

        assert "#### local" in tree["A"].content_lines()


class TestRefusedTarget:

    @pytest.mark.parametrize(
        "node_path", [("A", "{description}"), ("(today)",), ("A", "(x)")]
    )
    def test_sidecar_or_dynamic_target_refused(_, node_path):
        with pytest.raises(ValueError, match="sidecar or dynamic"):
            register_corpus_under_node(node_path, "text\n")

    def test_str_source_ending_md_raises(_):
        with pytest.raises(ValueError, match=r"\.md"):
            register_corpus_under_node((), "corpus.md")

    def test_swapped_arguments_raise(_):
        with pytest.raises(ValueError, match="file path"):
            register_corpus_under_node("corpus/a.md", ())

    def test_list_node_path_raises(_):
        with pytest.raises(TypeError):
            register_corpus_under_node(["A"], "## x\n")

    def test_empty_heading_raises(_):
        with pytest.raises(ValueError, match="non-empty"):
            register_corpus_under_node(("A", ""), "### x\n")

    def test_non_str_source_raises(_):
        with pytest.raises(TypeError):
            register_corpus_under_node((), 5)


class TestDuplicateSiblings:

    def test_duplicate_within_one_source_raises(_):
        register_corpus_under_node((), "# A\n## x\n## x\n")

        with pytest.raises(ValueError, match="duplicate heading 'x'"):
            load_corpus_tree()

    def test_duplicate_across_sources_names_both(_):
        register_corpus_under_node((), Path("one.md"))
        register_corpus_under_node((), Path("two.md"))
        content = {"one.md": "# A\n", "two.md": "# A\n"}

        def _read(source):
            return content[str(source)]

        with patch(
            "kaye_engine.prompt.prompt_corpus_loader._read_content_source",
            side_effect=_read,
        ):
            with pytest.raises(ValueError) as exc_info:
                load_corpus_tree()

        assert "one.md" in str(exc_info.value)
        assert "two.md" in str(exc_info.value)

    def test_same_heading_under_different_parents_is_fine(_):
        register_corpus_under_node((), "# A\n## x\n# B\n## x\n")

        tree = load_corpus_tree()

        assert _static_names(tree["B"]) == ["x"]


class TestLeadingContent:

    def test_leading_content_appended_to_target(_):
        register_corpus_under_node((), "# A\nOwn.\n")
        register_corpus_under_node(("A",), "Added.\n## x\n")

        tree = load_corpus_tree()

        assert tree["A"].content_lines()[0] == "Own."
        assert "Added." in tree["A"].content_lines()

    def test_heading_free_source_is_all_content(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "only text\n")

        tree = load_corpus_tree()

        assert tree["A"].content_lines() == ["only text", ""]


class TestDynamicHeading:

    def test_dynamic_heading_in_attached_source(_):
        register_corpus_under_node((), "# A\n")
        register_corpus_under_node(("A",), "## (today)\nPreface.\n")

        tree = load_corpus_tree()

        assert "(today)" in [c.name for c in tree["A"].children]
        assert "(today)" not in [c.name for c in tree.children]

    def test_duplicate_dynamic_heading_across_sources_raises(_):
        register_corpus_under_node((), "# (today)\n")
        register_corpus_under_node((), "# A\n## (today)\n")

        with pytest.raises(ValueError, match="duplicate heading for dynamic"):
            load_corpus_tree()


class TestNoLeak:

    def test_unclosed_fence_stays_in_its_source(_):
        register_corpus_under_node((), "# A\n```\nopen fence\n")
        register_corpus_under_node((), "# B\n")

        tree = load_corpus_tree()

        assert _static_names(tree) == ["A", "B"]

    def test_unclosed_comment_stays_in_its_source(_):
        register_corpus_under_node((), "# A\n<!-- never closed\n")
        register_corpus_under_node((), "# B\n<!-- closed -->\nB text\n")

        tree = load_corpus_tree()

        assert _static_names(tree) == ["A", "B"]
        assert "<!-- never closed" in tree["A"].content_lines()
        assert tree["B"].content_lines() == ["B text", ""]


class TestLifecycle:

    def test_registration_after_load_raises(_):
        register_corpus_under_node((), "# A\n")
        load_corpus_tree()

        with pytest.raises(ValueError, match="already loaded"):
            register_corpus_under_node((), "# B\n")

    def test_second_load_raises(_):
        load_corpus_tree()

        with pytest.raises(ValueError, match="already loaded"):
            load_corpus_tree()

    def test_clear_then_register_again(_):
        register_corpus_under_node((), "# A\n")
        load_corpus_tree()
        clear_corpus_tree()
        register_corpus_under_node((), "# B\n")

        tree = load_corpus_tree()

        assert _static_names(tree) == ["B"]

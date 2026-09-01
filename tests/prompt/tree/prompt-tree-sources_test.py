"""
prompt-tree-sources_test.py

Unit Tests (using pytest) for:

load_corpus_tree combining multiple ``sources`` -- str (literal
content) and Path (file to read) entries -- as if they were one file
"""

from pathlib import Path
from unittest.mock import mock_open, patch

from kaye_engine.prompt.prompt_corpus_loader import load_corpus_tree


# auxiliaries  #################################################################


def _open_side_effect(content_by_path):
    """
    :return: a ``builtins.open`` replacement dispatching to a
            per-path :func:`mock_open`, keyed by ``str(path)``
    :rtype: callable
    """

    def _open(path, *args, **kwargs):
        return mock_open(read_data=content_by_path[str(path)])(
            path, *args, **kwargs
        )

    return _open


# pytest  ######################################################################


class TestPathSources:

    def test_two_path_sources_combine_in_order(_):
        content_by_path = {
            "a.md": "# A\nContent A.\n",
            "b.md": "# B\nContent B.\n",
        }

        with patch(
            "builtins.open", side_effect=_open_side_effect(content_by_path)
        ):
            tree = load_corpus_tree(
                "sources-two-path-test", [Path("a.md"), Path("b.md")]
            )

        assert [c.name for c in tree.children][:2] == ["A", "B"]


class TestStrSources:

    def test_str_source_used_as_literal_content(_):
        def _open_raising(*args, **kwargs):
            raise AssertionError("open() must not be called for a str source")

        with patch("builtins.open", side_effect=_open_raising):
            tree = load_corpus_tree(
                "sources-str-literal-test", ["# A\nContent A.\n"]
            )

        assert [c.name for c in tree.children][:1] == ["A"]


class TestMixedSources:

    def test_mixed_str_and_path_sources_preserve_order(_):
        content_by_path = {"b.md": "# B\nContent B.\n"}

        with patch(
            "builtins.open", side_effect=_open_side_effect(content_by_path)
        ):
            tree = load_corpus_tree(
                "sources-mixed-order-test",
                ["# A\nContent A.\n", Path("b.md"), "# C\nContent C.\n"],
            )

        assert [c.name for c in tree.children][:3] == ["A", "B", "C"]


class TestSourceJoinBoundary:

    def test_no_trailing_newline_sources_still_parse_as_two_sections(_):
        # neither source ends in "\n" -- the "\n\n" join must still
        # keep the second source's heading from gluing onto the first
        # source's last line
        tree = load_corpus_tree(
            "sources-no-trailing-newline-test",
            ["# A\nContent A.", "# B\nContent B."],
        )

        assert [c.name for c in tree.children][:2] == ["A", "B"]

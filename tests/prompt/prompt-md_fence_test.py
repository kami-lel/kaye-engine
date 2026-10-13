"""
prompt-md_fence_test.py

Unit Tests (using pytest) for: compute_fenced_line_mask()
"""

from kaye_engine.prompt.md_fence import compute_fenced_line_mask


# Pytest unit tests  ###########################################################
class TestComputeFencedLineMask:

    def test_no_fence(_):
        lines = ["Text.", "", "More text."]
        assert compute_fenced_line_mask(lines) == [False, False, False]

    def test_fence_with_language_tag(_):
        lines = ["Before.", "```cpp", "int x = 1;", "```", "After."]
        assert compute_fenced_line_mask(lines) == [
            False,
            True,
            True,
            True,
            False,
        ]

    def test_bare_fence(_):
        lines = ["Before.", "```", "content", "```", "After."]
        assert compute_fenced_line_mask(lines) == [
            False,
            True,
            True,
            True,
            False,
        ]

    def test_tilde_fence(_):
        lines = ["Before.", "~~~", "content", "~~~", "After."]
        assert compute_fenced_line_mask(lines) == [
            False,
            True,
            True,
            True,
            False,
        ]

    def test_blank_lines_inside_fence_stay_marked(_):
        lines = ["```", "line1", "", "", "line2", "```"]
        assert compute_fenced_line_mask(lines) == [
            True,
            True,
            True,
            True,
            True,
            True,
        ]

    def test_text_after_closed_fence_is_unmarked(_):
        lines = ["```", "code", "```", "", "prose"]
        assert compute_fenced_line_mask(lines) == [
            True,
            True,
            True,
            False,
            False,
        ]

    def test_two_separate_fences(_):
        lines = ["```py", "a", "```", "mid", "```js", "b", "```"]
        assert compute_fenced_line_mask(lines) == [
            True,
            True,
            True,
            False,
            True,
            True,
            True,
        ]


class TestComputeFencedLineMaskTagBlock:

    def test_plain_tag_block_with_inner_blank(_):
        lines = ["a", "<some-tag>", "x", "", "y", "</some-tag>", "b"]
        assert compute_fenced_line_mask(lines) == [
            False,
            True,
            True,
            True,
            True,
            True,
            False,
        ]

    def test_tag_with_attributes(_):
        lines = ['<note kind="x">', "", "</note>"]
        assert compute_fenced_line_mask(lines) == [True, True, True]

    def test_indented_tag(_):
        lines = ["    <t>", "", "    </t>", ""]
        assert compute_fenced_line_mask(lines) == [True, True, True, False]

    def test_unclosed_tag_marks_nothing(_):
        lines = ["<your description text>", "", "prose"]
        assert compute_fenced_line_mask(lines) == [False, False, False]
        assert compute_fenced_line_mask(["<t>", "", "x"]) == [False] * 3

    def test_tag_inside_fence_is_plain_fenced_text(_):
        lines = ["```", "<t>", "```", "", "</t>"]
        assert compute_fenced_line_mask(lines) == [
            True,
            True,
            True,
            False,
            False,
        ]

    def test_fence_inside_tag_is_masked(_):
        lines = ["<t>", "```", "", "```", "", "</t>", ""]
        assert compute_fenced_line_mask(lines) == [True] * 6 + [False]

    def test_two_sequential_blocks(_):
        lines = ["<a>", "", "</a>", "", "<b>", "", "</b>"]
        assert compute_fenced_line_mask(lines) == [
            True,
            True,
            True,
            False,
            True,
            True,
            True,
        ]

    def test_inline_tag_is_not_a_block(_):
        lines = ["<a>x</a>", "", "<a>", "y"]
        assert compute_fenced_line_mask(lines) == [False] * 4

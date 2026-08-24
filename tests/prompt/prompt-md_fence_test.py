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

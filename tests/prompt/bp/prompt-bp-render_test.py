"""
prompt-bp-render_test.py

Unit Tests (using pytest) for: apply_sparseness()
"""

from kaye_engine.prompt.blueprint.render import (
    NO_TRIM_SPARSENESS,
    REPLACEMENT_NEWLINE_SYMBOL,
    apply_sparseness,
)


# Pytest unit tests  ###########################################################
class TestApplySparsenessRespectsCodeFence:

    def _lines(_):
        return [
            "Text.",
            "",
            "```cpp",
            "line1",
            "",
            "",
            "line2",
            "```",
            "",
            "More.",
        ]

    def test_no_trim(_):
        opt = apply_sparseness(_._lines(), NO_TRIM_SPARSENESS)
        assert opt == _._lines()

    def test_zero_strips_only_unfenced_blanks(_):
        opt = apply_sparseness(_._lines(), 0)

        print(opt)
        assert opt == [
            "Text.",
            "```cpp",
            "line1",
            "",
            "",
            "line2",
            "```",
            "More.",
        ]

    def test_default_one_leaves_fence_untouched(_):
        opt = apply_sparseness(_._lines(), 1)

        print(opt)
        assert opt == _._lines()

    def test_minus_one_preserves_multiple_fenced_blanks(_):
        opt = apply_sparseness(_._lines(), -1)

        print(opt)
        assert opt == [REPLACEMENT_NEWLINE_SYMBOL.join(_._lines())]

    def test_leading_trailing_fence_not_trimmed(_):
        lines = ["```", "", "code", "", "```"]

        opt = apply_sparseness(lines, 0)

        print(opt)
        assert opt == lines

"""
prompt-md_comment_test.py

Unit Tests (using pytest) for: strip_comment_blocks()
"""

from kaye_engine.prompt.md_comment import strip_comment_blocks


# Pytest unit tests  ###########################################################
class TestStripSingleLine:

    def test_no_comment_unchanged(_):
        lines = ["Text.", "", "More text."]
        assert strip_comment_blocks(lines) == lines

    def test_single_line_comment_dropped(_):
        lines = ["Before.", "<!-- note -->", "After."]
        assert strip_comment_blocks(lines) == ["Before.", "After."]

    def test_indented_comment_dropped(_):
        assert strip_comment_blocks(["  <!-- note -->"]) == []

    def test_inline_code_mention_kept(_):
        lines = ["collect under a `<!-- Endnotes -->` marker"]
        assert strip_comment_blocks(lines) == lines

    def test_trailing_comment_after_prose_kept(_):
        lines = ["Prose. <!-- note -->"]
        assert strip_comment_blocks(lines) == lines


class TestStripMultiLine:

    def test_block_dropped(_):
        lines = ["Before.", "<!--", "TODO a", "TODO b", "-->", "", "After."]
        assert strip_comment_blocks(lines) == ["Before.", "", "After."]

    def test_unclosed_opener_kept(_):
        lines = ["Before.", "<!--", "TODO a", "After."]
        assert strip_comment_blocks(lines) == lines

    def test_two_blocks_dropped(_):
        lines = ["<!--", "a", "-->", "Mid.", "<!-- b -->", "<!--", "c", "-->"]
        assert strip_comment_blocks(lines) == ["Mid."]

    def test_close_on_prose_line_ends_block(_):
        lines = ["<!-- start", "end -->", "After."]
        assert strip_comment_blocks(lines) == ["After."]

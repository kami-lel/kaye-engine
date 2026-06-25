"""
cli-a-cz-claude_md_test.py

Unit Tests (using pytest) for:

``python -m kaye claude code`` — verifies CLAUDE.md is created in the
exported folder.
"""


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_claude_md_exists(self, testee_claude_folder):
        assert (testee_claude_folder / "CLAUDE.md").exists()

    def test_claude_md_is_file(self, testee_claude_folder):
        assert (testee_claude_folder / "CLAUDE.md").is_file()

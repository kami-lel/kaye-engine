"""
user_prompt_export_test.py

Unit Tests (using pytest) for:

export_user_system_prompt_file
"""

import os
from unittest.mock import patch

import pytest

from kaye_engine.cli.claude.user_prompt import export
from kaye_engine.cli.claude.user_prompt.export import (
    export_user_system_prompt_file,
)
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _fixed_prompt():
    disable_dry_run()
    with patch.object(
        export, "generate_user_system_prompt", return_value="prompt\n"
    ):
        yield
    disable_dry_run()


# pytest  ######################################################################
class TestExportUserSystemPromptFile:

    def test_missing_file_is_created(_, tmp_path):
        path = tmp_path / "CLAUDE.md"
        export_user_system_prompt_file(path)
        assert path.read_text(encoding="utf-8") == "prompt\n"

    def test_identical_file_is_untouched(_, tmp_path):
        path = tmp_path / "CLAUDE.md"
        path.write_text("prompt\n", encoding="utf-8")
        os.utime(path, (1_000_000, 1_000_000))

        export_user_system_prompt_file(path)
        assert path.stat().st_mtime == 1_000_000

    def test_different_file_is_overwritten(_, tmp_path):
        path = tmp_path / "CLAUDE.md"
        path.write_text("old", encoding="utf-8")

        export_user_system_prompt_file(path)
        assert path.read_text(encoding="utf-8") == "prompt\n"

    def test_dry_run_leaves_different_file_alone(_, tmp_path):
        path = tmp_path / "CLAUDE.md"
        path.write_text("old", encoding="utf-8")

        enable_dry_run()
        export_user_system_prompt_file(path)
        assert path.read_text(encoding="utf-8") == "old"

"""
cli-a-usp-alts_test.py

Unit Tests (using pytest) for:

CLI aliases and flags of ``kaye claude user-system-prompt`` — verifies
subprocess is invoked with the correct command string for each form.
"""

import pytest

from tests.cli.a.s import prepare_root_folder


# Unit test classes  ###########################################################


class TestCommandAliases:  # ===================================================

    @pytest.mark.parametrize("alias,expected", [
        ("claude user-system-prompt", "claude user-system-prompt"),
        ("claude usp", "claude usp"),
        ("a user-system-prompt", "a user-system-prompt"),
        ("a usp", "a usp"),
        ("anthropic usp", "anthropic usp"),
    ])
    def test_command_invoked(
        self,
        mock_run,
        mock_tmp_path,
        mock_tmp_path_factory,
        cli_command,
        alias,
        expected,
    ):
        command = cli_command + alias + " "
        prepare_root_folder(
            tmp_path_factory=mock_tmp_path_factory,
            command=command,
            folder_name="test_folder",
        )
        mock_run.assert_called_once()
        called_command = mock_run.call_args[0][0]
        assert expected in called_command
        assert str(mock_tmp_path) in called_command


class TestFlags:  # ============================================================

    @pytest.mark.parametrize("flags,expected", [
        ("-r", "usp -r"),
        ("--rapid", "usp --rapid"),
        ("-c", "usp -c"),
        ("--coder", "usp --coder"),
        ("-r -c", "usp -r -c"),
    ])
    def test_command_invoked(
        self,
        mock_run,
        mock_tmp_path,
        mock_tmp_path_factory,
        cli_claude_command,
        flags,
        expected,
    ):
        command = cli_claude_command + "usp " + flags + " "
        prepare_root_folder(
            tmp_path_factory=mock_tmp_path_factory,
            command=command,
            folder_name="test_folder",
        )
        mock_run.assert_called_once()
        called_command = mock_run.call_args[0][0]
        assert expected in called_command
        assert str(mock_tmp_path) in called_command

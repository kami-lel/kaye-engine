"""
cli-a-v-alts_test.py

Unit Tests (using pytest) for:

CLI aliases for ``kaye claude vs-code-extension`` — verifies subprocess is
invoked with the correct command string for each alias.
"""

import pytest

from tests.cli.a.s import prepare_root_folder


# Unit test classes  ###########################################################


class TestCliCommand:  # =======================================================

    @pytest.mark.parametrize("alias,expected", [
        ("claude v", "claude v"),
        ("a vs-code-extension", "a vs-code-extension"),
        ("a v", "a v"),
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

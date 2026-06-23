"""
cli-a-s-alts-claude-s_test.py

Unit Tests (using pytest) for:

CLI alias: ``python -m kaye claude s`` — verifies subprocess is invoked with
the correct command string.
"""

from tests.cli.a.s import prepare_root_folder


# Unit test classes  ###########################################################


class TestCliCommand:  # =======================================================

    def test_command_invoked(
        self, mock_run, mock_tmp_path, mock_tmp_path_factory, cli_command
    ):
        command = cli_command + "claude s "
        prepare_root_folder(
            tmp_path_factory=mock_tmp_path_factory,
            command=command,
            folder_name="test_folder",
        )
        mock_run.assert_called_once()
        called_command = mock_run.call_args[0][0]
        assert "claude s" in called_command
        assert str(mock_tmp_path) in called_command

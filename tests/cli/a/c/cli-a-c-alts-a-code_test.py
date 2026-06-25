"""
cli-a-c-alts-a-code_test.py

Unit Tests (using pytest) for:

CLI alias: ``python -m kaye a code`` — verifies subprocess is invoked with
the correct command string.
"""

from tests.cli.a.s import prepare_root_folder


# Unit test classes  ###########################################################


class TestCliCommand:  # =======================================================

    def test_command_invoked(
        self, mock_run, mock_tmp_path, mock_tmp_path_factory, cli_command
    ):
        command = cli_command + "a code "
        prepare_root_folder(
            tmp_path_factory=mock_tmp_path_factory,
            command=command,
            folder_name="test_folder",
        )
        mock_run.assert_called_once()
        called_command = mock_run.call_args[0][0]
        assert "a code" in called_command
        assert str(mock_tmp_path) in called_command

import pytest

from tests.cli.a.s import prepare_root_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_plugin_folder(tmp_path_factory, cli_claude_command):
    command = cli_claude_command + "plugin "
    root = prepare_root_folder(tmp_path_factory, command, "plugin")
    return root / "kaye"

import pytest

from tests.cli.a.s import prepare_root_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_claude_folder(tmp_path_factory, cli_claude_command):
    command = cli_claude_command + "code "
    return prepare_root_folder(tmp_path_factory, command, "claude_code")


@pytest.fixture(scope="session")
def testee_plugin_folder(testee_claude_folder):
    return testee_claude_folder / "plugins" / "kaye-engine"

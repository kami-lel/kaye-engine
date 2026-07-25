import pytest

from tests.cli.a.s import prepare_root_folder

# Pytest fixtures  #############################################################

_MARKETPLACE_NAME = "kaye_marketplace"


@pytest.fixture(scope="session")
def testee_claude_folder(tmp_path_factory, cli_claude_command):
    command = cli_claude_command + "vs-code-extension "
    return prepare_root_folder(tmp_path_factory, command, "vs_code_extension")


@pytest.fixture(scope="session")
def testee_marketplace_folder(testee_claude_folder):
    return testee_claude_folder / _MARKETPLACE_NAME


@pytest.fixture(scope="session")
def testee_plugin_folder(testee_marketplace_folder):
    return testee_marketplace_folder / "plugins" / "kaye-engine"

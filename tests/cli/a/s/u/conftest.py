import pytest

from tests.cli.a.s import prepare_root_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_skills_folder(tmp_path_factory, cli_command):
    command = cli_command + "claude skill "
    return prepare_root_folder(tmp_path_factory, command, "skills")

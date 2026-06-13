import pytest

from tests.cli.s import prepare_root_folder

# TODO alts tests

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_skills_folder(tmp_path_factory, cli_command):
    command = cli_command + "skill update "
    return prepare_root_folder(tmp_path_factory, command, "skills")

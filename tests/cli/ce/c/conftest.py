import subprocess

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def ce_command():
    return "python3 -m kaye continue "


@pytest.fixture(scope="session")
def testee_local_config_folder(tmp_path_factory, ce_command):
    folder = tmp_path_factory.mktemp("testee_local_config_folder")

    # Execute continue export command with folder path
    cmd = ce_command + str(folder)
    subprocess.run(cmd, shell=True, check=True)

    return folder


@pytest.fixture(scope="session")
def testee_rules_folder(testee_local_config_folder):
    rules_folder = testee_local_config_folder / "rules"
    return rules_folder

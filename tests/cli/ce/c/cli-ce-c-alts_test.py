"""
cli-ce-c-alts_test.py

Unit Tests (using pytest) for:

Python CLI command ``continue`` create alternatives commands
"""

import subprocess

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_local_config_folder_alt(tmp_path_factory, ce_c_command):
    folder = tmp_path_factory.mktemp("testee_local_config_folder")

    # Execute continue export command with folder path
    cmd = ce_c_command + str(folder)
    subprocess.run(cmd, shell=True, check=True)

    return folder


@pytest.fixture(scope="session")
def testee_rules_folder_alt(testee_local_config_folder_alt):
    rules_folder = testee_local_config_folder_alt / "rules"
    return rules_folder


class TestAlt:

    def test_exits(_, testee_rules_folder_alt):
        assert testee_rules_folder_alt.exists()

    def test_is_dir(_, testee_rules_folder_alt):
        assert testee_rules_folder_alt.is_dir()

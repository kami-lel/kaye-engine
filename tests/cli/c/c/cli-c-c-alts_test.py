"""
cli-c-c-alts_test.py

Unit Tests (using pytest) for:

Python CLI command ``continue`` create alternatives commands
"""

import pytest


from tests.cli.c.c import prepare_local_config_folder
from tests.cli import *  # noqa: F401, F403

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_alt1(tmp_path_factory, cli_command):
    return prepare_local_config_folder(
        tmp_path_factory=tmp_path_factory,
        command=cli_command + "continue c ",
        folder_name="local_config_folder_alt1",
    )


@pytest.fixture(scope="class")
def testee_alt2(tmp_path_factory, cli_command):
    return prepare_local_config_folder(
        tmp_path_factory=tmp_path_factory,
        command=cli_command + "c config ",
        folder_name="local_config_folder_alt2",
    )


@pytest.fixture(scope="class")
def testee_alt3(tmp_path_factory, cli_command):
    return prepare_local_config_folder(
        tmp_path_factory=tmp_path_factory,
        command=cli_command + "c c ",
        folder_name="local_config_folder_alt3",
    )


# Pytest unit tests  ###########################################################


class TestAlt1:  # =============================================================

    def test_rules_exist(_, testee_alt1):
        _, rules_folder = testee_alt1
        assert rules_folder.exists()

    def test_rules_is_dir(_, testee_alt1):
        _, rules_folder = testee_alt1
        assert rules_folder.is_dir()

    def test_entries(_, testee_alt1):
        _, rules_folder = testee_alt1
        for v in MD_FILENAME2SKILL_NAME.values():
            assert (rules_folder / f"{v}.md").exists()


class TestAlt2:  # =============================================================

    def test_rules_exist(_, testee_alt2):
        _, rules_folder = testee_alt2
        assert rules_folder.exists()

    def test_rules_is_dir(_, testee_alt2):
        _, rules_folder = testee_alt2
        assert rules_folder.is_dir()

    def test_entries(_, testee_alt2):
        _, rules_folder = testee_alt2
        for v in MD_FILENAME2SKILL_NAME.values():
            assert (rules_folder / f"{v}.md").exists()


class TestAlt3:  # =============================================================

    def test_rules_exist(_, testee_alt3):
        _, rules_folder = testee_alt3
        assert rules_folder.exists()

    def test_rules_is_dir(_, testee_alt3):
        _, rules_folder = testee_alt3
        assert rules_folder.is_dir()

    def test_entries(_, testee_alt3):
        _, rules_folder = testee_alt3
        for v in MD_FILENAME2SKILL_NAME.values():
            assert (rules_folder / f"{v}.md").exists()

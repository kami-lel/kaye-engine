"""
cli-ce-c-alts_test.py

Unit Tests (using pytest) for:

Python CLI command ``continue`` create alternatives commands
"""

import pytest


from tests.cli.ce.c import RULE_FILES, prepare_local_config_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_alt1(tmp_path_factory):
    return prepare_local_config_folder(
        tmp_path_factory=tmp_path_factory,
        command="python3 -m kaye c ",
        folder_name="local_config_folder_alt1",
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
        for v in RULE_FILES:
            assert (rules_folder / v).exists()


# TODO more alternative commands form

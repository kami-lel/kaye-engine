"""
cli-a-s-alts_test.py

Unit Tests (using pytest) for:

Python CLI command ``claude skill`` alternative commands
"""

import pytest


from tests.cli.a.s import prepare_root_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_alt1(tmp_path_factory, cli_command):
    return prepare_root_folder(
        tmp_path_factory=tmp_path_factory,
        command=cli_command + "claude s ",
        folder_name="skills_alt1",
    )


@pytest.fixture(scope="class")
def testee_alt2(tmp_path_factory, cli_command):
    return prepare_root_folder(
        tmp_path_factory=tmp_path_factory,
        command=cli_command + "a skill ",
        folder_name="skills_alt2",
    )


@pytest.fixture(scope="class")
def testee_alt3(tmp_path_factory, cli_command):
    return prepare_root_folder(
        tmp_path_factory=tmp_path_factory,
        command=cli_command + "a s ",
        folder_name="skills_alt3",
    )


# Pytest unit tests  ###########################################################


class TestAlt1:  # =============================================================

    def test_skills_exist(_, testee_alt1):
        assert testee_alt1.exists()

    def test_skills_is_dir(_, testee_alt1):
        assert testee_alt1.is_dir()

    def test_entries(_, testee_alt1):
        for skill_dir in testee_alt1.iterdir():
            if skill_dir.is_dir():
                assert (skill_dir / "SKILL.md").exists()


class TestAlt2:  # =============================================================

    def test_skills_exist(_, testee_alt2):
        assert testee_alt2.exists()

    def test_skills_is_dir(_, testee_alt2):
        assert testee_alt2.is_dir()

    def test_entries(_, testee_alt2):
        for skill_dir in testee_alt2.iterdir():
            if skill_dir.is_dir():
                assert (skill_dir / "SKILL.md").exists()


class TestAlt3:  # =============================================================

    def test_skills_exist(_, testee_alt3):
        assert testee_alt3.exists()

    def test_skills_is_dir(_, testee_alt3):
        assert testee_alt3.is_dir()

    def test_entries(_, testee_alt3):
        for skill_dir in testee_alt3.iterdir():
            if skill_dir.is_dir():
                assert (skill_dir / "SKILL.md").exists()

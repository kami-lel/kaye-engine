"""
cli-a-s-alts-a-skill_test.py

Unit Tests (using pytest) for:

CLI alias: ``python -m kaye a skill`` (alias for claude, full command)
Verifies all skill SKILL.md files are exported.
"""

import pytest

from tests.cli.a import ALL_CLAUDE_SKILL_NAMES
from tests.cli.a.s import prepare_root_folder


# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_skills_folder(tmp_path_factory, cli_command):
    command = cli_command + "a skill "
    return prepare_root_folder(
        tmp_path_factory=tmp_path_factory,
        command=command,
        folder_name="skills_a_skill",
    )


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_skills_folder_exists(self, testee_skills_folder):
        assert testee_skills_folder.exists()

    def test_skills_folder_is_dir(self, testee_skills_folder):
        assert testee_skills_folder.is_dir()


class TestSkillFiles:  # =======================================================

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_exists(self, testee_skills_folder, skill_name):
        skill_file = testee_skills_folder / skill_name / "SKILL.md"
        assert skill_file.exists(), f"Missing {skill_name}/SKILL.md"

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_is_file(self, testee_skills_folder, skill_name):
        skill_file = testee_skills_folder / skill_name / "SKILL.md"
        assert skill_file.is_file(), f"{skill_name}/SKILL.md is not a file"

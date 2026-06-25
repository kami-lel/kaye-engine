"""
cli-a-c-skill_files_test.py

Unit Tests (using pytest) for:

``python -m kaye claude code`` — verifies all skill SKILL.md files are
exported under the plugin's ``skills/`` subfolder.
"""

import pytest

from tests.cli.a import ALL_CLAUDE_SKILL_NAMES


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_plugin_folder_exists(self, testee_plugin_folder):
        assert testee_plugin_folder.exists()

    def test_plugin_folder_is_dir(self, testee_plugin_folder):
        assert testee_plugin_folder.is_dir()

    def test_skills_subfolder_exists(self, testee_plugin_folder):
        assert (testee_plugin_folder / "skills").exists()

    def test_skills_subfolder_is_dir(self, testee_plugin_folder):
        assert (testee_plugin_folder / "skills").is_dir()


class TestSkillFiles:  # =======================================================

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_exists(self, testee_plugin_folder, skill_name):
        skill_file = testee_plugin_folder / "skills" / skill_name / "SKILL.md"
        assert skill_file.exists(), f"Missing skills/{skill_name}/SKILL.md"

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_is_file(self, testee_plugin_folder, skill_name):
        skill_file = testee_plugin_folder / "skills" / skill_name / "SKILL.md"
        assert skill_file.is_file(), (
            f"skills/{skill_name}/SKILL.md is not a file"
        )

"""
cli-a-p-alts-a-plugin_test.py

Unit Tests (using pytest) for:

CLI alias: ``python -m kaye a plugin`` — verifies all skill SKILL.md files
and the plugin.json manifest are exported.
"""

import pytest

from tests.cli.a import ALL_CLAUDE_SKILL_NAMES
from tests.cli.a.s import prepare_root_folder


# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_plugin_folder(tmp_path_factory, cli_command):
    command = cli_command + "a plugin "
    root = prepare_root_folder(tmp_path_factory, command, "plugin_a_plugin")
    return root / "kaye"


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_plugin_folder_exists(self, testee_plugin_folder):
        assert testee_plugin_folder.exists()

    def test_plugin_folder_is_dir(self, testee_plugin_folder):
        assert testee_plugin_folder.is_dir()


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


class TestPluginJson:  # =======================================================

    def test_plugin_json_exists(self, testee_plugin_folder):
        assert (testee_plugin_folder / ".claude-plugin" / "plugin.json").exists()

    def test_plugin_json_is_file(self, testee_plugin_folder):
        assert (testee_plugin_folder / ".claude-plugin" / "plugin.json").is_file()

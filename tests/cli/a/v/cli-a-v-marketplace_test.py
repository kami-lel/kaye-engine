"""
cli-a-v-marketplace_test.py

Unit Tests (using pytest) for:

``python -m kaye claude vs-code-extension`` — verifies a kaye_marketplace/
folder is created inside the Claude folder with the marketplace manifest,
plugin.json, and all skill SKILL.md files.
"""

import pytest

from tests.cli.a import ALL_CLAUDE_SKILL_NAMES


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_marketplace_folder_exists(self, testee_marketplace_folder):
        assert testee_marketplace_folder.exists()

    def test_marketplace_folder_is_dir(self, testee_marketplace_folder):
        assert testee_marketplace_folder.is_dir()


class TestMarketplaceJson:  # ==================================================

    def test_marketplace_json_exists(self, testee_marketplace_folder):
        path = testee_marketplace_folder / ".claude-plugin" / "marketplace.json"
        assert path.exists()

    def test_marketplace_json_is_file(self, testee_marketplace_folder):
        path = testee_marketplace_folder / ".claude-plugin" / "marketplace.json"
        assert path.is_file()


class TestPluginJson:  # =======================================================

    def test_plugin_json_exists(self, testee_plugin_folder):
        assert (testee_plugin_folder / ".claude-plugin" / "plugin.json").exists()

    def test_plugin_json_is_file(self, testee_plugin_folder):
        assert (testee_plugin_folder / ".claude-plugin" / "plugin.json").is_file()


class TestSkillFiles:  # =======================================================

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_exists(self, testee_plugin_folder, skill_name):
        skill_file = testee_plugin_folder / "skills" / skill_name / "SKILL.md"
        assert skill_file.exists(), (
            f"Missing plugins/kaye/skills/{skill_name}/SKILL.md"
        )

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_is_file(self, testee_plugin_folder, skill_name):
        skill_file = testee_plugin_folder / "skills" / skill_name / "SKILL.md"
        assert skill_file.is_file(), (
            f"plugins/kaye/skills/{skill_name}/SKILL.md is not a file"
        )

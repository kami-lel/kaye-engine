"""
cli-a-m-files_test.py

Unit Tests (using pytest) for:

``python -m kaye claude marketplace`` — verifies all skill SKILL.md files,
the plugin.json manifest, and the marketplace.json manifest are exported
in the correct locations.
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

    def test_plugin_json_exists(self, testee_marketplace_folder):
        path = (
            testee_marketplace_folder
            / "plugins" / "kaye-engine" / ".claude-plugin" / "plugin.json"
        )
        assert path.exists()

    def test_plugin_json_is_file(self, testee_marketplace_folder):
        path = (
            testee_marketplace_folder
            / "plugins" / "kaye-engine" / ".claude-plugin" / "plugin.json"
        )
        assert path.is_file()


class TestSkillFiles:  # =======================================================

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_exists(self, testee_marketplace_folder, skill_name):
        skill_file = (
            testee_marketplace_folder
            / "plugins" / "kaye-engine" / "skills" / skill_name / "SKILL.md"
        )
        assert skill_file.exists(), (
            f"Missing plugins/kaye-engine/skills/{skill_name}/SKILL.md"
        )

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_skill_file_is_file(self, testee_marketplace_folder, skill_name):
        skill_file = (
            testee_marketplace_folder
            / "plugins" / "kaye-engine" / "skills" / skill_name / "SKILL.md"
        )
        assert skill_file.is_file(), (
            f"plugins/kaye-engine/skills/{skill_name}/SKILL.md is not a file"
        )

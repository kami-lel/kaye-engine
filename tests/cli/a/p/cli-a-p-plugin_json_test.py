"""
cli-a-p-plugin_json_test.py

Unit Tests (using pytest) for:

``python -m kaye claude plugin`` — verifies the plugin.json manifest is
exported under ``.claude-plugin/`` with the expected content.
"""

import json

import pytest


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_plugin_json_path(testee_plugin_folder):
    return testee_plugin_folder / ".claude-plugin" / "plugin.json"


@pytest.fixture(scope="session")
def testee_plugin_json(testee_plugin_json_path):
    with open(testee_plugin_json_path, encoding="utf-8") as f:
        return json.load(f)


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_plugin_json_exists(self, testee_plugin_json_path):
        assert testee_plugin_json_path.exists()

    def test_plugin_json_is_file(self, testee_plugin_json_path):
        assert testee_plugin_json_path.is_file()


class TestContent:  # ==========================================================

    def test_name(self, testee_plugin_json):
        assert testee_plugin_json["name"] == "kaye-engine"

    def test_display_name(self, testee_plugin_json):
        assert (
            testee_plugin_json["displayName"]
            == "Prompt Engineering Project Kaye Engine"
        )

    def test_version(self, testee_plugin_json):
        assert "version" in testee_plugin_json

    def test_description(self, testee_plugin_json):
        assert "description" in testee_plugin_json
        assert testee_plugin_json["description"]

    def test_author_name(self, testee_plugin_json):
        assert testee_plugin_json["author"]["name"] == "kamiLeL"

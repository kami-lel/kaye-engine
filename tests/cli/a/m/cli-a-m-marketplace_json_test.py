"""
cli-a-m-marketplace_json_test.py

Unit Tests (using pytest) for:

``python -m kaye claude marketplace`` — verifies the marketplace.json manifest
contains the expected content.
"""

import json

import pytest


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_marketplace_json_path(testee_marketplace_folder):
    return testee_marketplace_folder / ".claude-plugin" / "marketplace.json"


@pytest.fixture(scope="session")
def testee_marketplace_json(testee_marketplace_json_path):
    with open(testee_marketplace_json_path, encoding="utf-8") as f:
        return json.load(f)


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_marketplace_json_exists(self, testee_marketplace_json_path):
        assert testee_marketplace_json_path.exists()

    def test_marketplace_json_is_file(self, testee_marketplace_json_path):
        assert testee_marketplace_json_path.is_file()


class TestContent:  # ==========================================================

    def test_schema(self, testee_marketplace_json):
        assert "$schema" in testee_marketplace_json

    def test_name(self, testee_marketplace_json):
        assert testee_marketplace_json["name"] == "kaye-engine"

    def test_version(self, testee_marketplace_json):
        assert "version" in testee_marketplace_json

    def test_description(self, testee_marketplace_json):
        assert "description" in testee_marketplace_json
        assert testee_marketplace_json["description"]

    def test_owner_name(self, testee_marketplace_json):
        assert testee_marketplace_json["owner"]["name"] == "kamiLeL"

    def test_plugins_list(self, testee_marketplace_json):
        assert "plugins" in testee_marketplace_json
        assert len(testee_marketplace_json["plugins"]) > 0

    def test_plugin_source(self, testee_marketplace_json):
        plugin = testee_marketplace_json["plugins"][0]
        assert plugin["source"] == "./plugins/kaye-engine"

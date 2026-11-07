"""
manifest_test.py

Unit Tests (using pytest) for:

- ManifestPluginJson deed logging
- MarketplaceJson deed logging
- skip of an unchanged manifest, overwrite of a changed one
"""

import logging
import os

import kamilog

from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.marketplace.manifest import MarketplaceJson
from kaye_engine.cli.claude.plugin.manifest import ManifestPluginJson


# pytest  ######################################################################
class TestManifestPluginJson:

    def test_logs_create_dir_then_create(_, tmp_path, caplog):
        with caplog.at_level(logging.INFO, logger=LOGGER_CLAUDE_NAME):
            with ManifestPluginJson(tmp_path / "plugin") as manifest:
                manifest.name = "kaye"

        messages = [rec.message for rec in caplog.records]
        assert messages[0].startswith("create dir ")
        assert messages[1].startswith("create ")
        assert messages[1].endswith("plugin.json")

    def test_existing_dir_logs_only_create(_, tmp_path, caplog):
        (tmp_path / ".claude-plugin").mkdir()
        with caplog.at_level(logging.INFO, logger=LOGGER_CLAUDE_NAME):
            with ManifestPluginJson(tmp_path) as manifest:
                manifest.name = "kaye"

        assert [rec.message.split()[0] for rec in caplog.records] == ["create"]


class TestMarketplaceJson:

    def test_logs_create_dir_then_create(_, tmp_path, caplog):
        with caplog.at_level(logging.INFO, logger=LOGGER_CLAUDE_NAME):
            with MarketplaceJson(tmp_path / "market") as market:
                market.name = "kaye"

        messages = [rec.message for rec in caplog.records]
        assert messages[0].startswith("create dir ")
        assert messages[1].startswith("create ")
        assert messages[1].endswith("marketplace.json")


class TestSkipUnchanged:

    def test_plugin_manifest_skips_identical_rewrite(_, tmp_path, caplog):
        with ManifestPluginJson(tmp_path) as manifest:
            manifest.name = "kaye"
        path = tmp_path / ".claude-plugin" / "plugin.json"
        os.utime(path, (1_000_000, 1_000_000))
        caplog.clear()

        with caplog.at_level(logging.DEBUG, logger=LOGGER_CLAUDE_NAME):
            with ManifestPluginJson(tmp_path) as manifest:
                manifest.name = "kaye"
        assert path.stat().st_mtime == 1_000_000
        assert [rec.levelno for rec in caplog.records] == [kamilog.SKIP]

    def test_plugin_manifest_overwrites_changed_content(_, tmp_path):
        with ManifestPluginJson(tmp_path) as manifest:
            manifest.name = "kaye"
        with ManifestPluginJson(tmp_path) as manifest:
            manifest.name = "ria"

        path = tmp_path / ".claude-plugin" / "plugin.json"
        assert '"ria"' in path.read_text(encoding="utf-8")

    def test_marketplace_skips_identical_rewrite(_, tmp_path, caplog):
        with MarketplaceJson(tmp_path) as market:
            market.name = "kaye"
        path = tmp_path / ".claude-plugin" / "marketplace.json"
        os.utime(path, (1_000_000, 1_000_000))
        caplog.clear()

        with caplog.at_level(logging.DEBUG, logger=LOGGER_CLAUDE_NAME):
            with MarketplaceJson(tmp_path) as market:
                market.name = "kaye"
        assert path.stat().st_mtime == 1_000_000
        assert [rec.levelno for rec in caplog.records] == [kamilog.SKIP]

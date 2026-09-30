"""
manifest_test.py

Unit Tests (using pytest) for:

- ManifestPluginJson deed logging
- MarketplaceJson deed logging
"""

import logging

from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.marketplace.manifest import MarketplaceJson
from kaye_engine.cli.claude.plugin.manifest import ManifestPluginJson


# pytest  ######################################################################
class TestManifestPluginJson:

    def test_logs_create_dir_then_save(_, tmp_path, caplog):
        with caplog.at_level(logging.INFO, logger=LOGGER_CLAUDE_NAME):
            with ManifestPluginJson(tmp_path / "plugin") as manifest:
                manifest.name = "kaye"

        messages = [rec.message for rec in caplog.records]
        assert messages[0].startswith("create dir ")
        assert messages[1].startswith("save ")
        assert messages[1].endswith("plugin.json")

    def test_existing_dir_logs_only_save(_, tmp_path, caplog):
        (tmp_path / ".claude-plugin").mkdir()
        with caplog.at_level(logging.INFO, logger=LOGGER_CLAUDE_NAME):
            with ManifestPluginJson(tmp_path) as manifest:
                manifest.name = "kaye"

        assert [rec.message.split()[0] for rec in caplog.records] == ["save"]


class TestMarketplaceJson:

    def test_logs_create_dir_then_save(_, tmp_path, caplog):
        with caplog.at_level(logging.INFO, logger=LOGGER_CLAUDE_NAME):
            with MarketplaceJson(tmp_path / "market") as market:
                market.name = "kaye"

        messages = [rec.message for rec in caplog.records]
        assert messages[0].startswith("create dir ")
        assert messages[1].startswith("save ")
        assert messages[1].endswith("marketplace.json")

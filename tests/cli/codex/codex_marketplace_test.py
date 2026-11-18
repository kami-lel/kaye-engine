"""
tests/cli/codex/codex_marketplace_test.py

test: ``codex marketplace`` -- catalog shape, one local entry per
consumer, plugins under ``plugins/``, the ``m`` alias
"""

import json
from argparse import ArgumentParser

from kaye_engine.cli.codex.main import register_cli_codex_parser
from kaye_engine.cli.codex.marketplace import parser as market_parser
from kaye_engine.cli.codex.marketplace.export import (
    export_codex_marketplace,
)
from kaye_engine.cli.codex.marketplace.manifest import (
    CodexMarketplace,
    CodexMarketplacePlugin,
)
from kaye_engine.cli.codex.platform import get_marketplace_display_name

from kaye_engine.repo import set_repo_name
from tests.cli.codex.codex_plugin_test import two_consumers  # noqa: F401
from tests.consumer_helper import isolated_repo


class TestStructure:

    def test_marketplace_aliases(_):
        root = ArgumentParser()
        register_cli_codex_parser(root.add_subparsers())

        for argv in (["codex", "marketplace"], ["o", "m"]):
            assert callable(root.parse_args(argv).func)

    def test_default_root_is_home(_):
        assert market_parser.DEFAULT_CODEX_MARKETPLACE_ROOT.is_absolute()


class TestHeader:

    def test_entry_is_local_with_policy_and_category(_):
        assert CodexMarketplacePlugin("kaye", "./plugins/kaye").as_dict() == {
            "name": "kaye",
            "source": {"source": "local", "path": "./plugins/kaye"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }

    def test_catalog_omits_empty_display_name(_):
        assert CodexMarketplace("m").as_dict() == {"name": "m", "plugins": []}

    def test_display_name_title_cases_kebab_name(_):
        assert get_marketplace_display_name("kaye-library-marketplace") == (
            "Kaye Library Marketplace"
        )


class TestContent:

    def test_catalog_lists_every_consumer_plugin(
        _, two_consumers, tmp_path  # noqa: F811
    ):
        with isolated_repo():
            set_repo_name("pkg-one")
            path = export_codex_marketplace(tmp_path)

        assert path == (
            tmp_path / ".agents" / "plugins" / "marketplace.json"
        ).resolve()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["name"] == "pkg-one"
        assert data["interface"] == {"displayName": "Pkg One"}
        assert [p["source"]["path"] for p in data["plugins"]] == [
            "./plugins/pkg-one",
            "./plugins/pkg-two",
        ]
        for name in ("pkg-one", "pkg-two"):
            plugin = tmp_path / "plugins" / name
            assert (plugin / ".codex-plugin" / "plugin.json").is_file()
            assert (plugin / "plugin.json").is_file()

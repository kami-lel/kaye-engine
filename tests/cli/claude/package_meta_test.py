"""
package_meta_test.py

Unit Tests (using pytest) for:

- read_package_meta keywords
- get_plugin_keywords
- plugin and marketplace manifests carrying them
"""

import json
from unittest.mock import patch

from kaye_engine.cli.claude import package_meta
from kaye_engine.cli.claude.package_meta import (
    PackageMeta,
    get_plugin_keywords,
    read_package_meta,
)
from kaye_engine.cli.claude.plugin.export_folder import (
    export_plugin_as_folder,
)
from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.consumer_helper import isolated_consumers
from tests.corpus_helper import load_corpus_from_sources


class _KeywordMetadata(_FakeMetadata):
    def get(self, key, default=None):
        if key == "Keywords":
            return "recipes, kitchen ,"
        return super().get(key, default)


def _meta(keywords=()):
    return PackageMeta("1", "s", "a", "e", "h", "r", keywords)


class TestReadPackageMeta:

    def test_splits_the_distribution_keywords(_):
        with patch.object(package_meta, "metadata") as meta_mock:
            meta_mock.side_effect = lambda name: _KeywordMetadata(name)

            meta = read_package_meta("pkg")

        assert meta.keywords == ("recipes", "kitchen")

    def test_no_keywords_gives_an_empty_tuple(_):
        with patch.object(package_meta, "metadata") as meta_mock:
            meta_mock.side_effect = lambda name: _FakeMetadata(name)

            meta = read_package_meta("pkg")

        assert meta.keywords == ()


class TestGetPluginKeywords:

    def test_uses_own_keywords_then_the_plugin_name(_):
        assert get_plugin_keywords(_meta(("a", "b")), "pkg") == [
            "a",
            "b",
            "pkg",
        ]

    def test_falls_back_to_generic_defaults_without_persona(_):
        keywords = get_plugin_keywords(_meta(), "pkg")

        assert keywords == ["prompt-engineering", "agent", "pkg"]
        assert "persona" not in keywords


class TestPluginManifest:

    def test_plugin_json_carries_no_persona_keyword(_, tmp_path):
        clear_corpus_tree()
        load_corpus_from_sources(["# R\n"])
        entry = BlueprintRegistry(
            canonical_name="s", blueprint=create_blueprint(), consumer="pkg"
        )
        with isolated_consumers(), patch.dict(
            exportable_registry, {"s": entry}, clear=True
        ), patch.object(package_meta, "metadata") as meta_mock:
            consumer = register_consumer("Package", "pkg", "1.0.0")
            meta_mock.side_effect = lambda name: _FakeMetadata(name)

            root = export_plugin_as_folder(tmp_path, consumer)
        clear_corpus_tree()

        data = json.loads(
            (root / ".claude-plugin" / "plugin.json").read_text()
        )
        assert "persona" not in data["keywords"]
        assert data["keywords"][-1] == "pkg"

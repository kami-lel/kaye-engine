"""
tests/cli/codex/codex_plugin_test.py

test: ``codex plugin`` -- both Codex manifests, one plugin per consumer,
the ``codex``/``o`` group and its ``plugin``/``p`` subcommand
"""

import json
from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.codex.main import register_cli_codex_parser
from kaye_engine.cli.codex.plugin import parser as plugin_parser
from kaye_engine.cli.codex.plugin.export import (
    export_codex_plugins_as_folders,
)
from kaye_engine.cli.codex.plugin.manifest import CodexPluginManifest
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.consumer_helper import isolated_consumers
from tests.corpus_helper import load_corpus_from_sources


class _FakeMetadata:
    def __init__(self, name):
        self._name = name

    def get(self, key, default=None):
        if key == "Author-email":
            return "Author {0} <{0}@example.com>".format(self._name)
        return default

    def get_all(self, _):
        return None

    def __getitem__(self, key):
        return "0.0.1" if key == "Version" else "summary of " + self._name


@pytest.fixture
def two_consumers():
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    entries = {
        name: BlueprintRegistry(
            canonical_name=name, blueprint=create_blueprint(), consumer=owner
        )
        for name, owner in (("one-skill", "pkg-one"), ("two-skill", "pkg-two"))
    }
    with isolated_consumers(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock:
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        meta_mock.side_effect = _FakeMetadata
        yield
    clear_corpus_tree()


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestStructure:

    def test_group_and_plugin_aliases(_):
        root = ArgumentParser()
        register_cli_codex_parser(root.add_subparsers())

        for argv in (["codex", "plugin"], ["o", "p"]):
            assert callable(root.parse_args(argv).func)

    def test_plugin_default_folder_is_home_plugins(_):
        assert plugin_parser.DEFAULT_CODEX_PLUGINS_FOLDER.name == "plugins"


class TestHeader:

    def test_empty_fields_are_omitted(_):
        manifest = CodexPluginManifest(name="kaye")

        assert manifest.root_dict() == {
            "$schema": CodexPluginManifest.SCHEMA,
            "name": "kaye",
        }
        assert manifest.codex_dict() == {
            "name": "kaye",
            "skills": "./skills/",
            "interface": {"category": "Productivity"},
        }

    def test_codex_manifest_carries_interface_root_does_not(_):
        manifest = CodexPluginManifest(
            name="kaye",
            version="1.0.0",
            description="desc",
            display_name="Kaye",
            author_name="Ann",
            author_email="ann@example.com",
        )

        assert "interface" not in manifest.root_dict()
        assert "extensions" not in manifest.root_dict()
        assert manifest.codex_dict()["interface"] == {
            "displayName": "Kaye",
            "shortDescription": "desc",
            "developerName": "Ann",
            "category": "Productivity",
        }
        assert manifest.root_dict()["author"] == {
            "name": "Ann",
            "email": "ann@example.com",
        }


class TestContent:

    def test_one_plugin_per_consumer_w_both_manifests(
        _, two_consumers, tmp_path
    ):
        roots = export_codex_plugins_as_folders(tmp_path)

        assert [r.name for r in roots] == ["pkg-one", "pkg-two"]
        root = _read(tmp_path / "pkg-two" / "plugin.json")
        codex = _read(tmp_path / "pkg-two" / ".codex-plugin" / "plugin.json")
        assert root["name"] == codex["name"] == "pkg-two"
        assert root["version"] == "2.2.0"
        assert codex["interface"]["displayName"] == "Package Two"
        assert [p.name for p in (tmp_path / "pkg-two" / "skills").iterdir()] == [
            "two-skill"
        ]

    def test_consumer_name_narrows_to_one_plugin(_, two_consumers, tmp_path):
        export_codex_plugins_as_folders(tmp_path, consumer_name="pkg-one")

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-one"]

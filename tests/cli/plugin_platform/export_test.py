"""
tests/cli/plugin_platform/export_test.py

test: the template exporters drive any ``PluginPlatform`` through its
hooks -- manifest per plugin, one entry per consumer, one marketplace
"""

from unittest.mock import patch

import pytest
from kaye_engine.cli.plugin_platform import export, package_meta
from kaye_engine.cli.plugin_platform.platform import PluginPlatform
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
        return default

    def get_all(self, _):
        return None

    def __getitem__(self, key):
        return "0.0.1" if key == "Version" else "summary of " + self._name


class _RecordingPlatform(PluginPlatform):
    name = "fake"
    default_surface = ("claude",)
    logger_name = "kaye-engine.fake"

    def __init__(self):
        self.calls = []

    def write_plugin_manifest(self, plugin_root, consumer, meta):
        self.calls.append(("manifest", plugin_root.name, meta.summary))

    def build_marketplace_entry(self, consumer, meta, source):
        return (consumer.canonical_name, source)

    def write_marketplace_manifest(self, root, name, entries, engine_meta):
        self.calls.append(("market", name, list(entries)))
        return root / "fake.json"


@pytest.fixture(autouse=True)
def _two_consumers():
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


class TestStructure:

    def test_platform_is_abstract(_):
        with pytest.raises(TypeError):
            PluginPlatform()  # pylint: disable=abstract-class-instantiated


class TestContent:

    def test_plugin_folder_calls_manifest_hook_and_writes_skills(
        _, tmp_path
    ):
        platform = _RecordingPlatform()
        root = export.export_plugins_as_folders(
            platform, tmp_path, consumer_name="pkg-one"
        )[0]

        assert platform.calls == [("manifest", "pkg-one", "summary of pkg-one")]
        assert [p.name for p in (root / "skills").iterdir()] == ["one-skill"]

    def test_marketplace_lists_every_consumer_under_plugins_dir(
        _, tmp_path
    ):
        platform = _RecordingPlatform()
        path = export.export_marketplace(
            platform, tmp_path, "market", plugins_dir="plugins/fake"
        )

        assert path == tmp_path / "fake.json"
        assert platform.calls[-1] == (
            "market",
            "market",
            [
                ("pkg-one", "./plugins/fake/pkg-one"),
                ("pkg-two", "./plugins/fake/pkg-two"),
            ],
        )
        assert (tmp_path / "plugins" / "fake" / "pkg-two" / "skills").is_dir()

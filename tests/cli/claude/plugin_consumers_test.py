"""
tests/cli/claude/plugin_consumers_test.py

test: one plugin per consumer -- folders, zips and the marketplace --
with 2 registered consumers, each with its own name, version and skills
"""

import json
import logging
import zipfile
from unittest.mock import patch

import kamilog
import pytest
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.marketplace.export import export_marketplace
from kaye_engine.cli.claude.plugin.export_folder import (
    export_plugins_as_folders,
)
from kaye_engine.cli.claude.plugin.export_zip import export_plugins_as_zips
from kaye_engine.cli.github_release.asset_name import (
    ASSET_DESKTOP_PLUGIN,
    get_release_asset_name,
)
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.cli.plugin_platform.consumers import (
    select_plugin_consumers,
)
from kaye_engine.deed import format_size
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.repo import set_repo_name, set_repo_version
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run
from kaye_engine.skill import LOGGER_SKILL_NAME
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.consumer_helper import isolated_consumers, isolated_repo
from tests.corpus_helper import load_corpus_from_sources


def _entry(name, consumer):
    return BlueprintRegistry(
        canonical_name=name,
        blueprint=create_blueprint(),
        consumer=consumer,
    )


@pytest.fixture(autouse=True)
def _two_consumers():
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    entries = {
        "lib-skill": _entry("lib-skill", "pkg-one"),
        "app-skill": _entry("app-skill", "pkg-two"),
        "app-other": _entry("app-other", "pkg-two"),
    }
    with isolated_consumers(), isolated_repo(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock:
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        register_consumer("Idle Package", "pkg-idle", "9.9.9")
        set_default_consumer("pkg-one")
        set_repo_name("pkg-one")
        set_repo_version("1.1.0")
        meta_mock.side_effect = lambda name: _FakeMetadata(name)
        yield
    clear_corpus_tree()


class _FakeMetadata:
    def __init__(self, name):
        self._name = name

    def get(self, key, default=None):
        if key == "Author-email":
            return "Author {0} <{0}@example.com>".format(self._name)
        return default

    def get_all(self, key):
        if key == "Project-URL":
            return [
                "homepage, https://example.com/" + self._name,
                "Repository, https://example.com/" + self._name + ".git",
            ]
        return None

    def __getitem__(self, key):
        if key == "Version":
            return "0.0.1"
        return "summary of " + self._name


def _skills(plugin_root):
    return sorted(p.name for p in (plugin_root / "skills").iterdir())


class TestSelectPluginConsumers:

    def test_no_name_selects_every_plugin_consumer(_):
        names = [c.canonical_name for c in select_plugin_consumers()]

        assert names == ["pkg-one", "pkg-two"]

    def test_name_selects_that_one_consumer(_):
        names = [c.canonical_name for c in select_plugin_consumers("pkg-two")]

        assert names == ["pkg-two"]

    def test_names_select_in_the_order_given(_):
        names = [
            c.canonical_name
            for c in select_plugin_consumers(["pkg-two", "pkg-one"])
        ]

        assert names == ["pkg-two", "pkg-one"]

    def test_repeated_name_selects_once(_):
        names = [
            c.canonical_name
            for c in select_plugin_consumers(["pkg-one", "pkg-one"])
        ]

        assert names == ["pkg-one"]

    def test_one_unknown_name_among_valid_ones_raises(_):
        with pytest.raises(ValueError, match="pkg-nope"):
            select_plugin_consumers(["pkg-one", "pkg-nope"])

    def test_unknown_name_raises_listing_valid_names(_):
        with pytest.raises(ValueError, match="pkg-one, pkg-two"):
            select_plugin_consumers("pkg-nope")

    def test_consumer_without_exportable_is_unknown(_):
        with pytest.raises(ValueError):
            select_plugin_consumers("pkg-idle")


class TestPluginFolders:

    def test_one_folder_per_consumer_holding_skills(_, tmp_path):
        export_plugins_as_folders(tmp_path)

        assert sorted(p.name for p in tmp_path.iterdir()) == [
            "pkg-one",
            "pkg-two",
        ]

    def test_each_plugin_holds_only_its_skills(_, tmp_path):
        export_plugins_as_folders(tmp_path)

        assert _skills(tmp_path / "pkg-one") == ["lib-skill"]
        assert _skills(tmp_path / "pkg-two") == ["app-other", "app-skill"]

    def test_manifest_from_own_record_and_distribution(_, tmp_path):
        export_plugins_as_folders(tmp_path)

        manifest = json.loads(
            (
                tmp_path / "pkg-two" / ".claude-plugin" / "plugin.json"
            ).read_text(encoding="utf-8")
        )
        assert manifest["name"] == "pkg-two"
        assert manifest["displayName"] == "Package Two"
        assert manifest["version"] == "2.2.0"
        assert manifest["description"] == "summary of pkg-two"
        assert manifest["homepage"] == "https://example.com/pkg-two"

    def test_skill_md_carries_consumer_version(_, tmp_path):
        export_plugins_as_folders(tmp_path)

        text = (tmp_path / "pkg-one" / "skills" / "lib-skill" / "SKILL.md")
        assert "1.1.0" in text.read_text(encoding="utf-8")


class TestConsumerFilter:

    def test_folders_for_one_consumer_only(_, tmp_path):
        export_plugins_as_folders(tmp_path, consumer_name="pkg-two")

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-two"]

    def test_zip_for_one_consumer_only(_, tmp_path):
        count = export_plugins_as_zips(tmp_path, consumer_name="pkg-one")

        assert count == 1
        assert [p.name for p in tmp_path.iterdir()] == ["pkg-one-1.1.0-claude-desktop-plugin.zip"]

    def test_unknown_name_raises_and_writes_nothing(_, tmp_path):
        with pytest.raises(ValueError):
            export_plugins_as_zips(tmp_path, consumer_name="pkg-nope")
        with pytest.raises(ValueError):
            export_plugins_as_folders(tmp_path, consumer_name="pkg-nope")

        assert list(tmp_path.iterdir()) == []


class TestPluginZips:

    def test_zips_named_as_release_assets(_, tmp_path):
        export_plugins_as_zips(tmp_path)

        assert sorted(p.name for p in tmp_path.iterdir()) == sorted(
            [
                get_release_asset_name(
                    ASSET_DESKTOP_PLUGIN, consumer=name
                )
                for name in ("pkg-one", "pkg-two")
            ]
        )
        assert (tmp_path / "pkg-one-1.1.0-claude-desktop-plugin.zip").exists()
        assert (
            tmp_path / "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip"
        ).exists()

    def test_no_version_drops_version_from_names(_, tmp_path):
        export_plugins_as_zips(tmp_path, includes_version=False)

        assert sorted(p.name for p in tmp_path.iterdir()) == sorted(
            [
                "pkg-one-claude-desktop-plugin.zip",
                "pkg-one-claude-desktop-plugin-pkg-two.zip",
            ]
        )

    def test_zip_holds_only_own_skills(_, tmp_path):
        export_plugins_as_zips(tmp_path)

        with zipfile.ZipFile(tmp_path / "pkg-one-1.1.0-claude-desktop-plugin.zip") as archive:
            names = archive.namelist()
        assert any(n.startswith("skills/lib-skill/") for n in names)
        assert not any("app-skill" in n for n in names)


def _capture(caplog, level):
    for name in (LOGGER_CLAUDE_NAME, LOGGER_SKILL_NAME):
        caplog.set_level(level, logger=name)


class TestPluginZipOutput:

    def test_default_level_shows_a_result_line_per_plugin(
        _, tmp_path, caplog
    ):
        _capture(caplog, kamilog.DONE)
        export_plugins_as_zips(tmp_path)

        assert [r.message for r in caplog.records] == [
            "export plugin (1 skill, {}): {}".format(
                _size_of(tmp_path / "pkg-one-1.1.0-claude-desktop-plugin.zip"),
                tmp_path / "pkg-one-1.1.0-claude-desktop-plugin.zip",
            ),
            "export plugin (2 skills, {}): {}".format(
                _size_of(tmp_path / "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip"),
                tmp_path / "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip",
            ),
        ]

    def test_info_level_hides_inner_per_file_deeds(_, tmp_path, caplog):
        _capture(caplog, logging.INFO)
        export_plugins_as_zips(tmp_path)

        text = caplog.text
        assert "SKILL.md" not in text
        assert "plugin.json" not in text
        assert "-> " not in text

    def test_debug_level_lists_archive_entries(_, tmp_path, caplog):
        _capture(caplog, logging.DEBUG)
        export_plugins_as_zips(tmp_path)

        assert "  skills/lib-skill/SKILL.md" in caplog.text
        assert "pkg-one-1.1.0-claude-desktop-plugin.zip: " in caplog.text

    def test_debug_level_separates_scratch_from_publish(
        _, tmp_path, caplog
    ):
        _capture(caplog, logging.DEBUG)
        export_plugins_as_zips(tmp_path)

        records = caplog.records
        assert any(
            r.levelno == kamilog.ENTER
            and r.message.startswith("build plugin in tmp")
            for r in records
        )
        assert any(
            r.levelno == kamilog.ENTER
            and r.message.startswith("publish plugin")
            for r in records
        )
        packs = [r for r in records if r.message.startswith("pack <tmp>")]
        assert packs
        assert all(r.badges == ("tmp",) for r in packs)
        moves = [r for r in records if r.message.startswith("move <tmp>")]
        assert moves
        assert all(r.badges == ("mv",) for r in moves)
        assert all(r.levelno == logging.DEBUG for r in moves)

    def test_info_level_shows_one_tmp_summary_per_plugin(_, tmp_path, caplog):
        _capture(caplog, logging.INFO)
        export_plugins_as_zips(tmp_path)

        summaries = [
            r for r in caplog.records if r.message.startswith("build plugin")
        ]
        assert len(summaries) == 2
        assert all(r.badges == ("tmp",) for r in summaries)

    def test_returns_zip_count(_, tmp_path):
        assert export_plugins_as_zips(tmp_path) == 2

    def test_dry_run_reports_size_na_and_writes_nothing(_, tmp_path, caplog):
        enable_dry_run()
        try:
            _capture(caplog, kamilog.DONE)
            destination = tmp_path / "out"
            export_plugins_as_zips(destination)
        finally:
            disable_dry_run()

        assert not destination.exists()
        assert (
            "export plugin (1 skill, size n/a): {}".format(
                destination / "pkg-one-1.1.0-claude-desktop-plugin.zip"
            )
            in caplog.text
        )


def _size_of(path):
    return format_size(path.stat().st_size)


class TestMarketplace:

    @pytest.fixture(autouse=True)
    def _repo_name(_):
        with isolated_repo():
            set_repo_name("pkg-one")
            yield

    def test_named_for_repo_listing_both_plugins(_, tmp_path):
        path = export_marketplace(tmp_path)

        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["name"] == "pkg-one"
        assert data["version"] == "0.0.1"
        assert [p["name"] for p in data["plugins"]] == ["pkg-one", "pkg-two"]
        assert [p["source"] for p in data["plugins"]] == [
            "./plugins/pkg-one",
            "./plugins/pkg-two",
        ]
        assert [p["version"] for p in data["plugins"]] == ["1.1.0", "2.2.0"]

    def test_plugins_written_under_plugins_folder(_, tmp_path):
        export_marketplace(tmp_path)

        assert _skills(tmp_path / "plugins" / "pkg-one") == ["lib-skill"]
        assert _skills(tmp_path / "plugins" / "pkg-two") == [
            "app-other",
            "app-skill",
        ]

    def test_no_skill_in_both_plugins(_, tmp_path):
        export_marketplace(tmp_path)

        one = set(_skills(tmp_path / "plugins" / "pkg-one"))
        two = set(_skills(tmp_path / "plugins" / "pkg-two"))
        assert not one & two

    def test_single_consumer_lists_one_plugin(_, tmp_path):
        for name in ("app-skill", "app-other"):
            exportable_registry.pop(name)

        data = json.loads(
            export_marketplace(tmp_path).read_text(encoding="utf-8")
        )

        assert data["name"] == "pkg-one"
        assert [p["name"] for p in data["plugins"]] == ["pkg-one"]

    def test_another_repo_name_names_another_marketplace(_, tmp_path):
        set_repo_name("pkg-two")

        data = json.loads(
            export_marketplace(tmp_path).read_text(encoding="utf-8")
        )

        assert data["name"] == "pkg-two"
        assert [p["name"] for p in data["plugins"]] == ["pkg-one", "pkg-two"]


class TestClaudeCode:

    def test_code_exports_every_consumer_plugin(_, tmp_path):
        from argparse import ArgumentParser

        from kaye_engine.cli.claude.code import parser as code_parser

        root = ArgumentParser()
        code_parser.register_code_parser(root.add_subparsers())
        args = root.parse_args(["code", str(tmp_path)])

        claude_logger = logging.getLogger(LOGGER_CLAUDE_NAME)
        saved_level = claude_logger.level
        try:
            with patch.object(
                code_parser, "check_setup_for_claude_cli", lambda: None
            ), patch.object(
                code_parser, "export_user_system_prompt_file"
            ), patch.object(
                code_parser, "find_user_system_prompt_file"
            ):
                args.func(args)
        finally:
            claude_logger.setLevel(saved_level)

        assert sorted(p.name for p in (tmp_path / "plugins").iterdir()) == [
            "pkg-one",
            "pkg-two",
        ]

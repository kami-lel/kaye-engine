"""
dry_run_test.py

Unit Tests (using pytest) for:

build_dry_run_parent_parser, enable_dry_run, disable_dry_run, is_dry_run
"""

import json
from argparse import ArgumentParser
from unittest.mock import patch

import kamilog
import pytest

from kaye_engine.cli import dry_run
from kaye_engine.cli.claude.plugin import export_zip as plugin_export_zip
from kaye_engine.cli.claude.plugin.manifest import ManifestPluginJson
from kaye_engine.cli.frontmatter_doc import FrontmatterDoc
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
    disable_dry_run,
    enable_dry_run,
    is_dry_run,
)


# auxiliaries  ##################################################################
@pytest.fixture(autouse=True)
def _reset_dry_run():
    disable_dry_run()
    yield
    disable_dry_run()


# TestParser  ####################################################################
class TestParser:
    @staticmethod
    def _parse(argv):
        parser = ArgumentParser(parents=[build_dry_run_parent_parser()])
        return parser.parse_args(argv)

    def test_default_is_live(_):
        assert _parse_default() is False

    def test_flag_sets_true(_):
        assert TestParser._parse(["--dry-run"]).dry_run is True

    def test_short_flag_sets_true(_):
        assert TestParser._parse(["-n"]).dry_run is True

    def test_builds_fresh_parser_per_call(_):
        assert build_dry_run_parent_parser() is not build_dry_run_parent_parser()


def _parse_default():
    return TestParser._parse([]).dry_run


# TestSwitch  ####################################################################
class TestSwitch:
    def test_starts_live(_):
        assert is_dry_run() is False

    def test_enable_turns_on(_):
        enable_dry_run()
        assert is_dry_run() is True

    def test_disable_turns_off(_):
        enable_dry_run()
        disable_dry_run()
        assert is_dry_run() is False

    @pytest.mark.parametrize("name", dry_run._LOGGER_NAMES)
    def test_enable_badges_every_engine_logger(_, name):
        enable_dry_run()
        assert kamilog.getLogger(name)._run_badges == (dry_run.DRY_BADGE,)

    @pytest.mark.parametrize("name", dry_run._LOGGER_NAMES)
    def test_disable_clears_every_engine_logger(_, name):
        enable_dry_run()
        disable_dry_run()
        assert kamilog.getLogger(name)._run_badges == ()


# TestApplyArg  ##################################################################
class TestApplyDryRunArg:
    def test_true_enables(_):
        apply_dry_run_arg(_Args(True))
        assert is_dry_run() is True

    def test_false_resets_a_previous_enable(_):
        enable_dry_run()
        apply_dry_run_arg(_Args(False))
        assert is_dry_run() is False

    def test_missing_attribute_counts_as_live(_):
        apply_dry_run_arg(object())
        assert is_dry_run() is False


class _Args:
    def __init__(self, dry_run):
        self.dry_run = dry_run


# TestWritersUnderDryRun  #########################################################
class TestWritersUnderDryRun:
    """each writer reports its deed with the dry badge, touches no disk"""

    @staticmethod
    def _badges(caplog):
        return [rec.badges for rec in caplog.records if hasattr(rec, "badges")]

    def test_frontmatter_doc_writes_nothing(_, tmp_path, caplog):
        class _Doc(FrontmatterDoc):
            def _render_frontmatter(self):
                return "a: 1\n"

        enable_dry_run()
        with caplog.at_level("DEBUG"):
            _Doc().write(tmp_path / "doc.md")

        assert not (tmp_path / "doc.md").exists()
        assert (dry_run.DRY_BADGE,) in TestWritersUnderDryRun._badges(caplog)

    def test_frontmatter_doc_writes_when_live(_, tmp_path):
        class _Doc(FrontmatterDoc):
            def _render_frontmatter(self):
                return "a: 1\n"

        _Doc().write(tmp_path / "doc.md")

        assert (tmp_path / "doc.md").is_file()

    def test_plugin_manifest_writes_nothing(_, tmp_path):
        enable_dry_run()
        with ManifestPluginJson(tmp_path / "plug") as manifest:
            manifest.name = "x"

        assert not (tmp_path / "plug").exists()

    def test_plugin_manifest_writes_when_live(_, tmp_path):
        with ManifestPluginJson(tmp_path / "plug") as manifest:
            manifest.name = "x"

        written = tmp_path / "plug" / ".claude-plugin" / "plugin.json"
        assert json.loads(written.read_text(encoding="utf-8"))["name"] == "x"

    def test_plugin_zip_creates_nothing(_, tmp_path, caplog):
        enable_dry_run()
        destination = tmp_path / "out"
        with patch.object(
            plugin_export_zip, "get_plugin_name", lambda: "plug"
        ), patch.object(
            plugin_export_zip, "get_claude_cli_consumer_version", lambda: "1"
        ), caplog.at_level("DEBUG"):
            plugin_export_zip.export_plugin_as_zip(destination)

        assert not destination.exists()
        assert "plug-1.zip" in caplog.text


# TestWiring  ####################################################################
class TestWiring:
    @pytest.mark.parametrize(
        "argv",
        [
            ["skill"],
            ["claude", "skills"],
            ["continue"],
            ["export-image-prompt", "F"],
            ["export-json"],
            ["claude", "plugin"],
            ["claude", "marketplace"],
            ["claude", "code"],
            ["claude", "vs-code-extension"],
        ],
    )
    def test_command_accepts_dry_run(_, argv):
        from kaye_engine.cli.cli_main import register_cli_main_parser

        parser, _sub = register_cli_main_parser()

        assert parser.parse_args(argv + ["--dry-run"]).dry_run is True

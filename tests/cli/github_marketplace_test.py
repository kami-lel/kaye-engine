"""
tests/cli/github_marketplace_test.py

test: ``build-github-marketplace OUTPUT`` -- one repo root serving Claude
and Codex, named ``REPO-marketplace``, writing only its owned paths
"""

import json
from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.cli_main import register_cli_subcommands
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.cli.github_marketplace.export import OWNED_PATHS
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree
from kaye_engine.repo import set_repo_name, set_repo_version

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.consumer_helper import isolated_consumers, isolated_repo
from tests.corpus_helper import load_corpus_from_sources


@pytest.fixture(autouse=True)
def _two_consumers():
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    entries = {
        name: BlueprintRegistry(
            canonical_name=name, blueprint=create_blueprint(), consumer=owner
        )
        for name, owner in (("lib-skill", "pkg-one"), ("app-skill", "pkg-two"))
    }
    with isolated_consumers(), isolated_repo(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock:
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        set_default_consumer("pkg-one")
        set_repo_name("pkg-one")
        set_repo_version("1.1.0")
        meta_mock.side_effect = _FakeMetadata
        yield
    disable_dry_run()
    clear_corpus_tree()


def _run(argv):
    parser = ArgumentParser()
    register_cli_subcommands(parser.add_subparsers())
    args = parser.parse_args(argv)
    args.func(args)


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestStructure:

    def test_writes_only_owned_root_entries(_, tmp_path):
        (tmp_path / "README.md").write_text("keep me", encoding="utf-8")

        _run(["build-github-marketplace", str(tmp_path)])

        assert sorted(p.name for p in tmp_path.iterdir()) == sorted(
            OWNED_PATHS + ("README.md",)
        )
        assert (tmp_path / "README.md").read_text(encoding="utf-8") == (
            "keep me"
        )

    def test_surface_flag_is_refused(_, tmp_path):
        with pytest.raises(SystemExit) as info:
            _run(["build-github-marketplace", str(tmp_path), "-u", "claude"])

        assert info.value.code == 1
        assert not any(tmp_path.iterdir())

    def test_dry_run_writes_nothing(_, tmp_path):
        out = tmp_path / "out"

        _run(["build-github-marketplace", "-n", str(out)])

        assert not out.exists()


class TestHeader:

    def test_both_manifests_named_repo_marketplace(_, tmp_path):
        _run(["build-github-marketplace", str(tmp_path)])

        claude = _read(tmp_path / ".claude-plugin" / "marketplace.json")
        codex = _read(tmp_path / ".agents" / "plugins" / "marketplace.json")
        assert claude["name"] == codex["name"] == "pkg-one-marketplace"
        assert codex["interface"] == {"displayName": "Pkg One Marketplace"}

    def test_claude_manifest_owned_by_default_consumer(_, tmp_path):
        _run(["build-github-marketplace", str(tmp_path)])

        claude = _read(tmp_path / ".claude-plugin" / "marketplace.json")
        assert claude["description"] == "summary of pkg-one"


class TestContent:

    def test_each_platform_lists_every_consumer_in_own_folder(_, tmp_path):
        _run(["build-github-marketplace", str(tmp_path)])

        claude = _read(tmp_path / ".claude-plugin" / "marketplace.json")
        codex = _read(tmp_path / ".agents" / "plugins" / "marketplace.json")
        assert [p["source"] for p in claude["plugins"]] == [
            "./plugins/claude/pkg-one",
            "./plugins/claude/pkg-two",
        ]
        assert [p["source"]["path"] for p in codex["plugins"]] == [
            "./plugins/codex/pkg-one",
            "./plugins/codex/pkg-two",
        ]
        one = tmp_path / "plugins"
        assert (one / "claude/pkg-one/.claude-plugin/plugin.json").is_file()
        assert (one / "codex/pkg-one/.codex-plugin/plugin.json").is_file()
        assert (one / "codex/pkg-two/skills/app-skill/SKILL.md").is_file()

"""
tests/cli/github_release_test.py

test: ``build-github-release`` -- one versioned zip per call, unknown
consumer exits 1, dry run writes nothing
"""

import zipfile
from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.cli_main import register_cli_subcommands
from kaye_engine.cli.claude import package_meta
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.consumer_helper import isolated_consumers
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
    }
    with isolated_consumers(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock:
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        meta_mock.side_effect = lambda name: _FakeMetadata(name)
        yield
    disable_dry_run()
    clear_corpus_tree()


def _parse(argv):
    parser = ArgumentParser()
    register_cli_subcommands(parser.add_subparsers())
    return parser.parse_args(argv)


def _run(argv):
    args = _parse(argv)
    with patch(
        "kaye_engine.cli.github_release.parser.check_setup_for_claude_cli"
    ):
        args.func(args)


class TestBuildGithubRelease:

    def test_writes_one_versioned_zip_into_output(_, tmp_path):
        _run(["build-github-release", "pkg-two", "-o", str(tmp_path)])

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-two-2.2.0.zip"]

    def test_zip_holds_manifest_at_root_and_only_own_skills(_, tmp_path):
        _run(["build-github-release", "pkg-one", "-o", str(tmp_path)])

        with zipfile.ZipFile(tmp_path / "pkg-one-1.1.0.zip") as archive:
            names = archive.namelist()
        assert ".claude-plugin/plugin.json" in names
        assert any(n.startswith("skills/lib-skill/") for n in names)
        assert not any("app-skill" in n for n in names)

    def test_output_defaults_to_dist(_, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        _run(["build-github-release", "pkg-one"])

        assert [p.name for p in (tmp_path / "dist").iterdir()] == [
            "pkg-one-1.1.0.zip"
        ]

    def test_unknown_consumer_exits_1_and_writes_nothing(
        _, tmp_path, caplog
    ):
        with pytest.raises(SystemExit) as raised:
            _run(["build-github-release", "pkg-nope", "-o", str(tmp_path)])

        assert raised.value.code == 1
        assert "pkg-one, pkg-two" in caplog.text
        assert list(tmp_path.iterdir()) == []

    def test_consumer_is_required(_):
        with pytest.raises(SystemExit):
            _parse(["build-github-release"])

    def test_dry_run_writes_nothing(_, tmp_path):
        out = tmp_path / "out"

        _run(["build-github-release", "pkg-one", "-n", "-o", str(out)])

        assert not out.exists()

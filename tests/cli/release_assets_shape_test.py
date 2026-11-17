"""
tests/cli/release_assets_shape_test.py

test: the release assets of a library-shaped repo (one consumer) and a
vault-shaped repo (default consumer plus the library it takes skills from),
with the exact names and contents of each plugin zip; ``claude plugin``
with no consumer argument writes the default consumer's plugin
"""

import zipfile
from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.claude.plugin.parser import register_plugin_parser
from kaye_engine.cli.cli_main import register_cli_subcommands
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.cli.github_release import installer_stage
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree
from kaye_engine.repo import set_repo_name, set_repo_version

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.cli.github_release_installer_windows_test import fake_payload
from tests.consumer_helper import isolated_consumers, isolated_repo
from tests.corpus_helper import load_corpus_from_sources

_INSTALLERS = [
    "{}-claude-vsc-installer-Win.zip",
    "{}-claude-vsc-installer-linux.run",
]


# auxiliaries  #################################################################
def _entry(name, consumer):
    return BlueprintRegistry(
        canonical_name=name,
        blueprint=create_blueprint(),
        consumer=consumer,
    )


def _setup(entries, consumers, repo_name, version, default):
    for display, canonical, consumer_version in consumers:
        register_consumer(display, canonical, consumer_version)
    set_default_consumer(default)
    set_repo_name(repo_name)
    set_repo_version(version)
    exportable_registry.clear()
    exportable_registry.update(entries)


@pytest.fixture(autouse=True)
def _isolation():
    disable_dry_run()
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    with isolated_consumers(), isolated_repo(), patch.dict(
        exportable_registry, {}, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock, patch.object(
        installer_stage, "generate_vs_code_payload", fake_payload
    ):
        meta_mock.side_effect = lambda name: _FakeMetadata(name)
        yield
    disable_dry_run()
    clear_corpus_tree()


@pytest.fixture
def library_repo():
    _setup(
        {"lib-skill": _entry("lib-skill", "kaye-library")},
        [("Kaye Library", "kaye-library", "1.4.1")],
        "kaye-library",
        "1.4.1",
        "kaye-library",
    )


@pytest.fixture
def vault_repo():
    # the vault took every library skill but one over, as override_exportable
    # does: the overridden skill belongs to the vault alone
    _setup(
        {
            "lib-skill": _entry("lib-skill", "kaye-library"),
            "taken-over": _entry("taken-over", "kaye-vault"),
            "vault-skill": _entry("vault-skill", "kaye-vault"),
        },
        [
            ("Kaye Library", "kaye-library", "1.4.1"),
            ("Kaye Vault", "kaye-vault", "1.2.2"),
        ],
        "kaye-vault",
        "1.2.2",
        "kaye-vault",
    )


def _run_release(output, *extra):
    parser = ArgumentParser()
    register_cli_subcommands(parser.add_subparsers())
    args = parser.parse_args(
        ["build-github-release-assets", str(output), *extra]
    )
    with patch(
        "kaye_engine.cli.github_release.parser.check_setup_for_claude_cli"
    ):
        args.func(args)


def _names(folder):
    return sorted(p.name for p in folder.iterdir())


def _skills_in_zip(path):
    with zipfile.ZipFile(path) as archive:
        return sorted(
            n.split("/")[1]
            for n in archive.namelist()
            if n.startswith("skills/") and n.endswith("/SKILL.md")
        )


# pytest  ######################################################################
class TestLibraryShapedRepo:

    def test_one_plugin_zip_and_two_installers(_, tmp_path, library_repo):
        _run_release(tmp_path)

        assert _names(tmp_path) == sorted(
            ["kaye-library-1.4.1-claude-desktop-plugin.zip"]
            + [n.format("kaye-library-1.4.1") for n in _INSTALLERS]
        )

    def test_dry_run_lists_them_and_writes_nothing(
        _, tmp_path, library_repo, caplog
    ):
        _run_release(tmp_path / "out", "--dry-run")

        assert not (tmp_path / "out").exists()
        assert "kaye-library-1.4.1-claude-desktop-plugin.zip" in caplog.text
        assert "claude-desktop-plugin-" not in caplog.text


class TestVaultShapedRepo:

    def test_default_consumer_zip_has_no_suffix_library_zip_has_one(
        _, tmp_path, vault_repo
    ):
        _run_release(tmp_path)

        assert _names(tmp_path) == sorted(
            [
                "kaye-vault-1.2.2-claude-desktop-plugin.zip",
                "kaye-vault-1.2.2-claude-desktop-plugin-kaye-library.zip",
            ]
            + [n.format("kaye-vault-1.2.2") for n in _INSTALLERS]
        )

    def test_library_zip_lacks_the_taken_over_skill(_, tmp_path, vault_repo):
        _run_release(tmp_path)

        library_zip = (
            tmp_path / "kaye-vault-1.2.2-claude-desktop-plugin-kaye-library.zip"
        )
        vault_zip = tmp_path / "kaye-vault-1.2.2-claude-desktop-plugin.zip"
        assert _skills_in_zip(library_zip) == ["lib-skill"]
        assert _skills_in_zip(vault_zip) == ["taken-over", "vault-skill"]

    def test_dry_run_lists_both_plugin_zips(
        _, tmp_path, vault_repo, caplog
    ):
        _run_release(tmp_path / "out", "--dry-run")

        assert not (tmp_path / "out").exists()
        assert "kaye-vault-1.2.2-claude-desktop-plugin.zip" in caplog.text
        assert (
            "kaye-vault-1.2.2-claude-desktop-plugin-kaye-library.zip"
            in caplog.text
        )


class TestClaudePluginDefault:

    def test_no_consumer_argument_writes_the_default_plugin(
        _, tmp_path, vault_repo
    ):
        parser = ArgumentParser()
        register_plugin_parser(parser.add_subparsers())
        args = parser.parse_args(["plugin", str(tmp_path)])
        with patch(
            "kaye_engine.cli.claude.plugin.parser.check_setup_for_claude_cli"
        ):
            args.func(args)

        assert _names(tmp_path) == ["kaye-vault"]

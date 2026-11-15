"""
tests/cli/github_release_test.py

test: ``build-github-release OUTPUT`` -- one zip per plugin consumer plus
both VS Code installers, all named ``REPO-VERSION-TYPE[-CONSUMER|-OS]``, the
old ``-o`` and consumer argument rejected, an unset repo name, version, or
default consumer exits 1, dry run lists every asset and writes nothing;
``get_release_asset_name``
"""

import zipfile
from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.cli_main import register_cli_subcommands
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.cli.github_release.asset_name import (
    ASSET_DESKTOP_PLUGIN,
    ASSET_VSC_INSTALLER,
    OS_LINUX,
    OS_WINDOWS,
    get_release_asset_name,
)
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.repo import set_repo_name, set_repo_version
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.cli.github_release_installer_windows_test import fake_payload
from kaye_engine.cli.github_release import installer_stage
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
    }
    with isolated_consumers(), isolated_repo(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock, patch.object(
        installer_stage, "generate_vs_code_payload", fake_payload
    ):
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        set_default_consumer("pkg-one")
        set_repo_name("pkg-one")
        set_repo_version("1.1.0")
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

    def test_one_run_writes_two_zips_and_both_installers(_, tmp_path):
        _run(["build-github-release", str(tmp_path)])

        assert sorted(p.name for p in tmp_path.iterdir()) == [
            "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip",
            "pkg-one-1.1.0-claude-desktop-plugin.zip",
            "pkg-one-1.1.0-claude-vsc-installer-Win.zip",
            "pkg-one-1.1.0-claude-vsc-installer-linux.run",
        ]

    def test_default_consumer_zip_leaves_its_name_out(_, tmp_path):
        set_default_consumer("pkg-two")

        _run(["build-github-release", str(tmp_path)])

        names = sorted(p.name for p in tmp_path.iterdir())
        assert "pkg-one-1.1.0-claude-desktop-plugin-pkg-one.zip" in names
        assert "pkg-one-1.1.0-claude-desktop-plugin.zip" in names

    def test_installers_are_the_expected_kind_of_file(_, tmp_path):
        _run(["build-github-release", str(tmp_path)])

        win = tmp_path / "pkg-one-1.1.0-claude-vsc-installer-Win.zip"
        with zipfile.ZipFile(win) as archive:
            assert "src/place-payload-into-claude-folder.ps1" in (
                archive.namelist()
            )
        run = tmp_path / "pkg-one-1.1.0-claude-vsc-installer-linux.run"
        assert run.read_bytes().startswith(b"#!/usr/bin/env bash")
        assert run.stat().st_mode & 0o111

    def test_installers_render_on_surface_claude_vsc(_, tmp_path):
        seen = []

        def spy(folder, *, render_profile=None):
            seen.append(render_profile)
            fake_payload(folder)

        with patch.object(installer_stage, "generate_vs_code_payload", spy):
            _run(["build-github-release", str(tmp_path)])

        assert len(seen) == 2
        assert all(profile.show_comment for profile in seen)

    def test_every_asset_starts_with_the_repo_name(_, tmp_path):
        set_repo_name("some-repo")

        _run(["build-github-release", str(tmp_path)])

        assert all(
            p.name.startswith("some-repo-1.1.0-") for p in tmp_path.iterdir()
        )

    def test_log_names_every_zip_written(_, tmp_path, caplog):
        _run(["build-github-release", str(tmp_path)])

        assert "pkg-one-1.1.0-claude-desktop-plugin.zip" in caplog.text
        assert "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip" in caplog.text

    def test_each_zip_holds_manifest_at_root_and_only_own_skills(
        _, tmp_path
    ):
        _run(["build-github-release", str(tmp_path)])

        with zipfile.ZipFile(
            tmp_path / "pkg-one-1.1.0-claude-desktop-plugin.zip"
        ) as archive:
            names = archive.namelist()
        assert ".claude-plugin/plugin.json" in names
        assert any(n.startswith("skills/lib-skill/") for n in names)
        assert not any("app-skill" in n for n in names)

    def test_output_is_required(_):
        with pytest.raises(SystemExit):
            _parse(["build-github-release"])

    def test_old_output_flag_is_rejected(_, tmp_path):
        with pytest.raises(SystemExit):
            _parse(["build-github-release", "-o", str(tmp_path)])

    def test_a_consumer_argument_is_rejected(_, tmp_path):
        with pytest.raises(SystemExit):
            _parse(["build-github-release", str(tmp_path), "pkg-one"])

    def test_dry_run_lists_every_asset_and_writes_nothing(
        _, tmp_path, caplog
    ):
        out = tmp_path / "out"

        _run(["build-github-release", "-n", str(out)])

        assert not out.exists()
        for name in (
            "pkg-one-1.1.0-claude-desktop-plugin.zip",
            "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip",
            "pkg-one-1.1.0-claude-vsc-installer-Win.zip",
            "pkg-one-1.1.0-claude-vsc-installer-linux.run",
        ):
            assert name in caplog.text

    @pytest.mark.parametrize(
        "unset", ["repo name", "repo version", "default consumer"]
    )
    def test_an_unset_registry_exits_1_and_writes_nothing(
        _, tmp_path, unset
    ):
        # pylint: disable=import-outside-toplevel
        from kaye_engine import consumer, repo

        if unset == "repo name":
            repo._repo_name = None
        elif unset == "repo version":
            repo._repo_version = None
        else:
            consumer._default_canonical_name = None

        with pytest.raises(SystemExit) as raised:
            _run(["build-github-release", str(tmp_path / "out")])

        assert raised.value.code == 1
        assert not (tmp_path / "out").exists()


class TestGetReleaseAssetName:

    def test_desktop_plugin_of_the_default_consumer(_):
        assert (
            get_release_asset_name(ASSET_DESKTOP_PLUGIN, consumer="pkg-one")
            == "pkg-one-1.1.0-claude-desktop-plugin.zip"
        )

    def test_desktop_plugin_of_another_consumer(_):
        assert (
            get_release_asset_name(ASSET_DESKTOP_PLUGIN, consumer="pkg-two")
            == "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip"
        )

    def test_windows_installer(_):
        assert (
            get_release_asset_name(ASSET_VSC_INSTALLER, os_name=OS_WINDOWS)
            == "pkg-one-1.1.0-claude-vsc-installer-Win.zip"
        )

    def test_linux_installer(_):
        assert (
            get_release_asset_name(ASSET_VSC_INSTALLER, os_name=OS_LINUX)
            == "pkg-one-1.1.0-claude-vsc-installer-linux.run"
        )

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"asset_type": "nope"},
            {"asset_type": ASSET_VSC_INSTALLER},
            {"asset_type": ASSET_VSC_INSTALLER, "os_name": "mac"},
            {"asset_type": ASSET_VSC_INSTALLER, "os_name": "Win",
             "consumer": "pkg-one"},
            {"asset_type": ASSET_DESKTOP_PLUGIN, "os_name": "Win"},
        ],
    )
    def test_bad_arguments_raise(_, kwargs):
        with pytest.raises(ValueError):
            get_release_asset_name(**kwargs)

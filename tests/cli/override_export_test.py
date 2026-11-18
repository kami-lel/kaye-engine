"""
tests/cli/override_export_test.py

test: after ``override_exportable`` the skill sits only in the overriding
consumer's plugin -- absent from the original consumer's plugin folder,
marketplace and release zip, present in the overrider's
"""

import zipfile
from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.claude.marketplace.export import export_marketplace
from kaye_engine.cli.claude.plugin.export_folder import (
    export_plugins_as_folders,
)
from kaye_engine.cli.cli_main import register_cli_subcommands
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.cli.github_release import installer_stage
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import create_blueprint
from kaye_engine.prompt.blueprint.registry import (
    blueprint_registry,
    override_exportable,
    register_blueprint,
)
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree
from kaye_engine.repo import set_repo_name, set_repo_version

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.cli.github_release_installer_windows_test import fake_payload
from tests.consumer_helper import isolated_consumers, isolated_repo
from tests.corpus_helper import load_corpus_from_sources

_NAMES = ("ovx-kept", "ovx-taken", "ovx-own", "ovx-core")


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _library_and_overrider():
    """
    ``ovx-kept`` and ``ovx-taken`` start in the library; the overrider takes
    ``ovx-taken`` over and has ``ovx-own`` besides; ``ovx-core`` is internal
    """
    disable_dry_run()
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    with isolated_consumers(), isolated_repo(), patch.object(
        package_meta, "metadata"
    ) as meta_mock, patch.object(
        installer_stage, "generate_vs_code_payload", fake_payload
    ):
        meta_mock.side_effect = lambda name: _FakeMetadata(name)
        register_consumer("Library", "ovx-library", "1.4.1")
        register_consumer("Overrider", "ovx-overrider", "1.2.2")
        set_default_consumer("ovx-overrider")
        set_repo_name("ovx-overrider")
        set_repo_version("1.2.2")

        register_blueprint(
            "ovx-core", create_blueprint(), is_exportable=False
        )
        register_blueprint(
            "ovx-kept",
            create_blueprint(dependencies=["ovx-core"]),
            consumer="ovx-library",
        )
        register_blueprint(
            "ovx-taken",
            create_blueprint(dependencies=["ovx-core"]),
            consumer="ovx-library",
        )
        register_blueprint(
            "ovx-own", create_blueprint(), consumer="ovx-overrider"
        )
        # the takeover wraps the library blueprint by object, never by name
        library_bp = blueprint_registry["ovx-taken"].blueprint
        override_exportable(
            "ovx-taken",
            create_blueprint(dependencies=[library_bp]),
            consumer="ovx-overrider",
        )
        yield
        for name in _NAMES:
            blueprint_registry.pop(name, None)
            exportable_registry.pop(name, None)
    disable_dry_run()
    clear_corpus_tree()


def _skills(plugin_root):
    return sorted(p.name for p in (plugin_root / "skills").iterdir())


def _skills_in_zip(path):
    with zipfile.ZipFile(path) as archive:
        return sorted(
            n.split("/")[1]
            for n in archive.namelist()
            if n.startswith("skills/") and n.endswith("/SKILL.md")
        )


# pytest  ######################################################################
class TestOverrideExport:

    def test_registry_names_the_overrider_as_owner(_):
        assert exportable_registry["ovx-taken"].consumer == "ovx-overrider"
        assert exportable_registry["ovx-kept"].consumer == "ovx-library"

    def test_plugin_folders_hold_no_library_copy(_, tmp_path):
        export_plugins_as_folders(tmp_path)

        assert _skills(tmp_path / "ovx-library") == ["ovx-kept"]
        assert _skills(tmp_path / "ovx-overrider") == ["ovx-own", "ovx-taken"]

    def test_marketplace_holds_no_library_copy(_, tmp_path):
        export_marketplace(tmp_path)

        library = tmp_path / "plugins" / "ovx-library"
        overrider = tmp_path / "plugins" / "ovx-overrider"
        assert _skills(library) == ["ovx-kept"]
        assert "ovx-taken" in _skills(overrider)

    def test_release_zips_hold_no_library_copy(_, tmp_path):
        parser = ArgumentParser()
        register_cli_subcommands(parser.add_subparsers())
        args = parser.parse_args(["build-github-release-assets", str(tmp_path)])
        with patch(
            "kaye_engine.cli.github_release.parser.check_setup_for_claude_cli"
        ):
            args.func(args)

        library_zip = (
            tmp_path / "ovx-overrider-1.2.2-claude-desktop-plugin-ovx-library.zip"
        )
        overrider_zip = (
            tmp_path / "ovx-overrider-1.2.2-claude-desktop-plugin.zip"
        )
        assert _skills_in_zip(library_zip) == ["ovx-kept"]
        assert _skills_in_zip(overrider_zip) == ["ovx-own", "ovx-taken"]

    def test_internal_blueprint_cannot_be_overridden(_):
        with pytest.raises(ValueError):
            override_exportable(
                "ovx-core", create_blueprint(), consumer="ovx-overrider"
            )

        assert blueprint_registry["ovx-core"].is_exportable is False

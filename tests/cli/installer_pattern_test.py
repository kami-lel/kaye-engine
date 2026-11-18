"""
tests/cli/installer_pattern_test.py

test: every installer follows one pattern -- the stage 1 payload holds one
marketplace folder named by the repo name, whose manifest lists one plugin
per consumer; ``place_vs_code_payload`` and the Linux installer install
``<repo name>/`` and enable ``PLUGIN@<repo name>`` keys; no installer
source hardcodes a marketplace or plugin name
"""

import json
import os
import shutil
import subprocess
from unittest.mock import patch

import pytest
from kaye_engine.cli.claude.vs_code import payload as payload_module
from kaye_engine.cli.claude.vs_code.place import place_vs_code_payload
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.cli.github_release import installer_stage
from kaye_engine.cli.github_release.installer_linux import (
    build_linux_installer,
)
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree
from kaye_engine.repo import set_repo_name, set_repo_version

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.consumer_helper import isolated_consumers, isolated_repo
from tests.corpus_helper import load_corpus_from_sources

_TEMPLATES = (
    installer_stage.get_installer_template_path(
        "place-payload-into-claude-folder.ps1"
    ),
    installer_stage.get_installer_template_path("install.sh"),
    installer_stage.get_installer_template_path("install.cmd"),
)

# every name a consumer project of this workspace is known by
# FIXME names consumer `kaye-vault`, here & in 3 more test files; AGENTS forbids
_HARDCODED_NAMES = ("kaye-engine", "kaye-library", "kaye-vault")

_REPO_NAMES = ("kaye-library", "kaye-vault")


# auxiliaries  #################################################################
def _entry(name, consumer):
    return BlueprintRegistry(
        canonical_name=name,
        blueprint=create_blueprint(),
        consumer=consumer,
    )


def _fake_prompt(path, *, use_coder=False, render_profile=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("prompt\n", encoding="utf-8")


@pytest.fixture(autouse=True)
def _consumers():
    disable_dry_run()
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    entries = {
        "lib-skill": _entry("lib-skill", "kaye-library"),
        "app-skill": _entry("app-skill", "kaye-vault"),
    }
    with isolated_consumers(), isolated_repo(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock, patch.object(
        payload_module, "export_user_system_prompt_file", _fake_prompt
    ):
        register_consumer("Kaye Library", "kaye-library", "1.4.1")
        register_consumer("Kaye Vault", "kaye-vault", "1.2.2")
        set_default_consumer("kaye-vault")
        set_repo_version("1.2.2")
        meta_mock.side_effect = lambda name: _FakeMetadata(name)
        yield
    disable_dry_run()
    clear_corpus_tree()


def _stage(tmp_path, repo_name):
    set_repo_name(repo_name)
    folder = tmp_path / "payload"
    folder.mkdir()
    payload_module.generate_vs_code_payload(folder)
    return folder


def _settings(claude):
    return json.loads((claude / "settings.json").read_text(encoding="utf-8"))


# pytest  ######################################################################
@pytest.mark.parametrize("repo_name", _REPO_NAMES)
class TestStagedPayload:

    def test_one_marketplace_folder_named_by_the_repo(
        _, tmp_path, repo_name
    ):
        folder = _stage(tmp_path, repo_name)

        markets = [
            d.name
            for d in folder.iterdir()
            if (d / ".claude-plugin" / "marketplace.json").is_file()
        ]
        assert markets == [repo_name]

    def test_manifest_name_equals_its_folder(_, tmp_path, repo_name):
        folder = _stage(tmp_path, repo_name)

        manifest = json.loads(
            (folder / repo_name / ".claude-plugin" / "marketplace.json")
            .read_text(encoding="utf-8")
        )
        assert manifest["name"] == repo_name

    def test_one_plugin_per_consumer_named_by_it(_, tmp_path, repo_name):
        folder = _stage(tmp_path, repo_name)

        manifest = json.loads(
            (folder / repo_name / ".claude-plugin" / "marketplace.json")
            .read_text(encoding="utf-8")
        )
        assert [p["name"] for p in manifest["plugins"]] == [
            "kaye-library",
            "kaye-vault",
        ]
        plugins = sorted(
            p.name for p in (folder / repo_name / "plugins").iterdir()
        )
        assert plugins == ["kaye-library", "kaye-vault"]


@pytest.mark.parametrize("repo_name", _REPO_NAMES)
class TestPlaceVsCodePayload:

    def test_installs_repo_folder_and_enables_plugin_keys(
        _, tmp_path, repo_name
    ):
        folder = _stage(tmp_path, repo_name)
        claude = tmp_path / "claude"

        place_vs_code_payload(folder, claude)

        assert (claude / repo_name / ".claude-plugin").is_dir()
        assert not (claude / "kaye-engine").exists()
        settings = _settings(claude)
        assert list(settings["extraKnownMarketplaces"]) == [repo_name]
        assert sorted(settings["enabledPlugins"]) == [
            "kaye-library@" + repo_name,
            "kaye-vault@" + repo_name,
        ]


@pytest.mark.skipif(
    not (shutil.which("bash") and shutil.which("python3")),
    reason="needs bash and python3",
)
@pytest.mark.parametrize("repo_name", _REPO_NAMES)
class TestLinuxInstaller:

    def test_installs_the_same_names_as_the_python_route(
        _, tmp_path, repo_name
    ):
        set_repo_name(repo_name)
        run_file = tmp_path / "inst.run"
        build_linux_installer(run_file)
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)

        subprocess.run(
            ["bash", str(run_file)],
            env=dict(os.environ, HOME=str(home)),
            capture_output=True,
            check=True,
        )

        claude = home / ".claude"
        assert (claude / repo_name / ".claude-plugin").is_dir()
        settings = _settings(claude)
        assert list(settings["extraKnownMarketplaces"]) == [repo_name]
        assert sorted(settings["enabledPlugins"]) == [
            "kaye-library@" + repo_name,
            "kaye-vault@" + repo_name,
        ]


class TestNoHardcodedName:

    @pytest.mark.parametrize("template", _TEMPLATES, ids=lambda p: p.name)
    @pytest.mark.parametrize("name", _HARDCODED_NAMES)
    def test_template_names_no_marketplace_or_plugin(_, template, name):
        assert name not in template.read_text(encoding="utf-8")

    @pytest.mark.parametrize("name", _HARDCODED_NAMES)
    def test_place_module_names_no_marketplace_or_plugin(_, name):
        import kaye_engine.cli.claude.vs_code.place as place

        with open(place.__file__, encoding="utf-8") as source:
            assert name not in source.read()

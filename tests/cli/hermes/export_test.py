"""
tests/cli/hermes/export_test.py

Unit Tests (using pytest) for:

- export_hermes_folder
"""

import os
from unittest.mock import patch

import pytest

from kaye_engine.cli import hermes
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run
from kaye_engine.cli.hermes.export import export_hermes_folder
from kaye_engine.cli.hermes.setup import setup_hermes_cli
from kaye_engine.consumer import register_consumer, set_entry_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, blueprint_registry
from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)

from tests.consumer_helper import TEST_CONSUMER, isolated_consumers
from tests.corpus_helper import load_corpus_from_sources


def _registry(name, **kwargs):
    return BlueprintRegistry(
        canonical_name=name,
        display_name="Display " + name,
        blueprint=Blueprint(meta=BlueprintMeta(description="d")),
        consumer=TEST_CONSUMER,
        **kwargs,
    )


@pytest.fixture(autouse=True)
def _inline_corpus():
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    entries = {
        "chat": _registry("chat"),
        "kaye-chat": _registry("kaye-chat", is_exportable=False),
        "ria-chat": _registry("ria-chat", is_exportable=False),
    }
    isolation = isolated_consumers()
    isolation.__enter__()  # pylint: disable=unnecessary-dunder-call
    register_consumer("Some Proj", "some-proj", "1.0")
    set_entry_consumer("some-proj")
    saved = (
        hermes._soul_blueprint_name,
        hermes._profile_blueprint_names,
    )
    with patch.dict(blueprint_registry, entries), patch.dict(
        exportable_registry, {"chat": entries["chat"]}, clear=True
    ):
        setup_hermes_cli(
            "chat", {"kaye": "kaye-chat", "ria": "ria-chat"}
        )
        yield
    (
        hermes._soul_blueprint_name,
        hermes._profile_blueprint_names,
    ) = saved
    isolation.__exit__(None, None, None)
    disable_dry_run()
    clear_corpus_tree()


def _list_files(folder):
    return sorted(
        str(path.relative_to(folder))
        for path in folder.rglob("*")
        if path.is_file()
    )


class TestExportHermesFolder:

    def test_writes_the_three_file_kinds(_, tmp_path):
        export_hermes_folder(tmp_path)
        assert _list_files(tmp_path) == [
            "SOUL.md",
            "profiles/kaye/SOUL.md",
            "profiles/kaye/skills/test-consumer/chat/SKILL.md",
            "profiles/ria/SOUL.md",
            "profiles/ria/skills/test-consumer/chat/SKILL.md",
            "skills/test-consumer/chat/SKILL.md",
        ]

    def test_profile_skills_match_default_profile(_, tmp_path):
        export_hermes_folder(tmp_path)
        rel = "skills/test-consumer/chat/SKILL.md"
        root = (tmp_path / rel).read_text(encoding="utf-8")
        for name in ("kaye", "ria"):
            copy = tmp_path / "profiles" / name / rel
            assert copy.read_text(encoding="utf-8") == root

    def test_internal_blueprint_never_becomes_a_skill(_, tmp_path):
        export_hermes_folder(tmp_path)
        assert not (tmp_path / "skills" / "test-consumer" / "kaye-chat").exists()

    def test_dry_run_writes_nothing(_, tmp_path):
        enable_dry_run()
        export_hermes_folder(tmp_path / "home")
        assert not (tmp_path / "home").exists()

    def test_second_run_leaves_every_file_untouched(_, tmp_path):
        export_hermes_folder(tmp_path)
        files = [tmp_path / name for name in _list_files(tmp_path)]
        for file in files:
            os.utime(file, (1_000_000, 1_000_000))

        export_hermes_folder(tmp_path)
        assert {f.stat().st_mtime for f in files} == {1_000_000}

    def test_changed_file_is_overwritten_alone(_, tmp_path):
        export_hermes_folder(tmp_path)
        soul = tmp_path / "SOUL.md"
        ria = tmp_path / "profiles" / "ria" / "SOUL.md"
        soul.write_text("stale", encoding="utf-8")
        os.utime(ria, (1_000_000, 1_000_000))

        export_hermes_folder(tmp_path)
        assert soul.read_text(encoding="utf-8") != "stale"
        assert ria.stat().st_mtime == 1_000_000

    def test_dry_run_leaves_changed_file_alone(_, tmp_path):
        export_hermes_folder(tmp_path)
        soul = tmp_path / "SOUL.md"
        soul.write_text("stale", encoding="utf-8")

        enable_dry_run()
        export_hermes_folder(tmp_path)
        assert soul.read_text(encoding="utf-8") == "stale"

    def test_unset_configuration_exits_one(_, tmp_path):
        hermes._soul_blueprint_name = None
        with pytest.raises(SystemExit) as info:
            export_hermes_folder(tmp_path)
        assert info.value.code == 1

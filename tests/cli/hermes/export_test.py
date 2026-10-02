"""
tests/cli/hermes/export_test.py

Unit Tests (using pytest) for:

- export_hermes_folder
"""

from unittest.mock import patch

import pytest

from kaye_engine.cli import hermes
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run
from kaye_engine.cli.hermes.export import export_hermes_folder
from kaye_engine.cli.hermes.setup import setup_hermes_cli
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, blueprint_registry
from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)


def _registry(name, **kwargs):
    return BlueprintRegistry(
        canonical_name=name,
        display_name="Display " + name,
        blueprint=Blueprint(meta=BlueprintMeta(description="d")),
        **kwargs,
    )


@pytest.fixture(autouse=True)
def _inline_corpus():
    clear_corpus_tree()
    load_corpus_tree(["# R\n"])
    entries = {
        "chat": _registry("chat"),
        "kaye-chat": _registry("kaye-chat", is_exportable=False),
        "ria-chat": _registry("ria-chat", is_exportable=False),
    }
    saved = (
        hermes._skill_category,
        hermes._soul_blueprint_name,
        hermes._profile_blueprint_names,
    )
    with patch.dict(blueprint_registry, entries), patch.dict(
        exportable_registry, {"chat": entries["chat"]}, clear=True
    ):
        setup_hermes_cli(
            "kaye", "chat", {"kaye": "kaye-chat", "ria": "ria-chat"}
        )
        yield
    (
        hermes._skill_category,
        hermes._soul_blueprint_name,
        hermes._profile_blueprint_names,
    ) = saved
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
        export_hermes_folder(tmp_path, version="1.0")
        assert _list_files(tmp_path) == [
            "SOUL.md",
            "profiles/kaye/SOUL.md",
            "profiles/ria/SOUL.md",
            "skills/kaye/chat/SKILL.md",
        ]

    def test_internal_blueprint_never_becomes_a_skill(_, tmp_path):
        export_hermes_folder(tmp_path, version="1.0")
        assert not (tmp_path / "skills" / "kaye" / "kaye-chat").exists()

    def test_dry_run_writes_nothing(_, tmp_path):
        enable_dry_run()
        export_hermes_folder(tmp_path / "home", version="1.0")
        assert not (tmp_path / "home").exists()

    def test_unset_configuration_exits_one(_, tmp_path):
        hermes._skill_category = None
        with pytest.raises(SystemExit) as info:
            export_hermes_folder(tmp_path, version="1.0")
        assert info.value.code == 1

"""
skill_form_test.py

Unit Tests (using pytest) for:

build_skill_form
"""

from unittest.mock import MagicMock

import pytest

from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.cli.open_webui.skill_form import (
    SKILL_FORM_FIELDS,
    build_skill_form,
)
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _corpus():
    clear_corpus_tree()
    load_corpus_tree(["# R\n## {when_to_use}\nw\n"])
    yield
    clear_corpus_tree()


def _build_blueprint_registry(description="d", when_to_use="w"):
    blueprint = Blueprint(
        meta=BlueprintMeta(
            description=description,
            when_to_use_node=("R", "{when_to_use}") if when_to_use else None,
        )
    )
    registry = BlueprintRegistry(
        canonical_name="test-skill",
        display_name="Test Skill",
        blueprint=blueprint,
    )
    registry.content = lambda **_: "rendered body"
    return registry


def _build_abbr_group():
    group = MagicMock(spec=ExportableAbbr)
    group.canonical_name = "abbr-group"
    group.display_name = "Abbr Group"
    group.is_user_invokable = True
    group.as_md_list.return_value = "- a: b"
    return group


# pytest  ######################################################################
class TestBuildSkillForm:

    def test_blueprint_returns_full_form(_):
        form = build_skill_form(_build_blueprint_registry())

        assert form == {
            "id": "test-skill",
            "name": "Test Skill",
            "description": "d\n\nw",
            "content": "rendered body",
            "meta": {"tags": []},
            "is_active": True,
        }

    def test_abbr_group_returns_full_form(_):
        form = build_skill_form(_build_abbr_group())

        assert form == {
            "id": "abbr-group",
            "name": "Abbr Group",
            "description": "Abbr Group",
            "content": "- a: b",
            "meta": {"tags": []},
            "is_active": True,
        }

    def test_empty_when_to_use_leaves_description_alone(_):
        form = build_skill_form(_build_blueprint_registry(when_to_use=""))

        assert form["description"] == "d"

    def test_keys_match_declared_fields(_):
        form = build_skill_form(_build_blueprint_registry())

        assert tuple(form) == SKILL_FORM_FIELDS

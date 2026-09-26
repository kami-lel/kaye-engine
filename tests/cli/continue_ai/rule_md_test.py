"""
rule_md_test.py

Unit Tests (using pytest) for:

ContinueRule
"""

import dataclasses
from unittest.mock import MagicMock

import yaml

from kaye_engine.cli.continue_ai.rule_md import ContinueRule
from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.render_profile import RenderProfile


def _split(text):
    _, front, body = text.split("---\n", 2)
    return yaml.safe_load(front), body


# pytest  ######################################################################
class TestRender:

    def test_minimal(_):
        opt = ContinueRule(name="x", body="hi").render()

        front, body = _split(opt)
        assert front == {"name": "x", "alwaysApply": False}
        assert body == "\nhi"

    def test_all_fields(_):
        rule = ContinueRule(
            name="x",
            description="d",
            globs=["**/*.py"],
            always_apply=True,
            invokable=True,
            body="b",
        )

        front, _body = _split(rule.render())

        assert front == {
            "name": "x",
            "description": "d",
            "alwaysApply": True,
            "invokable": True,
            "globs": ["**/*.py"],
        }

    def test_empty_optionals_omitted(_):
        rule = ContinueRule(name="x", description="", globs=[])

        front, _body = _split(rule.render())

        assert "description" not in front
        assert "globs" not in front
        assert "invokable" not in front


class TestWrite:

    def test_writes_rendered_text(_, tmp_path):
        rule = ContinueRule(name="x", body="hi")
        path = tmp_path / "x.md"

        rule.write(path)

        assert path.read_text(encoding="utf-8") == rule.render()


def _registry(**kwargs):
    blueprint = MagicMock()
    blueprint.sidecars.description_and_when_to_use = "d w"
    blueprint.sidecars.globs = ["*.py"]
    blueprint.render_prompt.return_value = "body"
    return BlueprintRegistry(
        canonical_name="test-rule",
        display_name="Test Rule",
        blueprint=blueprint,
        **kwargs,
    )


class TestFromExportable:

    def test_blueprint_rule(_):
        opt = ContinueRule.from_exportable(_registry())

        assert opt.name == "Test Rule"
        assert opt.description == "d w"
        assert opt.globs == ["*.py"]
        assert opt.always_apply is False
        assert opt.invokable is False
        assert opt.body == "body"

    def test_always_apply_rule(_):
        opt = ContinueRule.from_exportable(_registry(always_apply=True))

        assert opt.always_apply is True
        assert opt.invokable is False

    def test_blueprint_prompt(_):
        opt = ContinueRule.from_exportable(
            _registry(always_apply=True), is_prompt=True
        )

        assert opt.invokable is True
        assert opt.always_apply is False

    def test_abbr_group_rule(_):
        group = ExportableAbbr(
            canonical_name="abbr-x", display_name="Abbr X"
        )

        opt = ContinueRule.from_exportable(group)

        assert opt.name == "Abbr X"
        assert opt.description == "Abbr X"
        assert opt.globs == []
        assert opt.always_apply is False
        assert opt.body == group.as_md_list()

    def test_render_profile_reaches_content(_):
        registry = _registry()
        profile = RenderProfile(sparseness=0, show_comment=False)

        ContinueRule.from_exportable(registry, render_profile=profile)

        registry.blueprint.render_prompt.assert_called_once_with(
            profile=dataclasses.replace(
                registry.render_profile.merge(profile),
                display_name=registry.display_name,
            )
        )

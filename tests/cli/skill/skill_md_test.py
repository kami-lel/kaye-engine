"""
skill_md_test.py

Unit Tests (using pytest) for:

Skill version injection
"""

import dataclasses
from unittest.mock import patch

import yaml

from kaye_engine.cli.skill.skill_md import Skill
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.data import Blueprint, BlueprintMeta
from kaye_engine.prompt.blueprint.render_profile import RenderProfile


_REGISTRY_RENDER_PROMPT = "kaye_engine.prompt.blueprint.registry.render_prompt"


def _dummy_blueprint():
    return Blueprint(meta=BlueprintMeta(description="d"))


def _dummy_registry(blueprint):
    return BlueprintRegistry(
        canonical_name="test-skill",
        display_name="Test Skill",
        blueprint=blueprint,
    )

_NOT_CALLED_MSG = "Skill must not call importlib.metadata itself"


# pytest  ######################################################################
class TestVersionInjection:

    def test_render_frontmatter_uses_injected_version(_):
        skill = Skill(name="test-skill", description="d", version="1.2.3")

        with patch(
            "importlib.metadata.version",
            side_effect=AssertionError(_NOT_CALLED_MSG),
        ):
            frontmatter = yaml.safe_load(skill._render_frontmatter())

        assert frontmatter["metadata"]["version"] == "1.2.3"

    def test_from_exportable_threads_version(_):
        blueprint = _dummy_blueprint()

        registry = _dummy_registry(blueprint)

        with patch(_REGISTRY_RENDER_PROMPT, return_value="body"):
            skill = Skill.from_exportable(registry, version="1.2.3")

        assert skill.version == "1.2.3"
        assert skill.description == "d"
        assert skill.body == "body"

    def test_from_exportable_threads_render_profile(_):
        blueprint = _dummy_blueprint()

        registry = _dummy_registry(blueprint)
        render_profile = RenderProfile(
            variants=("Claude", "ClaudeCowork"),
            conditional_sidecars=("[Claude]", "[ClaudeCowork]"),
            sparseness=0,
            show_comment=False,
        )

        with patch(_REGISTRY_RENDER_PROMPT, return_value="body") as render:
            Skill.from_exportable(registry, render_profile=render_profile)

        render.assert_called_once_with(
            blueprint,
            profile=dataclasses.replace(
                registry.render_profile.merge(render_profile),
                display_name=registry.display_name,
            )
        )

    def test_from_exportable_without_render_profile_uses_registry_defaults(
        _,
    ):
        blueprint = _dummy_blueprint()

        registry = _dummy_registry(blueprint)

        with patch(_REGISTRY_RENDER_PROMPT, return_value="body") as render:
            Skill.from_exportable(registry)

        render.assert_called_once_with(
            blueprint,
            profile=dataclasses.replace(
                registry.render_profile, display_name=registry.display_name
            )
        )

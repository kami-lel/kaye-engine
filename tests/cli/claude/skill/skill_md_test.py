"""
skill_md_test.py

Unit Tests (using pytest) for:

Skill version injection
"""

from unittest.mock import MagicMock, patch

import yaml

from kaye_engine.cli.claude.skill.skill_md import Skill
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.render_profile import RenderProfile


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
        blueprint = MagicMock()
        blueprint.sidecars.description = "d"
        blueprint.sidecars.when_to_use = "w"
        blueprint.sidecars.globs = []
        blueprint.render_prompt.return_value = "body"

        registry = _dummy_registry(blueprint)

        skill = Skill.from_exportable(registry, version="1.2.3")

        assert skill.version == "1.2.3"

    def test_from_exportable_threads_render_profile(_):
        blueprint = MagicMock()
        blueprint.sidecars.description = "d"
        blueprint.sidecars.when_to_use = "w"
        blueprint.sidecars.globs = []
        blueprint.render_prompt.return_value = "body"

        registry = _dummy_registry(blueprint)
        render_profile = RenderProfile(
            variants=("Claude", "ClaudeCowork"),
            conditional_sidecars=("[Claude]", "[ClaudeCowork]"),
            sparseness=0,
            show_comment=False,
        )

        Skill.from_exportable(registry, render_profile=render_profile)

        blueprint.render_prompt.assert_called_once_with(
            profile=registry.render_profile.merge(render_profile)
        )

    def test_from_exportable_without_render_profile_uses_registry_defaults(
        _,
    ):
        blueprint = MagicMock()
        blueprint.sidecars.description = "d"
        blueprint.sidecars.when_to_use = "w"
        blueprint.sidecars.globs = []
        blueprint.render_prompt.return_value = "body"

        registry = _dummy_registry(blueprint)

        Skill.from_exportable(registry)

        blueprint.render_prompt.assert_called_once_with(
            profile=registry.render_profile
        )

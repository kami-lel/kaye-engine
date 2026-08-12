"""
skill_md_test.py

Unit Tests (using pytest) for:

Skill version injection
"""

from unittest.mock import MagicMock, patch

import yaml

from kaye_engine.cli.claude.skill.skill_md import Skill
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.claude_surface import ClaudeSurface

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
        blueprint.generate_prompt.return_value = "body"

        registry = BlueprintRegistry(
            canonical_name="test-skill",
            display_name="Test Skill",
            blueprint=blueprint,
        )

        skill = Skill.from_exportable(registry, version="1.2.3")

        assert skill.version == "1.2.3"

    def test_from_exportable_threads_surface(_):
        blueprint = MagicMock()
        blueprint.sidecars.description = "d"
        blueprint.sidecars.when_to_use = "w"
        blueprint.sidecars.globs = []
        blueprint.generate_prompt.return_value = "body"

        registry = BlueprintRegistry(
            canonical_name="test-skill",
            display_name="Test Skill",
            blueprint=blueprint,
        )

        Skill.from_exportable(registry, surface=ClaudeSurface.cowork)

        _, kwargs = blueprint.generate_prompt.call_args
        assert kwargs["affordances"] == ClaudeSurface.cowork.as_affordances()
        assert (
            kwargs["contains_sidecars"]
            == ClaudeSurface.cowork.as_contained_sidecars()
        )

    def test_from_exportable_without_surface_disables_affordances(_):
        blueprint = MagicMock()
        blueprint.sidecars.description = "d"
        blueprint.sidecars.when_to_use = "w"
        blueprint.sidecars.globs = []
        blueprint.generate_prompt.return_value = "body"

        registry = BlueprintRegistry(
            canonical_name="test-skill",
            display_name="Test Skill",
            blueprint=blueprint,
        )

        Skill.from_exportable(registry)

        _, kwargs = blueprint.generate_prompt.call_args
        assert kwargs["affordances"] is None
        assert kwargs["contains_sidecars"] == ()

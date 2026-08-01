"""
skill_md_test.py

Unit Tests (using pytest) for:

Skill version injection
"""

from unittest.mock import MagicMock, patch

import yaml

from kaye_engine.cli.claude.skill.skill_md import Skill

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

    def test_from_registry_threads_version(_):
        registry = MagicMock()
        registry.skill_name = "test-skill"
        registry.blueprint.sidecars.description = "d"
        registry.blueprint.sidecars.when_to_use = "w"
        registry.blueprint.sidecars.globs = []
        registry.user_invokable = True
        registry.blueprint.generate_prompt.return_value = "body"

        skill = Skill.from_registry(registry, version="1.2.3")

        assert skill.version == "1.2.3"

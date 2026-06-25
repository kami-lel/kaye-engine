"""
corpus_skill_frontmatter_test.py

Validates that every exported agent skill SKILL.md file has frontmatter
fields that conform to the agentskills.io specification
(https://agentskills.io/specification).

Parametrized over ``ALL_CLAUDE_SKILL_NAMES`` — the canonical set of every
blueprint, prompt, and abbreviation skill exported by ``kaye claude skill``.
Deriving the cases from that list (rather than hand-writing one test per
skill) keeps the suite exhaustive automatically: any skill newly added to the
corpus is covered without touching this file.

Each case reads the real on-disk SKILL.md from ``testee_skills_folder`` and
validates its frontmatter through ``SkillMDFileFrontmatterValidator``.
"""

from pathlib import Path

import pytest
import yaml

from tests.cli.a import ALL_CLAUDE_SKILL_NAMES
from tests.corpus import SkillMDFileFrontmatterValidator


# Pytest unit tests  ###########################################################


class TestSkillFrontmatter:  # =================================================

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_frontmatter_conforms_to_spec(_, testee_skills_folder, skill_name):
        skill_file = Path(testee_skills_folder) / skill_name / "SKILL.md"
        assert skill_file.is_file(), "missing {}/SKILL.md".format(skill_name)

        parts = skill_file.read_text().split("---", 2)
        data = yaml.safe_load(parts[1]) or {}

        # raises pydantic ValidationError if any field violates the spec,
        # including the now-required non-empty description
        SkillMDFileFrontmatterValidator.from_frontmatter(data)

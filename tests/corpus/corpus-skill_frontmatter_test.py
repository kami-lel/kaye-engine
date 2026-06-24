"""
corpus_skill_frontmatter_test.py

Validates that every exported agent skill SKILL.md file has frontmatter
fields that conform to the agentskills.io specification
(https://agentskills.io/specification).

Each test calls ``assert_agent_skill_frontmatter_limit``, a generic helper
that reads the actual exported file and validates it through
``SkillMDFileFrontmatterValidator``.  This mirrors the ``TestHeader`` pattern
in ``tests/cli/a/s/<group>/`` tests but exercises the real on-disk output
of ``kaye claude skill`` rather than constructing the validator from an
in-memory blueprint object.
"""

from pathlib import Path

import yaml

from tests.corpus import SkillMDFileFrontmatterValidator


# generic validator  ###########################################################


def assert_agent_skill_frontmatter_limit(
    skill_name: str, skills_folder
) -> bool:
    """
    Validate that a skill's SKILL.md frontmatter fields conform to the
    agentskills.io specification (https://agentskills.io/specification).

    Checks field presence, types, and character limits:

    - ``name``: required, 1–64 chars, ``^[a-z0-9]([a-z0-9]|-[a-z0-9])*$``
    - ``description``: optional, max 1024 chars
    - ``compatibility``: optional, max 500 chars
    - ``license``, ``metadata``, ``allowed-tools``, ``user-invocable``,
      ``when_to_use``, ``paths``: optional, type-checked

    Mirrors the per-skill ``TestHeader`` pattern across
    ``tests/cli/a/s/<group>/``, but reads from the actual exported file
    via ``testee_skills_folder`` rather than constructing the validator from
    an in-memory blueprint.

    :param skill_name: kebab-slug folder name under skills_folder
    :param skills_folder: exported skills root directory
    :return: True if all frontmatter fields pass spec constraints
    """
    skill_file = Path(skills_folder) / skill_name / "SKILL.md"
    content = skill_file.read_text()
    parts = content.split("---", 2)
    data = yaml.safe_load(parts[1]) or {}
    try:
        SkillMDFileFrontmatterValidator.from_frontmatter(data)
        return True
    except Exception:
        return False


# exportable blueprints  #######################################################


def test_date_and_time_format(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "date-and-time-format", testee_skills_folder
    )


def test_numerical_values_with_units(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "numerical-values-with-units", testee_skills_folder
    )


def test_annotation_markers(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "annotation-markers", testee_skills_folder
    )


def test_project_structure(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "project-structure", testee_skills_folder
    )


def test_project_readme_writer(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "project-readme-writer", testee_skills_folder
    )


def test_project_changelog_writer(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "project-changelog-writer", testee_skills_folder
    )


def test_project_agents_writer(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "project-agents-writer", testee_skills_folder
    )


def test_project_semantic_versioning(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "project-semantic-versioning", testee_skills_folder
    )


def test_kaye_peer_coder(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "kaye-peer-coder", testee_skills_folder
    )


def test_coder_bash(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-bash", testee_skills_folder
    )


def test_coder_c(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-c", testee_skills_folder
    )


def test_coder_cpp(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-cpp", testee_skills_folder
    )


def test_coder_unreal_engine(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-unreal-engine", testee_skills_folder
    )


def test_coder_c_sharp(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-c-sharp", testee_skills_folder
    )


def test_coder_unity_engine(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-unity-engine", testee_skills_folder
    )


def test_coder_gdscript(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-gdscript", testee_skills_folder
    )


def test_coder_html(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-html", testee_skills_folder
    )


def test_coder_javascript_and_typescript(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-javascript-and-typescript", testee_skills_folder
    )


def test_coder_python(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-python", testee_skills_folder
    )


def test_coder_python_docstring_style(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-python-docstring-style", testee_skills_folder
    )


def test_coder_python_testing_guidelines(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "coder-python-testing-guidelines", testee_skills_folder
    )


def test_style_guide_capitalization(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "style-guide-capitalization", testee_skills_folder
    )


def test_style_guide_briefness_style(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "style-guide-briefness-style", testee_skills_folder
    )


def test_style_guide_good_writing(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "style-guide-good-writing", testee_skills_folder
    )


def test_agent_behavior(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "agent-behavior", testee_skills_folder
    )


def test_prompt_writer(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "prompt-writer", testee_skills_folder
    )


def test_skill_description_writer(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "skill-description-writer", testee_skills_folder
    )


def test_international_phonetic_alphabet(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "international-phonetic-alphabet", testee_skills_folder
    )


def test_art_tutor(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "art-tutor", testee_skills_folder
    )


def test_assistant_barista(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "assistant-barista", testee_skills_folder
    )


def test_deutschlehrer(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "deutschlehrer", testee_skills_folder
    )


def test_editor(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "editor", testee_skills_folder
    )


def test_librarian(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "librarian", testee_skills_folder
    )


def test_secretary(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "secretary", testee_skills_folder
    )


def test_tarot_reader(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "tarot-reader", testee_skills_folder
    )


# prompts blueprints  ##########################################################


def test_create_readme(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "create-readme", testee_skills_folder
    )


def test_maintain_readme(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "maintain-readme", testee_skills_folder
    )


def test_create_changelog(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "create-changelog", testee_skills_folder
    )


def test_maintain_changelog(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "maintain-changelog", testee_skills_folder
    )


def test_create_agents_and_context(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "create-agents-and-context", testee_skills_folder
    )


def test_maintain_agents_and_context(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "maintain-agents-and-context", testee_skills_folder
    )


def test_create_docs(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "create-docs", testee_skills_folder
    )


def test_maintain_docs(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "maintain-docs", testee_skills_folder
    )


def test_initialize_project(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "initialize-project", testee_skills_folder
    )


def test_compact_with_maintenance(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "compact-with-maintenance", testee_skills_folder
    )


def test_prepare_for_feature_finish(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "prepare-for-feature-finish", testee_skills_folder
    )


def test_prepare_for_version_release(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "prepare-for-version-release", testee_skills_folder
    )


# abbrs  #######################################################################


def test_abbr_programming_language_codes(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-programming-language-codes", testee_skills_folder
    )


def test_abbr_natural_language_codes(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-natural-language-codes", testee_skills_folder
    )


def test_abbr_units_of_measure(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-units-of-measure", testee_skills_folder
    )


def test_abbr_currency_symbols(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-currency-symbols", testee_skills_folder
    )


def test_abbr_single_character(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-single-character", testee_skills_folder
    )


def test_abbr_emoji(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-emoji", testee_skills_folder
    )


def test_abbr_prefixes(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-prefixes", testee_skills_folder
    )


def test_abbr_suffixes(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-suffixes", testee_skills_folder
    )


def test_abbr_symbols(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-symbols", testee_skills_folder
    )


def test_abbr_starts_with_digits(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-digits-0-9", testee_skills_folder
    )


def test_abbr_starts_with_a(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-a", testee_skills_folder
    )


def test_abbr_starts_with_b(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-b", testee_skills_folder
    )


def test_abbr_starts_with_c(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-c", testee_skills_folder
    )


def test_abbr_starts_with_d(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-d", testee_skills_folder
    )


def test_abbr_starts_with_e(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-e", testee_skills_folder
    )


def test_abbr_starts_with_f(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-f", testee_skills_folder
    )


def test_abbr_starts_with_g(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-g", testee_skills_folder
    )


def test_abbr_starts_with_h(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-h", testee_skills_folder
    )


def test_abbr_starts_with_i(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-i", testee_skills_folder
    )


def test_abbr_starts_with_j(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-j", testee_skills_folder
    )


def test_abbr_starts_with_k(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-k", testee_skills_folder
    )


def test_abbr_starts_with_l(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-l", testee_skills_folder
    )


def test_abbr_starts_with_m(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-m", testee_skills_folder
    )


def test_abbr_starts_with_n(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-n", testee_skills_folder
    )


def test_abbr_starts_with_o(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-o", testee_skills_folder
    )


def test_abbr_starts_with_p(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-p", testee_skills_folder
    )


def test_abbr_starts_with_q(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-q", testee_skills_folder
    )


def test_abbr_starts_with_r(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-r", testee_skills_folder
    )


def test_abbr_starts_with_s(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-s", testee_skills_folder
    )


def test_abbr_starts_with_t(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-t", testee_skills_folder
    )


def test_abbr_starts_with_u(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-u", testee_skills_folder
    )


def test_abbr_starts_with_v(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-v", testee_skills_folder
    )


def test_abbr_starts_with_w(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-w", testee_skills_folder
    )


def test_abbr_starts_with_x(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-x", testee_skills_folder
    )


def test_abbr_starts_with_y(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-y", testee_skills_folder
    )


def test_abbr_starts_with_z(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-z", testee_skills_folder
    )


def test_abbr_starts_with_non_alphanumeric(testee_skills_folder):
    assert assert_agent_skill_frontmatter_limit(
        "abbr-starts-with-non-alphanumeric", testee_skills_folder
    )

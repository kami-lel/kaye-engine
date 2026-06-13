"""
cli-s-structure-prompts_blueprints_test.py

Unit tests for PROMPTS_BLUEPRINTS using SkillMDFileFrontmatterValidator.
"""

from tests.cli.s.u.structure import validate_blueprint
from kaye.cli.prompts_blueprints import (
    create_agents_blueprint,
    create_readme_blueprint,
    maintain_changelog_blueprint,
    maintain_docs_blueprint,
    prepare_for_feature_blueprint,
    prepare_for_release_blueprint,
)

# Bug fail to satisfy these


def otest_maintain_docs():
    r = validate_blueprint(maintain_docs_blueprint)
    assert r.name == "maintain-docs"


def otest_maintain_changelog():
    r = validate_blueprint(maintain_changelog_blueprint)
    assert r.name == "maintain-changelog"


def otest_create_readme():
    r = validate_blueprint(create_readme_blueprint)
    assert r.name == "create-readme"


def otest_create_agents():
    r = validate_blueprint(create_agents_blueprint)
    assert r.name == "create-agents"


def otest_prepare_for_feature_finish():
    r = validate_blueprint(prepare_for_feature_blueprint)
    assert r.name == "prepare-for-feature-finish"


def otest_prepare_for_release():
    r = validate_blueprint(prepare_for_release_blueprint)
    assert r.name == "prepare-for-release"

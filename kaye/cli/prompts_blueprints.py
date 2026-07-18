"""
prompts_blueprints.py

define ``PROMPTS_BLUEPRINTS``
"""

from kaye.prompt import load_prompt_corpus_tree
from kaye.prompt.prompt_blueprint import PromptBlueprint

_prompt_node = load_prompt_corpus_tree()["Projects"]
# blueprints  ##################################################################


# Create README
create_readme_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Create README"], recursively=True
)

# Maintain README
maintain_readme_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Maintain README"]
)

# Create CHANGELOG
create_changelog_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Create CHANGELOG"]
)

# Maintain CHANGELOG
maintain_changelog_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Maintain CHANGELOG"], recursively=True
)

# Create AGENTS and CONTEXT
create_agents_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Create AGENTS and CONTEXT"], recursively=True
)

# Maintain AGENTS and CONTEXT
maintain_agents_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Maintain AGENTS and CONTEXT"]
)

# Create Docs
create_docs_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Create Docs"]
)

# Maintain Docs
maintain_docs_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Maintain Docs"], recursively=True
)

# Initialize Project
initialize_project_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Initialize Project"]
)

# Prepare for Feature Landing
prepare_for_feature_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Prepare for Feature Landing"]
)

# Prepare for Version Release
prepare_for_release_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Prepare for Version Release"]
)

# Plan for Step By Step
plan_step_by_step_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Plan for Step By Step"], recursively=True
)

# Resolve Merge Conflict
resolve_merge_conflict_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Resolve Merge Conflict"], recursively=True
)

# Gap Review
gap_review_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Gap Review"], recursively=True
)

# Entry Point  #################################################################

# prompts blueprints used by continue export & skill export
PROMPTS_BLUEPRINTS = [
    create_readme_blueprint,
    maintain_readme_blueprint,
    create_changelog_blueprint,
    maintain_changelog_blueprint,
    create_agents_blueprint,
    maintain_agents_blueprint,
    create_docs_blueprint,
    maintain_docs_blueprint,
    initialize_project_blueprint,
    prepare_for_feature_blueprint,
    prepare_for_release_blueprint,
    plan_step_by_step_blueprint,
    resolve_merge_conflict_blueprint,
    gap_review_blueprint,
]

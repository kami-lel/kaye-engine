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

# Compact with Maintenance
compact_with_maintenance_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Compact with Maintenance"]
)

# Prepare for Feature Finish
prepare_for_feature_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Prepare for Feature Finish"]
)

# Prepare for Version Release
prepare_for_release_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Prepare for Version Release"]
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
    compact_with_maintenance_blueprint,
    prepare_for_feature_blueprint,
    prepare_for_release_blueprint,
]

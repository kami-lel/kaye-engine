"""
prompts_blueprints.py

define ``PROMPTS_BLUEPRINTS``
"""

from kaye.prompt import load_prompt_corpus_tree
from kaye.prompt.prompt_blueprint import PromptBlueprint

_prompt_node = load_prompt_corpus_tree()["Projects"]["project prompts"]
# blueprints  ##################################################################


# maintain docs
_maintain_docs_node = _prompt_node["Maintain Docs"]
maintain_docs_blueprint = PromptBlueprint.create_from_node(
    _maintain_docs_node, recursively=True
)

# maintain changelog
_maintain_changelog_node = _prompt_node["Maintain CHANGELOG"]
maintain_changelog_blueprint = PromptBlueprint.create_from_node(
    _maintain_changelog_node, recursively=True
)


# create README
create_readme_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Create README"]
)


# create AGENTS
create_agents_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Create AGENTS"]
)


# Prepare for Feature Finish
prepare_for_feature_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Prepare for Feature Finish"]
)
prepare_for_feature_blueprint.checkmark(
    _maintain_changelog_node["edit CHANGELOG"]
)
prepare_for_feature_blueprint.display_name = "Prepare for Feature Finish"


# Prepare for Release
prepare_for_release_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Prepare for Release"]
)
prepare_for_release_blueprint.checkmark(
    _maintain_changelog_node["edit CHANGELOG"]
)
prepare_for_release_blueprint.display_name = "Prepare for Release"

# Entry Point  #################################################################

# prompts blueprints used by continue export & skill export
PROMPTS_BLUEPRINTS = [
    maintain_docs_blueprint,
    maintain_changelog_blueprint,
    create_readme_blueprint,
    create_agents_blueprint,
    prepare_for_feature_blueprint,
    prepare_for_release_blueprint,
]

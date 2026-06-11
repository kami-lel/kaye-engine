"""
prompt_export.py

define ``export_prompts``
"""

from pathlib import Path

from kaye.prompt.prompt_blueprint import PromptBlueprint
from kaye.cli.metadata_md_file import MetadataMDFile

# blueprints  ##################################################################


_prompt_node = PromptBlueprint.create_empty_blueprint().corpus["Continue"][
    "Continue Prompts"
]


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

# resolve annotation markers
resolve_markers_blueprint = PromptBlueprint.create_from_node(
    _prompt_node["Resolve Annotation Markers"]
)
PromptBlueprint.create_empty_blueprint()


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


# constants  ###################################################################


FILENAME2BLUEPRINT = {
    "maintain_docs": maintain_docs_blueprint,
    "maintain_changelog": maintain_changelog_blueprint,
    "resolve_annotation_markers": resolve_markers_blueprint,
    "create_readme": create_readme_blueprint,
    "create_agents": create_agents_blueprint,
    "prepare_for_release": prepare_for_release_blueprint,
    "prepare_for_feature_finish": prepare_for_feature_blueprint,
}


# Entry Point  #################################################################
def export_prompts(prompts_folder):
    """
    export all prompts as Continue Prompts files


    :param prompts_folder: destination folder for prompt rule files
    :type prompts_folder: Path-like
    """
    folder = Path(prompts_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    for k, bp in FILENAME2BLUEPRINT.items():
        filename = k + ".md"
        file_path = prompts_folder / filename

        print("update prompt:\t{}".format(filename))

        with MetadataMDFile(file_path, blueprint=bp) as md_file:
            md_file.always_apply = False
            md_file.invokable = True
            md_file.write_continue_frontmatter_and_content()

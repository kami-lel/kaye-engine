"""
prompt_export.py

define ``export_prompts``
"""

from pathlib import Path

from kaye.prompt.prompt_blueprint import PromptBlueprint

from kaye.continue_export.rule_file import RuleFile

# blueprints  ##################################################################


_prompt_node = PromptBlueprint.create_empty_blueprint().corpus["Continue"][
    "Continue Prompts"
]


# maintain docs
maintain_docs_blueprint = PromptBlueprint.create_empty_blueprint()
maintain_docs_blueprint.checkmark(_prompt_node["Maintain Docs"])
maintain_docs_blueprint.display_name = "Maintain Docs"

# maintain changelog
maintain_changelog_blueprint = PromptBlueprint.create_empty_blueprint()
maintain_changelog_blueprint.checkmark(_prompt_node["Maintain Changelog"])
maintain_changelog_blueprint.display_name = "Maintain Changelog"

# resolve annotation markers
resolve_markers_blueprint = PromptBlueprint.create_empty_blueprint()
resolve_markers_blueprint.checkmark(_prompt_node["Resolve Annotation Markers"])
resolve_markers_blueprint.display_name = "Resolve Annotation Markers"

# resolve annotation markers
prepare_for_release_blueprint = PromptBlueprint.create_empty_blueprint()
prepare_for_release_blueprint.checkmark(_prompt_node["Prepare for Release"])
prepare_for_release_blueprint.display_name = "Prepare for Release"

# create README
create_readme_blueprint = PromptBlueprint.create_empty_blueprint()
create_readme_blueprint.checkmark(_prompt_node["Create README"])
create_readme_blueprint.display_name = "Create README"


# create AGENTS
create_agents_blueprint = PromptBlueprint.create_empty_blueprint()
create_agents_blueprint.checkmark(_prompt_node["Create AGENTS"])
create_agents_blueprint.display_name = "Create AGENTS"


# constants  ###################################################################


FILENAME2BLUEPRINT = {
    "maintain_docs": maintain_docs_blueprint,
    "maintain_changelog": maintain_changelog_blueprint,
    "resolve_annotation_markers": resolve_markers_blueprint,
    "prepare_for_release": prepare_for_release_blueprint,
    "create_readme": create_readme_blueprint,
    "create_agents": create_agents_blueprint,
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

        with RuleFile(file_path, encoding="utf-8") as rule:
            rule.name = bp.display_name
            rule.description = bp.description
            rule.always_apply = False
            rule.invokable = True
            rule.write_prefix()
            rule.write(bp.generate_prompt())

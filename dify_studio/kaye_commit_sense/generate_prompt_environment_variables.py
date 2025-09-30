"""
generate prompt Environment Variables (prefixed with ``prompt_``) content
for dify app
"""

from pathlib import Path

from kaye.gen_prompt import load_empty_prompt_blueprint

PRIMARY_MESSAGE_NAME = "primary_message"
PER_FILE_LONG_NAME = "per_file_summary_long"
PER_FILE_SHORT_NAME = "per_file_summary_short"

# shared across 3 prompts
COMMON_NODES = (
    "kaye-commit-sense",
    "Commentary Case",
    "Briefness Style",
)
PER_FILE_COMMON_NODES = (
    "Annotation Markers",
    "kaye-commit-sense-per-file",
)


def _print_debug_preview_tree(blueprint, filename):
    # todo printing of tree only when debugging
    print()
    print((filename + "  ").ljust(80, "-"))
    print(
        blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
    )


def _generate_path(blueprint_name):
    folder = Path(__file__).parent
    path = (folder / "prompt_{}.md".format(blueprint_name)).resolve()
    return path


if __name__ == "__main__":

    with open(
        _generate_path(PRIMARY_MESSAGE_NAME), "w", encoding="utf-8"
    ) as file:
        blueprint = load_empty_prompt_blueprint()
        blueprint.blueprint_name = PRIMARY_MESSAGE_NAME

        blueprint.enabled_nodes_names.extend(COMMON_NODES)
        blueprint.enabled_nodes_names.append(
            "kaye-commit-sense-primary-message-task"
        )

        _print_debug_preview_tree(blueprint, PRIMARY_MESSAGE_NAME)
        file.write(blueprint.generate_prompt())

    with open(
        _generate_path(PER_FILE_LONG_NAME), "w", encoding="utf-8"
    ) as file:
        blueprint = load_empty_prompt_blueprint()
        blueprint.blueprint_name = PER_FILE_LONG_NAME

        blueprint.enabled_nodes_names.extend(COMMON_NODES)
        blueprint.enabled_nodes_names.extend(PER_FILE_COMMON_NODES)
        blueprint.enabled_nodes_names.append("kaye-commit-sense-per-file-long")

        _print_debug_preview_tree(blueprint, PER_FILE_LONG_NAME)
        file.write(blueprint.generate_prompt())

    with open(
        _generate_path(PER_FILE_SHORT_NAME), "w", encoding="utf-8"
    ) as file:
        blueprint = load_empty_prompt_blueprint()
        blueprint.blueprint_name = PER_FILE_SHORT_NAME

        blueprint.enabled_nodes_names.extend(COMMON_NODES)
        blueprint.enabled_nodes_names.extend(PER_FILE_COMMON_NODES)
        blueprint.enabled_nodes_names.append(
            "kaye-commit-sense-per-file-short"
        )

        _print_debug_preview_tree(blueprint, PER_FILE_SHORT_NAME)
        file.write(blueprint.generate_prompt())

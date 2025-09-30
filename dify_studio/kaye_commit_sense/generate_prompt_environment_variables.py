"""
generate prompt Environment Variables (prefixed with ``prompt_``) content
for dify app
"""

from pathlib import Path

from kaye.gen_prompt import load_empty_prompt_blueprint

PRIMARY_MESSAGE_FILENAME = "prompt_primary_message.md"
PER_FILE_LONG_FILENAME = "prompt_per_file_summary_long.md"
PER_FILE_SHORT_FILENAME = "prompt_per_file_summary_short.md"

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


if __name__ == "__main__":
    folder = Path(__file__).parent

    with open(
        (folder / PRIMARY_MESSAGE_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_empty_prompt_blueprint()

        # add style nodes
        blueprint.enabled_nodes_names.extend(COMMON_NODES)
        blueprint.enabled_nodes_names.append(
            "kaye-commit-sense-primary-message-task"
        )

        _print_debug_preview_tree(blueprint, PRIMARY_MESSAGE_FILENAME)
        file.write(blueprint.generate_prompt())

    with open(
        (folder / PER_FILE_LONG_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_empty_prompt_blueprint()

        # add style nodes
        blueprint.enabled_nodes_names.extend(COMMON_NODES)
        blueprint.enabled_nodes_names.extend(PER_FILE_COMMON_NODES)
        blueprint.enabled_nodes_names.append("kaye-commit-sense-per-file-long")

        _print_debug_preview_tree(blueprint, PER_FILE_LONG_FILENAME)
        file.write(blueprint.generate_prompt())

    with open(
        (folder / PER_FILE_SHORT_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_empty_prompt_blueprint()

        # add style nodes
        blueprint.enabled_nodes_names.extend(COMMON_NODES)
        blueprint.enabled_nodes_names.extend(PER_FILE_COMMON_NODES)
        blueprint.enabled_nodes_names.append(
            "kaye-commit-sense-per-file-short"
        )

        _print_debug_preview_tree(blueprint, PER_FILE_SHORT_FILENAME)
        file.write(blueprint.generate_prompt())

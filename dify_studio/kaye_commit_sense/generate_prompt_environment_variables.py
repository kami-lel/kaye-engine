"""
generate prompt Environment Variables (prefixed with ``prompt_``) content
for dify app
"""

from pathlib import Path

from kaye.gen_prompt import load_empty_prompt_blueprint

# todo printing of tree only when debugging

PRIMARY_MESSAGE_FILENAME = "prompt_primary_message.md"
PER_FILE_LONG_FILENAME = "prompt_per_file_summary_long.md"
PER_FILE_SHORT_FILENAME = "prompt_per_file_summary_short.md"

# shared across 3 prompts
MESSAGE_STYLE_NODES = [
    "Commentary Case",
    "Briefness Style",
]


if __name__ == "__main__":
    folder = Path(__file__).parent

    with open(
        (folder / PRIMARY_MESSAGE_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_empty_prompt_blueprint()
        blueprint.enabled_nodes_names.extend(MESSAGE_STYLE_NODES)
        # print for debug
        print((PRIMARY_MESSAGE_FILENAME + "  ").ljust(80, "-"))
        print(
            blueprint.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
        )
        file.write("")  # TODO

    with open(
        (folder / PER_FILE_LONG_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        file.write("")  # TODO

    with open(
        (folder / PER_FILE_SHORT_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        file.write("")  # TODO

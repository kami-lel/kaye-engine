"""
generate conversation variable ``prompt_extract_info``
"""

from pathlib import Path

from kaye.gen_prompt import load_empty_prompt_blueprint

if __name__ == "__main__":
    with open(
        Path(__file__).parent / "prompt_extract_info.md",
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_empty_prompt_blueprint()
        blueprint.blueprint_name = "kaye-cash-tracker-extract-info"

        blueprint.enabled_nodes_names.append("kaye-cash-tracker-extract-info")

        print(
            blueprint.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
        )

        file.write(blueprint.generate_prompt())

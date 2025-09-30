"""
generate conversation variable ``prompt_extract_info``
"""

from pathlib import Path

from kaye.gen_prompt import load_embedded_prompt_blueprint

if __name__ == "__main__":
    with open(
        Path(__file__).parent / "prompt_extract_info.md",
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_embedded_prompt_blueprint()
        blueprint.blueprint_name = "Kaye Cash Tracker extract info"

        # TODO

        file.write(blueprint.generate_prompt())

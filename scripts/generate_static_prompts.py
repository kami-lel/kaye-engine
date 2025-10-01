"""
Generate Static Prompt Files For Embedded Prompt Blueprints

This script iterates over all embedded prompt blueprints, generates each
prompt via the load_embedded_prompt_blueprint function, and writes the
output as markdown files to the static prompts directory.
"""

from pathlib import Path

from kaye.gen_prompt import (
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
)

from tests.static_prompts import STATIC_PROMPT_FILE_EXTENSION

# relative path to folder static_prompts from this script
STATIC_PROMPTS_REL_PATH = "../tests/static_prompts"


if __name__ == "__main__":
    blueprints_names = get_embedded_prompt_blueprints_names()

    # resolve path to static prompt folder
    static_prompts_folder_path = (
        Path(__file__).parent / STATIC_PROMPTS_REL_PATH
    ).resolve()

    for name in blueprints_names:
        # generate each prompt and write to file
        file_path = static_prompts_folder_path / (
            name + STATIC_PROMPT_FILE_EXTENSION
        )
        blueprint = load_embedded_prompt_blueprint(name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(blueprint.generate_prompt(hide_comment=True))


# HACK deprecation?

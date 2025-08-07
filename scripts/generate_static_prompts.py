# TODO docstring


import os
from kaye.gen_prompt import (
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
)

# relative path to folder static_prompts
STATIC_PROMPTS_REL_PATH = "../tests/static_prompts"

if __name__ == "__main__":

    blueprints_names = get_embedded_prompt_blueprints_names(
        exclude_technical_blueprint=False
    )
    static_prompts_folder_path = os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), STATIC_PROMPTS_REL_PATH
        )
    )

    for blueprint in blueprints_names:
        content = load_embedded_prompt_blueprint(blueprint)
        # TODO continue

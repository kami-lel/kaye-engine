# Fixme detect blueprints files as .kaye_blueprint


from kaye.gen_prompt import (
    get_embedded_prompt_blueprints_folder_path,
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
)

if __name__ == "__main__":
    # get names of all blueprints
    blueprints = get_embedded_prompt_blueprints_names(
        exclude_technical_blueprint=True
    )

    # folder containing all blueprints .txt files
    folder_path = get_embedded_prompt_blueprints_folder_path()

    for blueprint_name in blueprints:
        blueprint = load_embedded_prompt_blueprint(blueprint_name)

        file_path = folder_path / "{}.txt".format(blueprint_name)

        with open(file_path, "w", encoding="utf-8") as file:
            # Todo print out to console
            content = blueprint.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
            file.write(content)

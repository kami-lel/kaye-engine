"""
test function ``load_embedded_prompt_blueprint()``
"""

from pathlib import Path

from kaye.gen_prompt import (
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
    PromptBlueprint,
)


class TestFull:  # special case "full"

    prompt_name = "full"

    def test_type(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    def test_generate_preview_tree(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[x]") for line in opt.splitlines())


class TestEmpty:  # special case "empty"

    prompt_name = "empty"

    def test_type(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    def test_generate_preview_tree(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[ ]") for line in opt.splitlines())

    def test_generate_prompt(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = blueprint.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""


class TestNonTech:  # test other embedded blueprints

    names = get_embedded_prompt_blueprints_names()

    def test_type(self):
        for prompt_name in self.names:
            prompt_name = load_embedded_prompt_blueprint(prompt_name)
            assert isinstance(prompt_name, PromptBlueprint)

    # test runtime generated prompts against files in .../static_prompts
    def test_generate_prompt(self):
        static_prompts_folder_path = (
            Path(__file__).parent / "../../../static_prompts"
        ).resolve()

        for prompt_name in self.names:
            blueprint = load_embedded_prompt_blueprint(prompt_name)
            opt = blueprint.generate_prompt(hide_comment=True)
            print(opt)
            assert opt == ""

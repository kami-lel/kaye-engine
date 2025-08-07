"""
test function ``load_embedded_prompt_blueprint()``
"""

from kaye.gen_prompt import load_embedded_prompt_blueprint, PromptBlueprint


class TestFull:  # special case "full"

    prompt_name = "full"

    def test_type(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    def test_repr(self):
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

    def test_repr(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[ ]") for line in opt.splitlines())

    def test_str(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = blueprint.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""


# TODO test non-tech

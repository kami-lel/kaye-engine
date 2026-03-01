"""
test function ``load_embedded_prompt_blueprint()``
"""

# FIXME

from kaye.prompt import (
    load_embedded_blueprint,
    PromptBlueprint,
)


class XTestFull:  # special case "full"

    prompt_name = "full"

    def test_type(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    def test_generate_preview_tree(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[x]") for line in opt.splitlines()[1:])

    def test_use_load(_):
        blueprint = load_full_prompt_blueprint()
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[x]") for line in opt.splitlines()[1:])


class XTestEmpty:  # special case "empty"

    prompt_name = "empty"

    def test_type(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    def test_generate_preview_tree(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[ ]") for line in opt.splitlines()[1:])

    def test_generate_prompt(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        opt = blueprint.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test_use_load(_):
        blueprint = load_empty_prompt_blueprint()
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert all(line.startswith("[ ]") for line in opt.splitlines()[1:])


class XTestChat:

    prompt_name = "chat"

    def test_type(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    def test_generate_preview_tree(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        opt = blueprint.generate_preview_tree(
            preview_line_count=0, hide_comment=True
        )
        print(opt)
        assert opt

    def test_generate_prompt(self):
        blueprint = load_embedded_blueprint(self.prompt_name)
        opt = blueprint.generate_prompt(hide_comment=True)

        print(opt)
        assert opt

"""
test function ``load_embedded_prompt_blueprint()``
"""

from kaye.gen_prompt import load_embedded_prompt_blueprint, PromptBlueprint


class TestFull:  # special case "full"

    prompt_name = "full"

    def test_type(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    # !!! this test change with prompt_corpus.md
    def test_repr(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = str(blueprint)
        print(opt)
        # BUG
        assert opt == ""


class TestConversation:

    prompt_name = "conversation"

    def test_type(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        assert isinstance(blueprint, PromptBlueprint)

    # !!! this test change with prompt_corpus.md
    def test_repr(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = blueprint.__repr__(preview_line_count=0)
        print(opt)
        # BUG
        assert opt == ""

    # !!! this test change with prompt_corpus.md
    def test_str(self):
        blueprint = load_embedded_prompt_blueprint(self.prompt_name)
        opt = str(blueprint)
        print(opt)
        # BUG
        assert opt == ""

from kaye.prompt.base_prompt_node import BasePromptNode


class UnitTestNode(BasePromptNode):

    @property
    def identifier(self):
        return self.name.upper()

    def content_lines(self, *args, **kwargs):
        return self.lines

from kaye.prompt.base_prompt_node import BasePromptNode


class UnitTestNode(BasePromptNode):

    def content_lines(self, *args, **kwargs):
        return self.lines

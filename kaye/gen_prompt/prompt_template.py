"""
define `PromptTemplate`
"""


class PromptTemplate:
    """
    _summary_

    :param full_prompt_tree: _description_
    :type full_prompt_tree: FullPromptTreeNode
    :param prompt_template_content: _description_
    :type prompt_template_content: str
    """

    @staticmethod
    def create_empty_prompt_template_from_full_prompt_tree(full_prompt_tree):
        pass  # TODO

    def __init__(self, full_prompt_tree, prompt_template_content):
        # TODO
        self._full_prompt_tree = full_prompt_tree

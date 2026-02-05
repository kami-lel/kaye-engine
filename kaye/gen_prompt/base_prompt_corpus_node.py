from anytree import Node as AnytreeNode


class BasePromptCorpusNode(AnytreeNode):

    # Todo

    def __hash__(self):
        raise NotImplementedError

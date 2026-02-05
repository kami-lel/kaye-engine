from anytree import Node as AnytreeNode


class BasePromptCorpusNode(AnytreeNode):

    # TODO

    def __hash__(self):
        raise NotImplementedError

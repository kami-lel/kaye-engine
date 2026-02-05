"""
define ``BasePromptNode``
"""

from anytree import Node as AnyTreeNode


class BasePromptNode(AnyTreeNode):

    # public API  ==============================================================

    def generate_prompt_tree_preview(
        self, content_line_count=3, content_line_width=64
    ):
        # enforce perform preview only from root
        if not self.is_root:
            raise NotImplementedError(
                "generating prompt tree preview is only possible with root node"
            )
        return ""  # TODO

    # abstract methods  ========================================================

    @property
    def name_in_lineage(self):
        """
        :return: this node's name used in ``.generate_lineage()``;
                ``""`` for root node
        :rtype: str
        """
        raise NotImplementedError

    # instance methods  ========================================================

    def generate_lineage(self):
        """
        :return: a **lineage** from root to current node (inclusively),
                represented as a ``list`` of node names,
                with node's name created from ``.name_in_lineage``;
        :rtype: list(str)
        :example:
        >>> node.generate_lineage()
        ["", "My Parent", "Myself"]
        """
        if self.is_root:
            return [""]

        ancestry_path = self.parent.generate_lineage()
        ancestry_path.append(self.name_in_lineage)
        return ancestry_path

    # magic methods  ===========================================================

    def __getitem__(self, key):
        """
        :param key:
        :type key: int or str
        :raises IndexError:
        :raises KeyError:
        :raises TypeError:
        :return: children node
        :rtype: BasePromptNode
        :example:
        >>> node[0]         # get first child
        >>> node["Info"]    # get child with name "Info"
        """
        if isinstance(key, int):  # get by index
            try:
                return self.children[key]
            except IndexError as err:
                # FIXME err msg
                raise IndexError(
                    "index out of range for PromptCorpusNode children: {}"
                    .format(key)
                ) from err

        elif isinstance(key, str):
            for child in self.children:
                if child.name == key:
                    return child
            # FIXME err msg
            raise KeyError(
                "fail to find child {} in {}".format(repr(key), repr(self))
            )

        else:
            raise TypeError(
                "{} index must be int/str: {}".format(
                    type(self).__name__, repr(key)
                )
            )

    def __hash__(self):
        return hash(tuple(self.generate_lineage()))

    def __repr__(self):
        """
        :raises NotImplementedError:
        :return: identical to ``.generate_prompt_tree_preview()``,
                only for root node
        :rtype: str
        """
        if self.is_root:
            return self.generate_prompt_tree_preview()
        return super().__repr__()

    def __str__(self):
        """
        :return:
        :rtype: str
        :example:
        >>> str(node)
        "PromptCorpusNode(Introduction#Data#Advanced)"
        """
        ancestry_path_name = "#".join(self.generate_lineage()[1:])
        return "{}({})".format(type(self).__name__, ancestry_path_name)

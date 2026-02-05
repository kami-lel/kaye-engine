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
    def __hash__(self):
        return hash(tuple(self.generate_lineage()))

    def __repr__(self):
        ancestry_path_name = "#".join(self.generate_lineage()[1:])
        return "{}({})".format(type(self).__name__, ancestry_path_name)

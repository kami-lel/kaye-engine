"""
define ``BasePromptNode``
"""

from anytree import Node as AnyTreeNode, RenderTree

__all__ = ("BasePromptNode",)


class BasePromptNode(AnyTreeNode):

    # public API  ==============================================================

    def generate_prompt_tree_preview(
        self, content_preview_lines=3, content_preview_width=64
    ):
        """
        generate **preview tree** of ``self`` as root,
        an human-readable representation


        TODO wrong

        :param preview_line_count: set maximum line count of
                *content preview* part, (excluding section heading line);
                defaults to 3
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part;
                defaults to 64.
        :type preview_line_width: int
        :return: the preview tree
        :rtype: str
        :example:
        >>> tree.generate_preview_tree()
        ○
        └── Project Title
            ├── Description
            │   A brief overview of the project, its purpose, and goals.
            ├── Installation
            │   1. Clone the repo
            │   2. Install dependencies
            │   3. Run the application
            ├── Usage
            │   Provide instructions on how to use the application.
            ├── Contributing
            │   1. Fork the repo
            │   2. Create a new branch
            │   3. Submit a pull request
            └── License
                This project is licensed under the MIT License.
        >>> tree.generate_preview_tree(preview_line_count=0)
        ○
        └── Project Title
            ├── Description
            ├── Installation
            ├── Usage
            ├── Contributing
            └── License
        """
        # enforce perform preview only from root
        if not self.is_root:
            raise NotImplementedError(
                "generating prompt tree preview is only possible with root node"
            )

        lines = []
        for pre, fill, node in RenderTree(self):  # iterate per node
            # tree structure line, i.e. line w/ node name
            lines.append(pre + node.name_in_lineage)

            # content preview part
            if content_preview_lines:
                content = node.content_lines
                if content:
                    for line in content[:content_preview_lines]:
                        lines.append((fill + line)[:content_preview_width])

        return "\n".join(lines)

    # abstract methods  ========================================================

    @property
    def name_in_lineage(self):
        """
        :return: this node's name used in ``.generate_lineage()``;
                ``""`` for root node
        :rtype: str
        """
        raise NotImplementedError

    @property
    def content_lines(self):
        """
        :return: content **lines** this node as appeared in concrete prompt;
                each element in ``list`` is a single line
        :rtype: list[str]
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

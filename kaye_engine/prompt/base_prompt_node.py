"""
base_prompt_node.py

define ``BasePromptNode``
"""

import copy

from anytree import Node as AnyTreeNode, RenderTree, PreOrderIter

__all__ = ("BasePromptNode",)


class BasePromptNode(AnyTreeNode):
    """
    abstract class of any node in the *prompt tree*
    """

    # public API  ==============================================================

    def generate_prompt_tree_preview(
        self, content_preview_lines=3, content_preview_width=64
    ):
        """
        generate a **preview** of *prompt tree*
        in human-readable representation,
        containing *content preview* part

        only applicable on **root** node


        :param content_preview_lines: set maximum line count
                (excluding section heading line) of *content preview* part;
                defaults to 3
        :type content_preview_lines: int
        :param content_preview_width: set maximum column width
                of *content preview* part;
                defaults to 64.
        :type content_preview_width: int
        :raises NotImplementedError:
        :return: the tree preview
        :rtype: str
        :example:
        >>> root.generate_prompt_tree_preview()
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

        >>> root.generate_prompt_tree_preview(content_preview_lines=0)
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
                ".generate_prompt_tree_preview() is only possible for root"
            )

        lines = []
        for pre, fill, node in RenderTree(self):  # iterate per node
            # tree structure line, i.e. line w/ node name
            lines.append(pre + node.name)

            # content preview part
            if content_preview_lines:
                content = node.content_lines()
                if content:
                    for line in content[:content_preview_lines]:
                        lines.append((fill + line)[:content_preview_width])

        return "\n".join(lines)

    # abstract methods  ========================================================

    def content_lines(self, **kwargs):
        """
        :return: content **lines** this node as appeared in concrete prompt;
                each element in ``list`` is a single line
        :rtype: list[str]
        """
        raise NotImplementedError

    def __copy__(self):
        """
        :return: a shallow copied identical node,
                but with no children and no parent (set to ``None``)
        :rtype: BasePromptNode
        """
        raise NotImplementedError

    # instance methods  ========================================================

    def generate_lineage(self):
        """
        :return: a **lineage**
                from root (exclusively) to current node (inclusively,)
                represented as a ``list`` of node's ``.name``
        :rtype: list(str)
        :example:
        >>> root.generate_lineage()
        []
        >>> node.generate_lineage()
        ["My Parent", "Myself"]
        """
        cached = self.__dict__.get("_lineage_cache")
        if cached is not None:
            return list(cached)

        if self.is_root:
            lineage = []
        else:
            lineage = self.parent.generate_lineage()
            lineage.append(self.name)

        self.__dict__["_lineage_cache"] = tuple(lineage)
        return lineage

    # magic methods  ===========================================================

    def __getitem__(self, key):
        """
        :param key: index of child; `.name` of child
        :type key: int or str
        :raises IndexError:
        :raises KeyError:
        :raises TypeError:
        :return: child node
        :rtype: BasePromptNode
        :example:
        >>> node[0]         # get first child
        >>> node["Info"]    # get child with name of "Info"
        """
        if isinstance(key, int):  # get by index
            try:
                return self.children[key]
            except IndexError as err:
                raise IndexError(
                    "index out of range for {}: {}".format(str(self), key)
                ) from err

        elif isinstance(key, str):  # get by name
            for child in self.children:
                if key == child.name:
                    return child
            raise KeyError(
                "{} contains no child with name of {}".format(self, repr(key))
            )

        else:
            raise TypeError(
                "{} index must be int/str: {}".format(
                    type(self).__name__, repr(key)
                )
            )

    def __hash__(self):
        cached = self.__dict__.get("_hash_cache")
        if cached is None:
            cached = hash(tuple(self.generate_lineage()))
            self.__dict__["_hash_cache"] = cached
        return cached

    def __eq__(self, other):
        """
        :param other:
        :type other: BasePromptNode
        :return: whether 2 nodes has the same lineage;
                if both nodes are roots,
                test whether 2 trees are identical in node name structure
                (node content is irrelevant)
        :rtype: bool
        """
        if not isinstance(other, BasePromptNode):
            return NotImplemented

        if self.is_root and other.is_root:
            return all(
                hash(a) == hash(b)
                for a, b in zip(PreOrderIter(self), PreOrderIter(other))
            )

        else:
            return hash(self) == hash(other)

    def __deepcopy__(self, memo):
        """
        :param memo:
        :type memo:
        :return: a deep copy with all descendants also copied
        :rtype: BasePromptNode
        """
        copied = copy.copy(self)

        # attach children
        for child in self.children:
            copied_child = copy.deepcopy(child)
            copied_child.parent = copied

        return copied

    # str-related  *************************************************************

    def __repr__(self):
        if self.is_root:
            return self.generate_prompt_tree_preview()
        return super().__repr__()

    def __str__(self):
        """
        :return:
        :rtype: str

        :example:
        >>> str(root)
        "PromptCorpusNode()"
        >>> str(corpus_node)
        "PromptCorpusNode(Introduction#Data#Advanced)"
        >>> str(abbr_node)
        "ShorthandNode(Introduction#Data#(decode-only-abbr))"
        """
        lineage = "#".join(node.name for node in self.path[1:])
        return "{}({})".format(type(self).__name__, lineage)

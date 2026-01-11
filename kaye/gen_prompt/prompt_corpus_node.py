"""
define ``PromptCorpusNode``
"""

import re

from anytree import Node as AnytreeNode, RenderTree

# section heading prefix used for parsing .md file of prompt corpus
HEADING_PREFIX = "#"
ROOT_NODE_NAME = "○"  # placeholder name for root node

__all__ = ("PromptCorpusNode",)


class PromptCorpusNode(AnytreeNode):
    """
    A `PromptCorpusNode` encapsule a single node in the *prompt corpus tree*.


    :param name: section heading of the node
    :type name: str
    :param parent: parent node in the tree structure;
            `None` if the root node
    :type parent: PromptCorpusNode
    :param text_lines: content to be parsed, each ``str`` represents a line
    :type text_lines: list(str)
    :example:
    >>> tree = PromptCorpusNode.parse(prompt_corpus_text)
    """

    @classmethod
    def parse(cls, prompt_corpus_text):
        """
        Parse *prompt corpus* text into the tree structure.

        :param prompt_corpus_text: full source *prompt corpus* content
        :type prompt_corpus_text: str
        :return: **root node** of the parsed *prompt corpus* tree structure
        :rtype: PromptCorpusNode
        """

        text_lines = cls._convert_corpus_text2lines(prompt_corpus_text)
        root = cls(ROOT_NODE_NAME, None, text_lines)
        return root

    def __init__(self, name, parent, text_lines):
        super().__init__(name, parent)
        self.content = []  # content lines

        self._init_populate_children(text_lines)

        # trim leading/trailing empty strings
        start, end = 0, len(self.content)
        while start < end and self.content[start] == "":
            start += 1
        while end > start and self.content[end - 1] == "":
            end -= 1
        self.content = self.content[start:end]

        self.path_of_names = self._init_generate_path_of_names()

    def generate_preview_tree(
        self, preview_line_count=3, preview_line_width=64
    ):
        """
        :param preview_line_count: set maximum line count of
                *content preview* part, (excluding section heading line);
                defaults to 3
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part;
                defaults to 64.
        :type preview_line_width: int
        :return: human-readable representation of ``self`` node and children,
                showing the tree structure, node name (i.e. section headings,)
                node content preview, etc.
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
        opt_lines = []

        for pre, fill, node in RenderTree(self):
            # line for the node
            opt_lines.append(pre + node.name)
            # lines for the content of node
            opt_lines.extend(
                node.generate_preview_tree_content_part(
                    fill, preview_line_count, preview_line_width
                )
            )

        return "\n".join(opt_lines)

    def generate_preview_tree_content_part(
        self, fill, preview_line_count, preview_line_width
    ):
        """
        :param fill: set prefix filling before each line
        :type fill: str
        :param preview_line_count: set maximum line count of
                *content preview* part, (excluding section heading line)
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part
        :type preview_line_width: int
        :return: content lines of ``self`` as it will be shown in
                tree ``__repr__()``, with formatting included
                Each entry represent a line in the ``__repr__()``
        :rtype: list[str]
        :example:
        >>> node.generate_preview_tree_content_part('$$$' 3, 10)
        ["$$$You per", "$$$When tr", "$$$User ma"]
        """
        lines = []
        if self.content and preview_line_count:  # print content of node
            for content_line in self.content[:preview_line_count]:
                lines.append(fill + content_line[:preview_line_width])
        return lines

    @staticmethod
    def _convert_corpus_text2lines(full_prompt):
        # reduce formatting empty lines
        cleanup = re.sub(r"\n{3,}", "\n\n", full_prompt)
        return list(cleanup.split("\n"))

    def _init_populate_children(self, text_lines):
        """
        helper method used in ``__init__()``

        create children nodes of ``self`` and populate self.content
        by parsing ``text_lines``
        """
        # find every sub-section heading lines
        heading_prefix = HEADING_PREFIX * (self.depth + 1) + " "
        heading_lines = []
        for idx, line in enumerate(text_lines):
            if line.startswith(heading_prefix):
                heading_lines.append(idx)

        # contain no subsection
        if not heading_lines:
            # all lines are content
            self.content = list(text_lines)
            return

        # this node contains subsections, then parse the content part out
        self.content = text_lines[: heading_lines[0]]
        if not any(self.content):
            self.content = []

        # parse sub-sections as nodes
        heading_lines.append(len(text_lines))
        for start, end in zip(heading_lines, heading_lines[1:]):
            # extract heading content
            # e.g. "### this is heading " -> "this is heading"
            heading_content = text_lines[start][len(heading_prefix) :].strip()
            children_nodes = text_lines[start + 1 : end]
            PromptCorpusNode(heading_content, self, children_nodes)

    def _init_generate_path_of_names(self):
        """
        helper method used in ``__init__()``

        generate content of ``.path_of_names``
        """
        if self.parent is None:
            return tuple()  # root node
        else:
            nodes_path = self.path[1:]  # remove root node
            return tuple(node.name for node in nodes_path)

    def __getitem__(self, key=None):
        """
        TODO
        :param key: heading of children node; if ``None``, get node parent
        :type key: str or NoneType
        :return: children or parent node of ``self``
        :rtype: PromptCorpusNode
        :raises IndexError:
        :raises KeyError:
        :raises TypeError:
        :example:
        node = ~
        node['Info']    # get child node with heading 'Info'
        node[]          # get parent node
        """
        if key is None:
            return self.parent

        elif isinstance(key, int):
            try:
                return self.children[key]
            except IndexError as err:
                raise IndexError(
                    "index out of range for PromptCorpusNode children: {}"
                    .format(key)
                ) from err

        elif isinstance(key, str):
            for child in self.children:
                if child.name == key:
                    return child
            raise KeyError(
                "fail to find child {} in this PromptCorpusNode".format(
                    repr(key)
                )
            )

        else:
            raise TypeError(
                "unsupported type for PromptCorpusNode[~]: {}".format(
                    type(key)
                )
            )

    def __repr__(self):
        """
        :return:
        :rtype: str
        :example:
        node=~~~
        assert str(node) == "PromptCorpusNode(Introduction#Data#Advanced)"
        """
        return "PromptCorpusNode({})".format("#".join(self.path_of_names))

    def __str__(self):
        return self.generate_preview_tree()

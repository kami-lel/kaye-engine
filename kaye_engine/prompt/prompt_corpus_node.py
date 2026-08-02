"""
prompt_corpus_node.py

define ``PromptCorpusNode``
"""

from .base_prompt_node import BasePromptNode

# section heading prefix used for parsing .md file of prompt corpus
HEADING_PREFIX_ELEMENT = "#"

__all__ = ("PromptCorpusNode",)


# auxiliaries  #################################################################


def _split_sections(text_lines, parent):
    # find every sub-section heading lines one level below parent
    prefix_element_cnt = 1 if parent is None else parent.depth + 2
    heading_prefix = HEADING_PREFIX_ELEMENT * prefix_element_cnt + " "

    heading_lines_idx = [
        idx
        for idx, line in enumerate(text_lines)
        if line.startswith(heading_prefix)
    ]

    if not heading_lines_idx:
        # contains no subsection, i.e. all of text_lines are node content
        return _trim_blank_lines(text_lines), []

    # contains subsections  ------------------------------------------------
    content_lines = _trim_blank_lines(text_lines[: heading_lines_idx[0]])

    child_specs = []
    for start, end in zip(
        heading_lines_idx, heading_lines_idx[1:] + [len(text_lines)]
    ):
        # extract heading content
        # e.g. "### this is heading " -> "this is heading"
        child_heading = text_lines[start][len(heading_prefix) :].strip()
        child_text_lines = text_lines[start + 1 : end]
        child_specs.append((child_heading, child_text_lines))

    return content_lines, child_specs


def _trim_blank_lines(lines):
    # trim leading/trailing empty strings
    start, end = 0, len(lines)
    while start < end and lines[start] == "":
        start += 1
    while end > start and lines[end - 1] == "":
        end -= 1
    return lines[start:end]


class PromptCorpusNode(BasePromptNode):  #######################################
    """
    A `PromptCorpusNode` encapsule a single node in the *prompt corpus tree*.


    :param heading: section heading, i.e. node name
    :type heading: str
    :param parent: parent node in the tree structure;
            `None` if the root node
    :type parent: PromptCorpusNode
    :param content_lines: section content, each ``str`` represents a line
    :type content_lines: list(str)
    :example:
    >>> tree = PromptCorpusNode.parse(prompt_corpus_text)
    """

    # constructor  =============================================================
    def __init__(self, heading, parent, content_lines):
        super().__init__(heading, parent)

        self._content_lines = content_lines

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        return self._content_lines

    def __copy__(self):
        copied = type(self)(self.name, None, [])
        copied._content_lines = self._content_lines
        return copied

    # parsing  ==================================================================

    @classmethod
    def parse(cls, name, parent, text_lines):
        """
        recursively build a subtree from raw markdown ``text_lines``,
        splitting on heading lines one level deeper than ``parent``


        :param name: heading of the node being built
        :type name: str
        :param parent: parent node; `None` if building the root node
        :type parent: PromptCorpusNode
        :param text_lines: raw markdown lines to parse into this subtree
        :type text_lines: list(str)
        :return: the built node, already attached to ``parent``
        :rtype: PromptCorpusNode
        """
        content_lines, child_specs = _split_sections(text_lines, parent)

        node = cls(name, parent, content_lines)

        for child_heading, child_text_lines in child_specs:
            cls.parse(child_heading, node, child_text_lines)

        return node

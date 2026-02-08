"""
define ``load_prompt_corpus_tree``
and its supporting function ``get_embedded_prompt_corpus_file_path()``
"""

import re
from pathlib import Path


from .prompt_corpus_node import PromptCorpusNode
from .today_node import TodayNode
from .abbr_nodes import AbbrNode, PLCNode

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "load_prompt_corpus_tree",
)


def get_embedded_prompt_corpus_file_path():
    """
    :return: absolute path of embedded prompt corpus ``prompt_corpus.md`` file
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_corpus.md"
    ).absolute()


def load_prompt_corpus_tree(disable_dynamic_nodes=False):
    """
    TODO


    :param disable_dynamic_nodes: do not attach dynamics nodes to the tree;
            defaults to False
    :type disable_dynamic_nodes: bool, optional
    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    # read corpus from file  ---------------------------------------------------
    prompt_corpus_file_path = get_embedded_prompt_corpus_file_path()
    with open(
        prompt_corpus_file_path, "r", encoding="utf-8", newline=""
    ) as file:
        prompt_corpus_text = file.read()

    # text split & clean up  ---------------------------------------------------
    # reduce 2+ empty lines into single empty line
    text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
    # split to lines
    text_lines = list(text_cleanup.split("\n"))

    root = PromptCorpusNode(ROOT_NODE_NAME, None, [])

    # create prompt corpus nodes  ----------------------------------------------
    _populate_children_from_text_lines_recursively(root, text_lines)

    # attach dynamic nodes  ----------------------------------------------------
    if not disable_dynamic_nodes:
        TodayNode(root)
        AbbrNode(root)
        PLCNode(root)

    return root


# helpers  #####################################################################
ROOT_NODE_NAME = "○"
HEADING_PREFIX = "#"


def _populate_children_from_text_lines_recursively(parent, text_lines):
    # BUG BUG

    # find every sub-section heading lines
    heading_prefix = HEADING_PREFIX * (self.depth + 1) + " "
    heading_lines = []
    for idx, line in enumerate(text_lines):
        if line.startswith(heading_prefix):
            heading_lines.append(idx)

    # contain no subsection
    if not heading_lines:
        # all lines are content
        self._content_lines = list(text_lines)
        return

    # this node contains subsections, then parse the content part out
    self._content_lines = text_lines[: heading_lines[0]]
    if not any(self._content_lines):
        self._content_lines = []

    # parse sub-sections as nodes
    heading_lines.append(len(text_lines))
    for start, end in zip(heading_lines, heading_lines[1:]):
        # extract heading content
        # e.g. "### this is heading " -> "this is heading"
        heading_content = text_lines[start][len(heading_prefix) :].strip()
        children_nodes = text_lines[start + 1 : end]
        PromptCorpusNode(heading_content, self, children_nodes)

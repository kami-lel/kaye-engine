"""
define ``load_prompt_corpus_tree``
and its supporting function ``get_embedded_prompt_corpus_file_path()``
"""

from pathlib import Path
from .prompt_corpus_node import PromptCorpusNode

from .. import kamilog, PROGRAM_NAME

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "load_prompt_corpus_tree",
    "load_embedded_prompt_corpus",  # HACK HACK rm
)

logger = kamilog.getLogger(PROGRAM_NAME)


def get_embedded_prompt_corpus_file_path():
    """
    :return: absolute path of embedded prompt corpus ``prompt_corpus.md`` file
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_corpus.md"
    ).absolute()


def load_prompt_corpus_tree():  # TODO TODO
    pass


def load_embedded_prompt_corpus():  # HACK HACK rm
    """
    Load a prompt corpus tree of the **embedded** prompt corpus text.


    :return: **root** node of the parsed *prompt corpus* tree
    :rtype: PromptCorpusNode
    :raises FileNotFoundError:
    :raises IOError:
    """

    full_prompt_file_path = get_embedded_prompt_corpus_file_path()
    with open(full_prompt_file_path, "r", encoding="utf-8", newline="") as file:
        file_content = file.read()
        logger.debug(
            "embedded prompt corpus loaded from: %s", full_prompt_file_path
        )
        return PromptCorpusNode.parse(file_content)


def _create_dynamic_node(heading, parent):  # HACK HACK
    if heading == TodayNode.HEADING:
        return TodayNode(parent)


# public API  ==============================================================


ROOT_NODE_NAME = "○"  # placeholder name for root node


@classmethod
def parse(cls, prompt_corpus_text):  # TODO TODO parse also dynamic nodes
    """
    parse *prompt corpus* text into the tree structure.


    :param prompt_corpus_text: full source *prompt corpus* content
    :type prompt_corpus_text: str
    :return: **root node** of the parsed *prompt* tree structure
    :rtype: PromptCorpusNode
    """
    # reduce 2+ empty lines into single empty line
    text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
    # split to lines
    text_lines = list(text_cleanup.split("\n"))

    root = cls(ROOT_NODE_NAME, None, text_lines)
    return root


def _init_populate_children(self, text_lines):
    """
    create node children and add content to ``._content_line``

    (helper method used in ``__init__()``)
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

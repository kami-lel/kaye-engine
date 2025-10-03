"""
define ``load_embedded_prompt_corpus``
"""

from pathlib import Path
from .prompt_corpus_node import PromptCorpusNode

from .. import kamilog, PROGRAM_NAME

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "load_embedded_prompt_corpus",
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


def load_embedded_prompt_corpus():
    """
    Load the prompt corpus embedded with this Python package,
    then parse the text to the tree structure.

    :return: **root node** of the parsed *prompt corpus* tree structure
    :rtype: PromptCorpusNode
    :raises FileNotFoundError:
    :raises IOError:
    """

    full_prompt_file_path = get_embedded_prompt_corpus_file_path()
    with open(
        full_prompt_file_path, "r", encoding="utf-8", newline=""
    ) as file:
        file_content = file.read()
        logger.debug(
            "embedded prompt corpus loaded from: %s", full_prompt_file_path
        )
        return PromptCorpusNode.parse(file_content)

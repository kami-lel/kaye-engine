"""
Kaye Programmatic API: Prompt Generation

The **core** module of *Kaye Python API*,
implement a systematic, dynamic, and structured framework
for **prompt management and manipulation**.
"""

from .base_prompt_node import *
from .prompt_corpus_node import *
from .prompt_corpus_loader import *
from .prompt_blueprint import *
from .prompt_blueprint_loader import *
from .abbr_nodes import *
from .today_node import *
from .embedded_blueprints import *


def collapse_lines_into_single_line(lines):
    """
    collapse an iterable of text lines into one single-line string


    :param lines: the text lines to collapse onto a single line
    :type lines: Iterable[str]
    :return: the lines joined into one string by the line-break glyph
    :rtype: str
    """
    return "↵".join(lines)

"""
render.comment.py

define:

- ``comment_line_registry``
- ``register_comment_line``
- ``render_comment_lines``
"""

import importlib.metadata
from datetime import datetime

from kaye_engine import PACKAGE_NAME

from .util import REPLACEMENT_NEWLINE_SYMBOL

__all__ = (
    "comment_line_registry",
    "register_comment_line",
    "render_comment_lines",
)


# registered client lines, in first-seen order
comment_line_registry = []


def register_comment_line(line):
    """
    register a line appended to every generated prompt comment

    a line already registered is ignored, keeping the first-seen order


    :param line: one comment line, e.g. a client project's version
    :type line: str
    :raises TypeError: if ``line`` is not a ``str``
    :raises ValueError: if ``line`` contains a newline or ``-->``
    """
    if not isinstance(line, str):
        raise TypeError(
            "comment line must be str, got {}".format(type(line).__name__)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("comment line must not contain a newline")
    if "-->" in line:
        raise ValueError("comment line must not contain '-->'")

    if line not in comment_line_registry:
        comment_line_registry.append(line)


def get_default_comment_lines(display_name=""):
    """
    (helper function used in ``render_comment_lines()``)


    :param display_name: blueprint's human-readable name, omitted when
            empty; defaults to ""
    :type display_name: str, optional
    :return: blueprint name line (if any), then Kaye Engine version line
    :rtype: list[str]
    """
    kaye_version = importlib.metadata.version(PACKAGE_NAME)

    # append render date-time in version for alpha releases
    if "a" in kaye_version:
        kaye_version += datetime.now().strftime(".0%Y%m%d%H%M%S")

    lines = []
    if display_name:
        lines.append("blueprint: {}".format(display_name))
    lines.append("Kaye Engine v{}".format(kaye_version))
    return lines


def render_comment_lines(display_name="", *, is_compact=False):
    """
    render the generated-by comment: default lines, then registered lines

    :param display_name: blueprint's human-readable name, omitted from the
            comment when empty; defaults to ""
    :type display_name: str, optional
    :param is_compact: whether to join all lines into one comment line
            with ``REPLACEMENT_NEWLINE_SYMBOL``; defaults to False
    :type is_compact: bool, optional
    :return: comment lines, delimiters included
    :rtype: list[str]

    :example:
    >>> render_comment_lines("Chat")
    ['<!--', 'blueprint: Chat', 'Kaye Engine v1.2.3', '-->']
    >>> render_comment_lines("Chat", is_compact=True)
    ['<!-- blueprint: Chat↵Kaye Engine v1.2.3 -->']
    """
    body = get_default_comment_lines(display_name) + comment_line_registry

    if is_compact:
        return ["<!-- " + REPLACEMENT_NEWLINE_SYMBOL.join(body) + " -->"]
    return ["<!--", *body, "-->"]

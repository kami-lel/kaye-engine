"""
render.comment.py

define:

- ``comment_line_registry``
- ``register_comment_line``
"""

__all__ = (
    "comment_line_registry",
    "register_comment_line",
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

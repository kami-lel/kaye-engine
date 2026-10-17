"""
md_comment.py

define ``strip_comment_blocks``
"""

__all__ = ("strip_comment_blocks",)

_OPEN = "<!--"
_CLOSE = "-->"


def strip_comment_blocks(lines):
    """
    drop every line-anchored markdown comment from ``lines``

    a comment opens on a line whose stripped content starts with
    ``<!--`` and closes on the first line, the opening one included,
    whose stripped content ends with ``-->``; every line from open to
    close is dropped. A comment sharing its line with prose, e.g. inside
    inline code, is not line-anchored and stays


    :param lines:
    :type lines: list[str]
    :return: ``lines`` without comment blocks
    :rtype: list[str]
    """
    result = []
    for line in lines:
        stripped = line.strip()
        if (
            stripped.startswith(_OPEN)
            and stripped.endswith(_CLOSE)
            and len(stripped) >= len(_OPEN) + len(_CLOSE)
        ):
            continue
        result.append(line)
    return result

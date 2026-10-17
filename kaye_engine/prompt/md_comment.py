"""
md_comment.py

define ``strip_comment_blocks``
"""

__all__ = ("strip_comment_blocks",)

_OPEN = "<!--"
_CLOSE = "-->"


def _find_comment_close(lines, start):
    """
    :return: position of the first line at or after ``start`` whose
        stripped content ends with ``-->``, or ``None`` if there is none
    :rtype: int | None
    """
    for idx in range(start, len(lines)):
        if lines[idx].strip().endswith(_CLOSE):
            return idx
    return None


def strip_comment_blocks(lines):
    """
    drop every line-anchored markdown comment from ``lines``

    a comment opens on a line whose stripped content starts with
    ``<!--`` and closes on the first line, the opening one included,
    whose stripped content ends with ``-->``; every line from open to
    close is dropped. An opening line with no closing line drops
    nothing. A comment sharing its line with prose, e.g. inside inline
    code, is not line-anchored and stays


    :param lines:
    :type lines: list[str]
    :return: ``lines`` without comment blocks
    :rtype: list[str]
    """
    result = []
    idx = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        end = None
        if stripped.startswith(_OPEN):
            # a one-line comment needs room for both delimiters
            first = stripped if len(stripped) >= 7 else _OPEN
            if first.endswith(_CLOSE):
                end = idx
            else:
                end = _find_comment_close(lines, idx + 1)
        if end is None:
            result.append(lines[idx])
            idx += 1
        else:
            idx = end + 1
    return result

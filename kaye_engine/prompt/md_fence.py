"""
md_fence.py

define ``compute_fenced_line_mask``
"""

import re

__all__ = ("compute_fenced_line_mask",)

_FENCE_PATTERN = re.compile(r"^(`{3,}|~{3,})")
_TAG_OPEN_PATTERN = re.compile(r"^<([A-Za-z][\w-]*)(\s[^>]*)?>$")


def _find_tag_close(lines, fenced_mask, start, name):
    """
    :return: position of the nearest non-fenced line after ``start``
        holding only ``</name>``, or ``None`` if there is none
    :rtype: int | None
    """
    closing = f"</{name}>"
    for idx in range(start + 1, len(lines)):
        if not fenced_mask[idx] and lines[idx].strip() == closing:
            return idx
    return None


def compute_fenced_line_mask(lines):
    """
    determine, for each line, if it belongs to a fenced code block or a
    markdown tag block

    a fence opens on a line whose stripped content starts with 3+
    backticks or 3+ tildes (optionally followed by a language tag, e.g.
    ` ```cpp `), and closes on the next line starting with the same fence
    character. Both delimiter lines are marked as inside the block

    a tag block opens on a non-fenced line holding only ``<name>`` (or
    ``<name attrs>``), and closes on the nearest following non-fenced line
    holding only ``</name>``; both delimiter lines are marked. An opening
    line with no closing line marks nothing


    :param lines:
    :type lines: list[str]
    :return: per-line mask, True if that line is part of a fenced code
        block or a tag block (delimiter lines included)
    :rtype: list[bool]
    """
    mask = [False] * len(lines)
    fence_char = None

    for idx, line in enumerate(lines):
        match = _FENCE_PATTERN.match(line.strip())

        if fence_char is None:
            if match:
                fence_char = match.group(1)[0]
                mask[idx] = True
            continue

        mask[idx] = True

        if match and match.group(1)[0] == fence_char:
            fence_char = None

    idx = 0
    while idx < len(lines):
        match = None
        if not mask[idx]:
            match = _TAG_OPEN_PATTERN.match(lines[idx].strip())
        end = None
        if match:
            end = _find_tag_close(lines, mask, idx, match.group(1))
        if end is None:
            idx += 1
            continue
        for k in range(idx, end + 1):
            mask[k] = True
        idx = end + 1

    return mask

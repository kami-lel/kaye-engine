"""
md_fence.py

define ``compute_fenced_line_mask``
"""

import re

__all__ = ("compute_fenced_line_mask",)

_FENCE_PATTERN = re.compile(r"^(`{3,}|~{3,})")


def compute_fenced_line_mask(lines):
    """
    determine, for each line, if it belongs to a fenced code block

    a fence opens on a line whose stripped content starts with 3+
    backticks or 3+ tildes (optionally followed by a language tag, e.g.
    ` ```cpp `), and closes on the next line starting with the same fence
    character. Both delimiter lines are marked as inside the block


    :param lines:
    :type lines: list[str]
    :return: per-line mask, True if that line is part of a fenced code
        block (delimiter lines included)
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

    return mask

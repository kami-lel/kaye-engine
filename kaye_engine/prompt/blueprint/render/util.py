"""
render.util.py

define:

- ``REPLACEMENT_NEWLINE_SYMBOL``
- ``NO_TRIM_SPARSENESS``
- ``apply_sparseness``
"""

from ...md_fence import compute_fenced_line_mask

__all__ = (
    "REPLACEMENT_NEWLINE_SYMBOL",
    "NO_TRIM_SPARSENESS",
    "apply_sparseness",
)


# constants  ####################################################################
REPLACEMENT_NEWLINE_SYMBOL = "↵"
NO_TRIM_SPARSENESS = 99


def apply_sparseness(lines, sparseness):
    """
    apply the ``sparseness`` blank-line policy to a list of prompt lines

    (helper function used in ``render_prompt_lines()``)


    :param lines:
    :type lines: list[str]
    :param sparseness: see ``render_prompt_lines()`` for the full contract
    :type sparseness: int
    :return: lines with the ``sparseness`` policy applied
    :rtype: list[str]
    """
    if sparseness == NO_TRIM_SPARSENESS:
        return lines

    fenced_mask = compute_fenced_line_mask(lines)

    # trim leading/trailing empty lines that are not part of a code block
    start, end = 0, len(lines)
    while start < end and lines[start] == "" and not fenced_mask[start]:
        start += 1
    while end > start and lines[end - 1] == "" and not fenced_mask[end - 1]:
        end -= 1
    trimmed = lines[start:end]
    trimmed_fenced_mask = fenced_mask[start:end]

    if sparseness == -1:
        return [REPLACEMENT_NEWLINE_SYMBOL.join(trimmed)]

    result = []
    empty_run = 0
    for line, is_fenced in zip(trimmed, trimmed_fenced_mask):
        if line == "" and not is_fenced:
            empty_run += 1
            continue
        result.extend([""] * min(empty_run, sparseness))
        empty_run = 0
        result.append(line)
    result.extend([""] * min(empty_run, sparseness))

    return result


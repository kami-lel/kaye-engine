"""
kaye_engine.prompt.blueprint.render.__init__.py

facade re-exporting the render subpackage's public API:

- ``render_blueprint_tree``
- ``render_prompt_lines``
- ``render_negative_prompt_lines``
- ``render_comment``
- ``apply_sparseness``
- ``REPLACEMENT_NEWLINE_SYMBOL``
- ``NO_TRIM_SPARSENESS``

(split across ``tree.py``, ``lines.py``, ``sidecar_splice.py``, and
``util.py``, so each concern stays a manageable module while every
existing ``render.X`` call site keeps working unchanged)
"""

from .lines import render_negative_prompt_lines, render_prompt_lines
from .tree import render_blueprint_tree
from .util import (
    NO_TRIM_SPARSENESS,
    REPLACEMENT_NEWLINE_SYMBOL,
    apply_sparseness,
    render_comment,
)

__all__ = (
    "REPLACEMENT_NEWLINE_SYMBOL",
    "apply_sparseness",
    "render_blueprint_tree",
    "render_comment",
    "render_negative_prompt_lines",
    "render_prompt_lines",
)

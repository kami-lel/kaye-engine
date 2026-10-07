"""
kaye_engine.prompt.blueprint.render.__init__.py

facade re-exporting the render subpackage's public API:

- ``preview_selection``
- ``render_prompt_lines``
- ``render_negative_prompt_lines``
- ``render_comment_lines``
- ``register_comment_line``
- ``apply_sparseness``
- ``REPLACEMENT_NEWLINE_SYMBOL``
- ``NO_TRIM_SPARSENESS``

(split across ``tree.py``, ``lines.py``, ``sidecar_splice.py``, and
``util.py``, so each concern stays a manageable module while every
existing ``render.X`` call site keeps working unchanged)
"""

from .comment import register_comment_line, render_comment_lines
from .lines import render_negative_prompt_lines, render_prompt_lines
from .meta import (
    show_dependencies,
    show_globs,
    show_description,
    show_description_and_when_to_use,
    show_display_name,
    show_when_to_use,
)
from .prompt import (
    preview_blueprint,
    preview_blueprint_without_dependencies,
    render_prompt,
    render_prompt_without_dependencies,
)
from .tree import preview_selection
from .util import (
    NO_TRIM_SPARSENESS,
    REPLACEMENT_NEWLINE_SYMBOL,
    apply_sparseness,
)

__all__ = (
    "show_dependencies",
    "REPLACEMENT_NEWLINE_SYMBOL",
    "apply_sparseness",
    "show_globs",
    "preview_blueprint",
    "preview_selection",
    "preview_blueprint_without_dependencies",
    "show_description",
    "show_description_and_when_to_use",
    "show_display_name",
    "show_when_to_use",
    "register_comment_line",
    "render_comment_lines",
    "render_negative_prompt_lines",
    "render_prompt",
    "render_prompt_lines",
    "render_prompt_without_dependencies",
)

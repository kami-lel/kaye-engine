"""
render.prompt.py

define the render pipeline over a ``Blueprint``:

- ``render_prompt``, ``render_prompt_without_dependencies``
- ``preview_blueprint``, ``preview_blueprint_without_dependencies``
"""

import dataclasses

from ..dynamic_substitution import apply_dynamic_substitutions
from ..render_mode import RenderMode
from ..render_profile import RenderProfile
from ..selection import bind_selection, resolve_selection
from .lines import render_negative_prompt_lines, render_prompt_lines
from .tree import preview_selection
from .util import NO_TRIM_SPARSENESS, apply_sparseness

__all__ = (
    "preview_blueprint",
    "preview_blueprint_without_dependencies",
    "render_prompt",
    "render_prompt_without_dependencies",
)


# auxiliaries  #################################################################
def _render_selection_prompt(selection, *, profile=None, **kwargs):
    """
    render the **concrete prompt** that can be used as LLM system message
    from ``selection``, then resolve every inline ``(((name)))``
    placeholder against the same render options

    ``profile.mode`` picks the rendering behavior:
    ``RenderMode.NEGATIVE`` renders the negative prompt in place of
    the positive one, ``RenderMode.POST_ORDER`` reorders every
    subtree to children-before-parent (siblings keep their original
    relative order), and ``RenderMode.IMAGE`` (which also implies
    ``POST_ORDER``) forces ``sparseness=1`` regardless of what
    ``profile.sparseness`` was set to. Combined as
    ``RenderMode.NEGATIVE | RenderMode.IMAGE``, the negative prompt
    prints no title at all, only the ``{avoid}`` content

    the order is: render lines at no-trim sparseness, substitute, then
    apply the real sparseness

    (helper function used in ``render_prompt()`` and
    ``render_prompt_without_dependencies()``)


    :param selection:
    :type selection: BlueprintSelection
    :param profile: bundled render settings; defaults to a plain
            `RenderProfile()`
    :type profile: RenderProfile, optional
    :param kwargs: further render options (e.g. ``query``)
    :return: generated prompt
    :rtype: str
    """
    profile = profile or RenderProfile()
    if RenderMode._IMAGE in profile.mode:
        profile = dataclasses.replace(profile, sparseness=1)
    merged_kwargs = {**profile.as_kwargs(), **kwargs}

    render_lines = (
        render_negative_prompt_lines
        if RenderMode.NEGATIVE in profile.mode
        else render_prompt_lines
    )

    unsparse_profile = dataclasses.replace(
        profile, sparseness=NO_TRIM_SPARSENESS
    )
    text = "\n".join(
        render_lines(
            selection,
            profile=unsparse_profile,
            # render at NO_TRIM_SPARSENESS hides the real sparseness
            is_comment_compact=(profile.sparseness == -1),
            **kwargs,
        )
    )
    substituted = apply_dynamic_substitutions(text, **merged_kwargs)
    return "\n".join(
        apply_sparseness(substituted.split("\n"), profile.sparseness)
    )


# Public API  ##################################################################
def render_prompt_without_dependencies(blueprint, *, profile=None, **kwargs):
    """
    render the prompt from ``blueprint``'s own nodes only, ignoring
    ``dependencies``

    (see ``render_prompt()`` for parameters)


    :raises ValueError: a path of ``blueprint`` is not in the loaded corpus
    :return: generated prompt
    :rtype: str
    """
    return _render_selection_prompt(
        bind_selection(blueprint), profile=profile, **kwargs
    )


def render_prompt(blueprint, *, profile=None, **kwargs):
    """
    render the **concrete prompt** that can be used as LLM system message
    from ``blueprint``'s nodes merged with the full transitive closure of
    its ``dependencies``


    :param blueprint:
    :type blueprint: Blueprint
    :param profile: bundled render settings; defaults to a plain
            `RenderProfile()`
    :type profile: RenderProfile, optional
    :param kwargs: further render options (e.g. ``query``)
    :raise ValueError: a dependency cycle or an unknown dependency name, or
            a path of a blueprint that is not in the loaded corpus
    :return: generated prompt
    :rtype: str
    """
    return _render_selection_prompt(
        resolve_selection(blueprint), profile=profile, **kwargs
    )


def preview_blueprint_without_dependencies(blueprint, **kwargs):
    """
    generate **preview tree** of ``blueprint``'s own nodes only

    (see ``preview_selection()`` for parameters)


    :raises ValueError: a path of ``blueprint`` is not in the loaded corpus
    :return: the preview tree
    :rtype: str
    """
    return preview_selection(bind_selection(blueprint), **kwargs)


def preview_blueprint(blueprint, **kwargs):
    """
    generate **preview tree** of ``blueprint``'s nodes merged with the
    full transitive closure of its ``dependencies``

    (see ``preview_selection()`` for parameters)


    :raise ValueError: a dependency cycle or an unknown dependency name
    :return: the preview tree
    :rtype: str
    """
    return preview_selection(resolve_selection(blueprint), **kwargs)

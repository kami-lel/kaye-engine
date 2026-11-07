"""
builtin_render_profiles.py

define ``register_builtin_render_profiles`` -- registers the 5 render
profiles the engine ships, each with its remark, and runs once when
``kaye_engine.prompt`` is imported
"""

from .blueprint.render_profile import RenderProfile
from .blueprint.render_profile_registry import (
    register_render_profile,
    render_profile_registry,
)
from .builtin_affordances import (
    BUILTIN_AFFORDANCES,
    register_builtin_affordances,
)

__all__ = ("register_builtin_render_profiles",)


# constants  ###################################################################

# on every Claude surface by default: `git`, and the target diffusion
# model, which is not a Claude tool
_COMMON_AFFORDANCES = ("git", "QwenImage")

# the one Claude variant no Chat or Code surface carries (VSC only)
_VSC_ONLY_AFFORDANCES = ("Claude:getDiagnostics",)

# every other Claude variant: Chat and Code tools, iOS calendar included
_CLAUDE_AFFORDANCES = (
    tuple(
        name
        for _, variants in BUILTIN_AFFORDANCES.values()
        for name in variants
        if name.startswith("Claude:") and name not in _VSC_ONLY_AFFORDANCES
    )
    + _COMMON_AFFORDANCES
)

# the tools Claude Code in Visual Studio Code carries
_VSC_AFFORDANCES = (
    "Claude:Read/Write/Edit~",
    "Claude:NotebookEdit",
    "Claude:Bash",
    "Claude:Agent~",
    "Claude:Task~",
    "Claude:TodoWrite",
    "Claude:Enter/ExitPlanMode",
    "Claude:Enter/ExitWorktree",
    "Claude:CronCreate/Delete/List",
    "Claude:Monitor",
    "Claude:RemoteTrigger",
    "Claude:ScheduleWakeup",
    "Claude:AskUserQuestion",
    "Claude:Inbox~",
    "Claude:PushNotification",
    "Claude:ReportFindings",
    "Claude:SendUserFile",
    "Claude:Web~",
    "Claude:McpResource~",
    "Claude:Skill",
    "Claude:ToolSearch",
    "Claude:Artifact",
    "Claude:DesignSync",
    "Claude:Docs~",
    "Claude:PDFViewer~",
    "Claude:Gmail",
    "Claude:TickTick",
    "Claude:getDiagnostics",
) + _COMMON_AFFORDANCES

# every Hermes tool variant, plus the image model
_HERMES_AFFORDANCES = (
    tuple(
        name
        for _, variants in BUILTIN_AFFORDANCES.values()
        for name in variants
        if name.startswith("Hermes:")
    )
    + ("QwenImage",)
)

_UNIVERSAL_SIDECAR = "Claude"

# platform-identity marker of the Hermes Agents surface
_HERMES_SIDECAR = "for Hermes"

# every surface renders {avoid} content inline, unconditionally
_AVOID_SIDECAR = "avoid"


# auxiliaries  #################################################################
def _claude_profile(affordances, identity_name):
    """
    :return: a ``RenderProfile`` whose ``variants`` carry only
            ``affordances`` and whose ``conditional_sidecars`` are those
            plus the surface's identity marker and the universal
            ``Claude`` marker, each bracket-wrapped, then ``avoid`` --
            identity names are never registered variants, so they never
            belong in ``variants``
    :rtype: RenderProfile
    """
    marked = dict.fromkeys(
        affordances
        + ((identity_name,) if identity_name else ())
        + (_UNIVERSAL_SIDECAR,)
    )
    return RenderProfile(
        variants=affordances,
        conditional_sidecars=tuple("[{}]".format(name) for name in marked)
        + (_AVOID_SIDECAR,),
    )


# Main Entry Point  ############################################################
def register_builtin_render_profiles():
    """
    register the built-in affordances and the 5 built-in render profiles
    into ``render_profile_registry``, skipping any name already
    registered, so a repeated call stays idempotent instead of raising
    """
    register_builtin_affordances()

    builtins = (
        (
            "claude",
            _claude_profile(_CLAUDE_AFFORDANCES, None),
            "Anthropic Claude apps: chat, Cowork, Code, iOS",
        ),
        (
            "claude-vsc",
            _claude_profile(_VSC_AFFORDANCES, "ClaudeVSC"),
            "Anthropic Claude Code extension for Microsoft Visual Studio"
            " Code",
        ),
        # no affordance variants (empty, not None, so affordance gating
        # stays on and Fallback content renders), no Claude identity
        (
            "continue",
            RenderProfile(variants=(), conditional_sidecars=(_AVOID_SIDECAR,)),
            "Continue.dev rules",
        ),
        # the Hermes tool variants plus the image model, no Claude
        # affordance variants (so Claude-only Fallbacks render), plus the
        # Hermes identity marker
        (
            "hermes",
            RenderProfile(
                variants=_HERMES_AFFORDANCES,
                conditional_sidecars=tuple(
                    "[{}]".format(name) for name in _HERMES_AFFORDANCES
                )
                + ("[{}]".format(_HERMES_SIDECAR), _AVOID_SIDECAR),
            ),
            "Hermes Agents",
        ),
        # the image model alone, so every Claude-tool affordance renders its
        # Fallback; no Claude identity
        (
            "comfy",
            RenderProfile(
                variants=("QwenImage",),
                conditional_sidecars=("[QwenImage]", _AVOID_SIDECAR),
            ),
            "Comfy Org ComfyUI image prompts",
        ),
    )

    for name, profile, remark in builtins:
        if name not in render_profile_registry:
            register_render_profile(name, profile, remark)


register_builtin_render_profiles()

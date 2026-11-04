"""
builtin_render_profiles.py

define ``register_builtin_render_profiles`` -- registers the 8 render
profiles the engine ships, each with its remark, and runs once when
``kaye_engine.prompt`` is imported
"""

from .blueprint.render_profile import RenderProfile
from .blueprint.render_profile_registry import (
    register_render_profile,
    render_profile_registry,
)
from .builtin_affordances import register_builtin_affordances

__all__ = ("register_builtin_render_profiles",)


# constants  ###################################################################

# on every Claude surface by default: `git`, and the target diffusion
# model, which is not a Claude tool
_COMMON_AFFORDANCES = ("git", "QwenImage")

_CHAT_AFFORDANCES = (
    "ClaudeChat:ask_user_input_v0",
    "ClaudeChat:places_map_display_v0",
    "ClaudeChat:places_list_display_v0",
    "ClaudeChat:recipe_display_v0",
    "ClaudeChat:itinerary_display_v0",
    "ClaudeChat:step_card_display_v0",
    "ClaudeChat:options_card_display_v0",
    "ClaudeChat:comparison_card_display_v0",
    "ClaudeChat:featured_card_display_v0",
    "ClaudeChat:product_carousel_display_v0",
    "ClaudeChat:link_preview_display_v0",
    "ClaudeChat:visualize:show_widget",
    "ClaudeChat:memory~",
    "ClaudeChat:weather_fetch",
    "ClaudeChat:places_search",
    "ClaudeChat:message_compose_v1",
    "ClaudeChat:view/str_replace/create_file~",
    "ClaudeChat:present_files",
    "ClaudeChat:bash_tool",
    "ClaudeChat:Gmail",
    "ClaudeChat:GoogleCalendar:EventEdit",
    "ClaudeChat:GoogleCalendar:EventInfo",
    "ClaudeChat:GoogleCalendar:Subcalendar",
    "ClaudeChat:web_~",
    "ClaudeChat:TickTick",
) + _COMMON_AFFORDANCES

_IOSCHAT_AFFORDANCES = _CHAT_AFFORDANCES + (
    "ClaudeiOSChat:Calendar:EventEdit",
    "ClaudeiOSChat:Calendar:EventInfo",
    "ClaudeiOSChat:Calendar:Subcalendar",
)

_COWORK_TIER_AFFORDANCES = (
    "ClaudeCode:AskUserQuestion",
    "ClaudeCode:Skill",
    "ClaudeCode:Read/Write/Edit~",
    "ClaudeCode:SendUserFile",
    "ClaudeCode:Bash",
    "ClaudeCode:Web~",
) + _COMMON_AFFORDANCES

_COWORK_AFFORDANCES = _COWORK_TIER_AFFORDANCES + (
    "ClaudeCowork:Gmail",
    "ClaudeCowork:TickTick",
    "ClaudeCowork:GoogleCalendar:EventEdit",
    "ClaudeCowork:GoogleCalendar:EventInfo",
    "ClaudeCowork:GoogleCalendar:Subcalendar",
)

_CODE_TIER_AFFORDANCES = (
    "ClaudeCode:Artifact",
    "ClaudeCode:PushNotification",
    "ClaudeCode:NotebookEdit",
    "ClaudeCode:RemoteTrigger",
    "ClaudeCode:DesignSync",
    "ClaudeCode:ReportFindings",
    "ClaudeCode:Enter/ExitPlanMode",
    "ClaudeCode:Enter/ExitWorktree",
    "ClaudeCode:ScheduleWakeup",
    "ClaudeCode:CronCreate/Delete/List",
    "ClaudeCode:Monitor",
    "ClaudeCode:Task~",
    "ClaudeCode:PowerShell",
)

_CODE_AFFORDANCES = _COWORK_TIER_AFFORDANCES + _CODE_TIER_AFFORDANCES

_VSC_EXCLUDED_AFFORDANCES = (
    "ClaudeCode:SendUserFile",
    "ClaudeCode:ReportFindings",
    "ClaudeCode:PowerShell",
)

_VSC_AFFORDANCES = tuple(
    name
    for name in _CODE_AFFORDANCES
    + (
        "ClaudeCode:Agent~",
        "ClaudeCode:TodoWrite",
    )
    if name not in _VSC_EXCLUDED_AFFORDANCES
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
    marked = dict.fromkeys(affordances + (identity_name, _UNIVERSAL_SIDECAR))
    return RenderProfile(
        variants=affordances,
        conditional_sidecars=tuple("[{}]".format(name) for name in marked)
        + (_AVOID_SIDECAR,),
    )


# Main Entry Point  ############################################################
def register_builtin_render_profiles():
    """
    register the built-in affordances and the 8 built-in render profiles
    into ``render_profile_registry``, skipping any name already
    registered, so a repeated call stays idempotent instead of raising
    """
    register_builtin_affordances()

    builtins = (
        (
            "chat",
            _claude_profile(_CHAT_AFFORDANCES, "ClaudeChat"),
            "Anthropic Claude chat app on web and desktop",
        ),
        (
            "cowork",
            _claude_profile(_COWORK_AFFORDANCES, "ClaudeCowork"),
            "Anthropic Claude Cowork desktop agent",
        ),
        (
            "code",
            _claude_profile(_CODE_AFFORDANCES, "ClaudeCode"),
            "Anthropic Claude Code in the terminal",
        ),
        (
            "vsc",
            _claude_profile(_VSC_AFFORDANCES, "ClaudeVSC"),
            "Anthropic Claude Code extension for Microsoft Visual Studio"
            " Code",
        ),
        (
            "ioschat",
            _claude_profile(_IOSCHAT_AFFORDANCES, "ClaudeiOSChat"),
            "Anthropic Claude chat app on Apple iOS",
        ),
        # no affordance variants (empty, not None, so affordance gating
        # stays on and Fallback content renders), no Claude identity
        (
            "continue",
            RenderProfile(variants=(), conditional_sidecars=(_AVOID_SIDECAR,)),
            "Continue.dev rules",
        ),
        # no affordance variants, but the Hermes identity marker is on
        (
            "hermes",
            RenderProfile(
                variants=(),
                conditional_sidecars=("[{}]".format(_HERMES_SIDECAR),)
                + (_AVOID_SIDECAR,),
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

"""
builtin_affordances.py

define ``AFFORDANCE_GROUPS`` and ``register_builtin_affordances`` -- the
affordance families the built-in render profiles refer to
"""

from .affordance_registry import (
    affordance_registry,
    register_affordance,
    register_variant,
    variant_registry,
)

__all__ = (
    "AFFORDANCE_GROUPS",
    "register_builtin_affordances",
)

# affordance name -> its variant canonical names; a `~` suffix on a
# variant marks that it bundles 2+ tools
AFFORDANCE_GROUPS = {
    "ask-user-question": (
        "ClaudeChat:ask_user_input_v0",
        "ClaudeCode:AskUserQuestion",
    ),
    "file-edit": (
        "ClaudeChat:view/str_replace/create_file~",
        "ClaudeCode:Read/Write/Edit~",
    ),
    "task-tracking": (
        "ClaudeCode:TodoWrite",
        "ClaudeCode:Task~",
    ),
    "file-delivery": (
        "ClaudeCode:SendUserFile",
        "ClaudeChat:present_files",
    ),
    "cli": (
        "ClaudeCode:Bash",
        "ClaudeCode:PowerShell",
        "ClaudeChat:bash_tool",
    ),
    "agent": ("ClaudeCode:Agent~",),
    "plan-mode": ("ClaudeCode:Enter/ExitPlanMode",),
    "worktree": ("ClaudeCode:Enter/ExitWorktree",),
    "cron": ("ClaudeCode:CronCreate/Delete/List",),
    "memory": ("ClaudeChat:memory~",),
    "places-map-display": ("ClaudeChat:places_map_display_v0",),
    "places-list-display": ("ClaudeChat:places_list_display_v0",),
    "recipe-display": ("ClaudeChat:recipe_display_v0",),
    "itinerary-display": ("ClaudeChat:itinerary_display_v0",),
    "step-card-display": ("ClaudeChat:step_card_display_v0",),
    "options-card-display": ("ClaudeChat:options_card_display_v0",),
    "comparison-card-display": ("ClaudeChat:comparison_card_display_v0",),
    "featured-card-display": ("ClaudeChat:featured_card_display_v0",),
    "product-carousel-display": ("ClaudeChat:product_carousel_display_v0",),
    "link-preview-display": ("ClaudeChat:link_preview_display_v0",),
    "visualize-show-widget": ("ClaudeChat:visualize:show_widget",),
    "artifact": ("ClaudeCode:Artifact",),
    "push-notification": ("ClaudeCode:PushNotification",),
    "weather-fetch": ("ClaudeChat:weather_fetch",),
    "places-search": ("ClaudeChat:places_search",),
    "message-compose": ("ClaudeChat:message_compose_v1",),
    "web": (
        "ClaudeChat:web_~",
        "ClaudeCode:Web~",
    ),
    "email-management": (
        "ClaudeChat:Gmail",
        "ClaudeCowork:Gmail",
    ),
    "getting-things-done": (
        "ClaudeChat:TickTick",
        "ClaudeCowork:TickTick",
    ),
    "calendar-event-edit": (
        "ClaudeChat:GoogleCalendar:EventEdit",
        "ClaudeCowork:GoogleCalendar:EventEdit",
        "ClaudeiOSChat:Calendar:EventEdit",
    ),
    "calendar-event-info": (
        "ClaudeChat:GoogleCalendar:EventInfo",
        "ClaudeCowork:GoogleCalendar:EventInfo",
        "ClaudeiOSChat:Calendar:EventInfo",
    ),
    "calendar-subcalendar": (
        "ClaudeChat:GoogleCalendar:Subcalendar",
        "ClaudeCowork:GoogleCalendar:Subcalendar",
        "ClaudeiOSChat:Calendar:Subcalendar",
    ),
    "notebook-edit": ("ClaudeCode:NotebookEdit",),
    "remote-trigger": ("ClaudeCode:RemoteTrigger",),
    "skill": ("ClaudeCode:Skill",),
    "design-sync": ("ClaudeCode:DesignSync",),
    "report-findings": ("ClaudeCode:ReportFindings",),
    "schedule-wakeup": ("ClaudeCode:ScheduleWakeup",),
    "monitor": ("ClaudeCode:Monitor",),
    "git": ("git",),
    # target diffusion model, not a Claude tool: on every Claude surface by
    # default, like `git`
    "image-model": ("QwenImage",),
}


# Main Entry Point  ############################################################
def register_builtin_affordances():
    """
    register every variant of ``AFFORDANCE_GROUPS`` into
    ``variant_registry``, skipping any already registered, so a repeated
    call stays idempotent instead of raising
    """
    for affordance_name, variant_names in AFFORDANCE_GROUPS.items():
        if affordance_name not in affordance_registry:
            register_affordance(affordance_name)
        for canonical_name in variant_names:
            if canonical_name in variant_registry:
                continue
            register_variant(canonical_name, affordance_name=affordance_name)

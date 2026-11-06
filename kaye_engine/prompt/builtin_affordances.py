"""
builtin_affordances.py

define ``BUILTIN_AFFORDANCES``, ``AFFORDANCE_GROUPS`` and
``register_builtin_affordances`` -- the affordance families the built-in
render profiles refer to, each with its remark
"""

from .affordance_registry import (
    affordance_registry,
    register_affordance,
    register_variant,
    variant_registry,
)

__all__ = (
    "AFFORDANCE_GROUPS",
    "BUILTIN_AFFORDANCES",
    "register_builtin_affordances",
)

# affordance name -> (its remark, {variant canonical name: its remark}); a
# `~` suffix on a variant marks that it bundles 2+ tools
BUILTIN_AFFORDANCES = {
    "ask-user-question": (
        "ask multiple-choice questions",
        {
            "ClaudeChat:ask_user_input_v0": "show tappable multiple-choice",
            "ClaudeCode:AskUserQuestion": "ask selectable-option question",
        },
    ),
    "file-edit": (
        "view and edit files",
        {
            "ClaudeChat:view/str_replace/create_file~": (
                "edit Chat sandbox files"
            ),
            "ClaudeCode:Read/Write/Edit~": "edit local files",
        },
    ),
    "task-tracking": (
        "track session tasks",
        {
            "ClaudeCode:TodoWrite": "keep session to-do list",
            "ClaudeCode:Task~": "manage background tasks",
        },
    ),
    "file-delivery": (
        "send files to user",
        {
            "ClaudeCode:SendUserFile": "send local file",
            "ClaudeChat:present_files": "present sandbox files",
        },
    ),
    "cli": (
        "run shell commands",
        {
            "ClaudeCode:Bash": "run shell command",
            "ClaudeCode:PowerShell": "run PowerShell command, Code only",
            "ClaudeChat:bash_tool": "run Chat sandbox shell command",
        },
    ),
    "agent": (
        "launch and message subagents",
        {
            "ClaudeCode:Agent~": "manage subagents and sessions",
        },
    ),
    "plan-mode": (
        "plan before editing",
        {
            "ClaudeCode:Enter/ExitPlanMode": "toggle planning mode",
        },
    ),
    "worktree": (
        "isolate work in a git worktree",
        {
            "ClaudeCode:Enter/ExitWorktree": "enter and exit worktree",
        },
    ),
    "cron": (
        "schedule cloud agents",
        {
            "ClaudeCode:CronCreate/Delete/List": "manage scheduled agents",
        },
    ),
    "memory": (
        "store persistent memory",
        {
            "ClaudeChat:memory~": "read and write memory files",
        },
    ),
    "places-map-display": (
        "show places on a map",
        {
            "ClaudeChat:places_map_display_v0": "show map of places",
        },
    ),
    "places-list-display": (
        "show places as a list",
        {
            "ClaudeChat:places_list_display_v0": "show list of places",
        },
    ),
    "recipe-display": (
        "show recipe card",
        {
            "ClaudeChat:recipe_display_v0": "show scalable recipe card",
        },
    ),
    "itinerary-display": (
        "show travel itinerary card",
        {
            "ClaudeChat:itinerary_display_v0": "show day-by-day itinerary",
        },
    ),
    "step-card-display": (
        "show step-by-step card",
        {
            "ClaudeChat:step_card_display_v0": "show numbered steps",
        },
    ),
    "options-card-display": (
        "show alternatives card",
        {
            "ClaudeChat:options_card_display_v0": "show multi-approach options",
        },
    ),
    "comparison-card-display": (
        "show product comparison card",
        {
            "ClaudeChat:comparison_card_display_v0": (
                "show side-by-side comparison"
            ),
        },
    ),
    "featured-card-display": (
        "show best-pick product card",
        {
            "ClaudeChat:featured_card_display_v0": "show single best pick",
        },
    ),
    "product-carousel-display": (
        "show product carousel",
        {
            "ClaudeChat:product_carousel_display_v0": "show paged products",
        },
    ),
    "link-preview-display": (
        "show link preview cards",
        {
            "ClaudeChat:link_preview_display_v0": "show external link previews",
        },
    ),
    "visualize-show-widget": (
        "render inline diagram or widget",
        {
            "ClaudeChat:visualize:show_widget": "render inline SVG or HTML",
        },
    ),
    "artifact": (
        "publish shareable web page",
        {
            "ClaudeCode:Artifact": "publish HTML page",
        },
    ),
    "push-notification": (
        "send push notification",
        {
            "ClaudeCode:PushNotification": "send push notification",
        },
    ),
    "weather-fetch": (
        "fetch weather by location",
        {
            "ClaudeChat:weather_fetch": "look up weather",
        },
    ),
    "places-search": (
        "search places",
        {
            "ClaudeChat:places_search": "search Google Places",
        },
    ),
    "message-compose": (
        "draft messages",
        {
            "ClaudeChat:message_compose_v1": "draft email, Slack, text",
        },
    ),
    "web": (
        "search and fetch web pages",
        {
            "ClaudeChat:web_~": "search and fetch in Chat",
            "ClaudeCode:Web~": "search and fetch in Code",
        },
    ),
    "email-management": (
        "read and send email",
        {
            "ClaudeChat:Gmail": "use Gmail in Chat",
            "ClaudeCowork:Gmail": "use Gmail in Cowork",
        },
    ),
    "getting-things-done": (
        "manage tasks",
        {
            "ClaudeChat:TickTick": "use TickTick in Chat",
            "ClaudeCowork:TickTick": "use TickTick in Cowork",
        },
    ),
    "calendar-event-edit": (
        "edit calendar events",
        {
            "ClaudeChat:GoogleCalendar:EventEdit": "edit Google Calendar, Chat",
            "ClaudeCowork:GoogleCalendar:EventEdit": (
                "edit Google Calendar, Cowork"
            ),
            "ClaudeiOSChat:Calendar:EventEdit": "edit calendar, iOS",
        },
    ),
    "calendar-event-info": (
        "look up calendar events",
        {
            "ClaudeChat:GoogleCalendar:EventInfo": (
                "look up Google Calendar, Chat"
            ),
            "ClaudeCowork:GoogleCalendar:EventInfo": (
                "look up Google Calendar, Cowork"
            ),
            "ClaudeiOSChat:Calendar:EventInfo": "look up calendar, iOS",
        },
    ),
    "calendar-subcalendar": (
        "list calendars",
        {
            "ClaudeChat:GoogleCalendar:Subcalendar": (
                "list Google calendars, Chat"
            ),
            "ClaudeCowork:GoogleCalendar:Subcalendar": (
                "list Google calendars, Cowork"
            ),
            "ClaudeiOSChat:Calendar:Subcalendar": "list calendars, iOS",
        },
    ),
    "notebook-edit": (
        "edit Jupyter cells",
        {
            "ClaudeCode:NotebookEdit": "edit notebook cells",
        },
    ),
    "remote-trigger": (
        "trigger remote agent runs",
        {
            "ClaudeCode:RemoteTrigger": "trigger cloud agent run",
        },
    ),
    "skill": (
        "invoke skills",
        {
            "ClaudeCode:Skill": "invoke `/skill-name`",
        },
    ),
    "design-sync": (
        "sync design assets",
        {
            "ClaudeCode:DesignSync": "sync design state",
        },
    ),
    "report-findings": (
        "report code-review findings",
        {
            "ClaudeCode:ReportFindings": "emit structured review findings",
        },
    ),
    "schedule-wakeup": (
        "schedule loop resume",
        {
            "ClaudeCode:ScheduleWakeup": "resume `/loop` dynamic mode",
        },
    ),
    "monitor": (
        "stream background events",
        {
            "ClaudeCode:Monitor": "stream process events",
        },
    ),
    "git": (
        "run git commands",
        {
            "git": "run git with Bash permissions configured",
        },
    ),
    # target diffusion model, not a Claude tool: on every Claude surface by
    # default, like `git`
    "image-model": (
        "target diffusion image model",
        {
            "QwenImage": "target Qwen-Image and Qwen-Image-Edit",
        },
    ),
}

# affordance name -> its variant canonical names, derived from
# `BUILTIN_AFFORDANCES`
AFFORDANCE_GROUPS = {
    affordance_name: tuple(variants)
    for affordance_name, (_, variants) in BUILTIN_AFFORDANCES.items()
}


# Main Entry Point  ############################################################
def register_builtin_affordances():
    """
    register every affordance and variant of ``BUILTIN_AFFORDANCES``,
    remarks included, skipping any already registered, so a repeated
    call stays idempotent instead of raising
    """
    for affordance_name, (remark, variants) in BUILTIN_AFFORDANCES.items():
        if affordance_name not in affordance_registry:
            register_affordance(affordance_name, remark)
        for canonical_name, variant_remark in variants.items():
            if canonical_name in variant_registry:
                continue
            register_variant(
                canonical_name,
                affordance_name=affordance_name,
                remark=variant_remark,
            )

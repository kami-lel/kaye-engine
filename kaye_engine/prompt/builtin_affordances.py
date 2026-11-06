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
            "Claude:ask_user_input_v0": "show tappable multiple-choice",
            "Claude:AskUserQuestion": "ask selectable-option question",
            "Hermes:clarify": "ask question, get decision",
        },
    ),
    "file-edit": (
        "view and edit files",
        {
            "Claude:view/str_replace/create_file~": (
                "edit sandbox files"
            ),
            "Claude:Read/Write/Edit~": "edit local files",
            "Hermes:read_file": "read file with line numbers",
            "Hermes:write_file": "write or overwrite file",
            "Hermes:patch": "find-and-replace edit in file",
        },
    ),
    "task-tracking": (
        "track session tasks",
        {
            "Claude:TodoWrite": "keep session to-do list",
            "Claude:Task~": "manage background tasks",
            "Hermes:todo_list": "track multi-step task list",
        },
    ),
    "file-delivery": (
        "send files to user",
        {
            "Claude:SendUserFile": "send local file",
            "Claude:present_files": "present sandbox files",
        },
    ),
    "cli": (
        "run shell commands",
        {
            "Claude:Bash": "run shell command",
            "Claude:PowerShell": "run PowerShell command",
            "Claude:bash_tool": "run sandbox shell command",
            "Claude:Terminal~": "drive in-app terminal tabs",
            "Hermes:terminal": "run shell commands",
            "Hermes:process_manage": "poll, wait on, kill processes",
            "Hermes:execute_code": "run Python calling Hermes tools",
            "Hermes:read_terminal": "read in-app terminal pane",
            "Hermes:close_terminal": "hide process terminal tab",
        },
    ),
    "agent": (
        "launch and message subagents",
        {
            "Claude:Agent~": "manage subagents and sessions",
            "Claude:ccd_session~": "start and hand off sessions",
            "Claude:ccd_session_mgmt~": "list, edit, stop sessions",
            "Hermes:delegate_task": "spawn isolated subagents",
        },
    ),
    "plan-mode": (
        "plan before editing",
        {
            "Claude:Enter/ExitPlanMode": "toggle planning mode",
        },
    ),
    "worktree": (
        "isolate work in a git worktree",
        {
            "Claude:Enter/ExitWorktree": "enter and exit worktree",
        },
    ),
    "cron": (
        "schedule cloud agents",
        {
            "Claude:CronCreate/Delete/List": "manage scheduled agents",
            "Claude:CodeRemote~": "manage remote repos and triggers",
            "Claude:ScheduledTasks~": "manage scheduled local tasks",
            "Hermes:cronjob_manage": "schedule and manage cron jobs",
        },
    ),
    "memory": (
        "store persistent memory",
        {
            "Claude:memory~": "read and write memory files",
            "Hermes:memory": "save durable facts across sessions",
        },
    ),
    "places-map-display": (
        "show places on a map",
        {
            "Claude:places_map_display_v0": "show map of places",
        },
    ),
    "places-list-display": (
        "show places as a list",
        {
            "Claude:places_list_display_v0": "show list of places",
        },
    ),
    "recipe-display": (
        "show recipe card",
        {
            "Claude:recipe_display_v0": "show scalable recipe card",
        },
    ),
    "itinerary-display": (
        "show travel itinerary card",
        {
            "Claude:itinerary_display_v0": "show day-by-day itinerary",
        },
    ),
    "step-card-display": (
        "show step-by-step card",
        {
            "Claude:step_card_display_v0": "show numbered steps",
        },
    ),
    "options-card-display": (
        "show alternatives card",
        {
            "Claude:options_card_display_v0": "show multi-approach options",
        },
    ),
    "comparison-card-display": (
        "show product comparison card",
        {
            "Claude:comparison_card_display_v0": (
                "show side-by-side comparison"
            ),
        },
    ),
    "featured-card-display": (
        "show best-pick product card",
        {
            "Claude:featured_card_display_v0": "show single best pick",
        },
    ),
    "product-carousel-display": (
        "show product carousel",
        {
            "Claude:product_carousel_display_v0": "show paged products",
        },
    ),
    "link-preview-display": (
        "show link preview cards",
        {
            "Claude:link_preview_display_v0": "show external link previews",
        },
    ),
    "visualize-show-widget": (
        "render inline diagram or widget",
        {
            "Claude:visualize:show_widget": "render inline SVG or HTML",
        },
    ),
    "artifact": (
        "publish shareable web page",
        {
            "Claude:Artifact": "publish HTML page",
            "Claude:RemoteArtifact~": "manage remote device artifacts",
        },
    ),
    "push-notification": (
        "send push notification",
        {
            "Claude:PushNotification": "send push notification",
            "Claude:Inbox~": "read inbox and notifications",
        },
    ),
    "weather-fetch": (
        "fetch weather by location",
        {
            "Claude:weather_fetch": "look up weather",
        },
    ),
    "places-search": (
        "search places",
        {
            "Claude:places_search": "search Google Places",
        },
    ),
    "message-compose": (
        "draft messages",
        {
            "Claude:message_compose_v1": "draft email, Slack, text",
        },
    ),
    "web": (
        "search and fetch web pages",
        {
            "Claude:Web~": "search and fetch web pages",
            "Hermes:web_search": "search the web",
            "Hermes:web_extract": "extract page or PDF content",
        },
    ),
    "email-management": (
        "read and send email",
        {
            "Claude:Gmail": "use Gmail",
        },
    ),
    "getting-things-done": (
        "manage tasks",
        {
            "Claude:TickTick": "use TickTick",
        },
    ),
    "calendar-event-edit": (
        "edit calendar events",
        {
            "Claude:GoogleCalendar:EventEdit": "edit Google Calendar",
            "Claude:iOS:Calendar:EventEdit": "edit calendar, iOS",
        },
    ),
    "calendar-event-info": (
        "look up calendar events",
        {
            "Claude:GoogleCalendar:EventInfo": (
                "look up Google Calendar"
            ),
            "Claude:iOS:Calendar:EventInfo": "look up calendar, iOS",
        },
    ),
    "calendar-subcalendar": (
        "list calendars",
        {
            "Claude:GoogleCalendar:Subcalendar": (
                "list Google calendars"
            ),
            "Claude:iOS:Calendar:Subcalendar": "list calendars, iOS",
        },
    ),
    "notebook-edit": (
        "edit Jupyter cells",
        {
            "Claude:NotebookEdit": "edit notebook cells",
        },
    ),
    "remote-trigger": (
        "trigger remote agent runs",
        {
            "Claude:RemoteTrigger": "trigger cloud agent run",
        },
    ),
    "skill": (
        "invoke skills",
        {
            "Claude:Skill": "invoke `/skill-name`",
            "Claude:~Skills": "list, search, suggest skills",
            "Hermes:skills_list": "list available skills",
            "Hermes:skill_view": "load skill content and files",
            "Hermes:skill_manage": "create, patch, delete skills",
        },
    ),
    "design-sync": (
        "sync design assets",
        {
            "Claude:DesignSync": "sync design state",
        },
    ),
    "report-findings": (
        "report code-review findings",
        {
            "Claude:ReportFindings": "emit structured review findings",
        },
    ),
    "schedule-wakeup": (
        "schedule loop resume",
        {
            "Claude:ScheduleWakeup": "resume `/loop` dynamic mode",
        },
    ),
    "monitor": (
        "stream background events",
        {
            "Claude:Monitor": "stream process events",
        },
    ),
    "file-search": (
        "search files by name or content",
        {
            "Claude:FileSearch~": "glob and grep local files",
            "Hermes:search_files": "search contents or find files by name",
        },
    ),
    "tool": (
        "discover deferred tools",
        {
            "Claude:ToolSearch": "load deferred tool schemas",
            "Hermes:tool_search": "search deferred tool catalog",
            "Hermes:tool_describe": "load deferred tool schema",
            "Hermes:tool_call": "invoke deferred tool",
        },
    ),
    "user-message": (
        "message the user directly",
        {
            "Claude:SendUserMessage": "send message to user",
            "Claude:ShowOnboardingRolePicker": "show onboarding role picker",
        },
    ),
    "connector": (
        "find and enable connectors",
        {
            "Claude:Connector~": "list, search, suggest connectors",
            "Claude:ccd_connectors~": "manage session connectors",
        },
    ),
    "plugin": (
        "find and install plugins",
        {
            "Claude:Plugin~": "list, search, suggest plugins",
        },
    ),
    "mcp-resource": (
        "read MCP server resources",
        {
            "Claude:McpResource~": "list and read MCP resources",
        },
    ),
    "doc": (
        "create and edit living docs",
        {
            "Claude:Docs~": "create, query, edit docs",
        },
    ),
    "pdf-viewer": (
        "display PDF files",
        {
            "Claude:PDFViewer~": "list and display PDFs",
        },
    ),
    "browser": (
        "drive a web browser",
        {
            "Claude:Browser~": "control built-in browser",
            "Claude:Chrome~": "control Chrome via extension",
            "Claude:RemoteBrowser~": "control browser on remote device",
            "Hermes:browser_navigate": "navigate to URL",
            "Hermes:browser_back": "go back in history",
            "Hermes:browser_click": "click element by ref ID",
            "Hermes:browser_type": "type text into field",
            "Hermes:browser_press": "press keyboard key",
            "Hermes:browser_scroll": "scroll page up or down",
            "Hermes:browser_snapshot": "snapshot page text with ref IDs",
            "Hermes:browser_console": "read console, evaluate JS",
            "Hermes:browser_get_images": "list page images with URLs",
            "Hermes:browser_vision": "screenshot page for inspection",
        },
    ),
    "computer-use": (
        "control a desktop by screen",
        {
            "Claude:ComputerUse~": "control local desktop apps",
            "Claude:RemoteDevice~": "control remote device desktop and files",
        },
    ),
    "ide-diagnostics": (
        "read IDE diagnostics",
        {
            "Claude:getDiagnostics": "read editor errors and warnings",
        },
    ),
    "app-management": (
        "manage the desktop app",
        {
            "Claude:ccd_directory~": "change and propose directories",
            "Claude:ccd_host~": "manage host worktrees and storage",
            "Claude:ccd_pr~": "bind pull requests, set auto-merge",
            "Claude:ccd_settings~": "read and set app settings",
            "Claude:ccd_sidebar~": "organize sidebar groups, sections",
            "Claude:ccd_turn~": "update plan, wrap up turn",
            "Claude:ccd_view~": "show and close panes",
            "Claude:ccd_window~": "manage window splits and layout",
        },
    ),
    "chat-utility": (
        "use chat app utilities",
        {
            "Claude:claude_ai~": "time, location, image search, research",
            "Claude:widgets~": "sports data, quiz, translation, chart",
        },
    ),
    "browser-vault": (
        "use browser password vault",
        {
            "Hermes:browser_vault_list": "list saved logins, cards, addresses",
            "Hermes:browser_vault_fill": "fill page from vault item",
            "Hermes:browser_vault_save_login": "save site login to vault",
            "Hermes:browser_vault_enter_code": "enter one-time or 2FA code",
            "Hermes:browser_vault_unlock": "prompt user to unlock vault",
        },
    ),
    "image-vision": (
        "look at images",
        {
            "Hermes:vision_analyze": "load image to view it",
        },
    ),
    "text-to-speech": (
        "speak text aloud",
        {
            "Hermes:text_to_speech": "convert text to speech audio",
        },
    ),
    "session-search": (
        "search past sessions",
        {
            "Hermes:session_search": "search or read past sessions",
        },
    ),
    "desktop": (
        "drive desktop app panes",
        {
            "Hermes:desktop_preview": "open, close, read preview pane",
            "Hermes:drive_preview": "interact with preview page",
            "Hermes:annotate_preview": "highlight preview elements",
            "Hermes:focus_pane": "reveal and focus pane",
            "Hermes:apply_layout": "apply saved layout preset",
            "Hermes:desktop_project": "create or switch Projects",
            "Hermes:read_window_below": "identify window behind app",
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

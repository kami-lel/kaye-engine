"""
claude_affordances.py

define ``_register_claude_affordances`` -- registers every Claude
affordance from ``docs/claude-doc.md`` into ``affordance_registry`` via
``register_affordance``; called automatically from ``setup_claude_cli``,
so no consumer project registers these itself. Generic registration only
(name/description) -- per-surface membership is owned entirely by
``ClaudeSurface`` and is not touched here.
"""

from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    register_affordance,
)

__all__ = ()

# (canonical_name, display_name, remark)
_AFFORDANCES = (
    (
        "ClaudeChat:ask_user_input_v0",
        "ask_user_input_v0",
        "show tappable multiple-choice questions",
    ),
    (
        "ClaudeCowork:AskUserQuestion",
        "AskUserQuestion",
        "asks the user a clarifying question with selectable options",
    ),
    (
        "ClaudeChat:places_map_display_v0",
        "places_map_display_v0",
        "show places on a map",
    ),
    (
        "ClaudeChat:places_list_display_v0",
        "places_list_display_v0",
        "show places as a browsable list",
    ),
    (
        "ClaudeChat:recipe_display_v0",
        "recipe_display_v0",
        "interactive scalable recipe card",
    ),
    (
        "ClaudeChat:itinerary_display_v0",
        "itinerary_display_v0",
        "day-by-day travel itinerary card",
    ),
    (
        "ClaudeChat:step_card_display_v0",
        "step_card_display_v0",
        "numbered step-by-step walkthrough card",
    ),
    (
        "ClaudeChat:options_card_display_v0",
        "options_card_display_v0",
        "multi-approach options card",
    ),
    (
        "ClaudeChat:comparison_card_display_v0",
        "comparison_card_display_v0",
        "side-by-side product comparison card",
    ),
    (
        "ClaudeChat:featured_card_display_v0",
        "featured_card_display_v0",
        "single best-pick product card",
    ),
    (
        "ClaudeChat:product_carousel_display_v0",
        "product_carousel_display_v0",
        "paged product browsing card",
    ),
    (
        "ClaudeChat:link_preview_display_v0",
        "link_preview_display_v0",
        "external link preview cards",
    ),
    (
        "ClaudeChat:visualize:show_widget",
        "visualize:show_widget",
        "renders inline SVG/HTML diagram, chart, or widget",
    ),
    (
        "ClaudeCode:Artifact",
        "Artifact",
        "publishes an HTML/Markdown page as a shareable web artifact",
    ),
    (
        "ClaudeCode:SendUserFile",
        "SendUserFile",
        "sends a local file to the user",
    ),
    (
        "ClaudeCode:PushNotification",
        "PushNotification",
        "sends a push notification",
    ),
    (
        "ClaudeChat:memory_",
        "memory_read/.../memory_list",
        "read, write, append, edit, delete, and list memory files",
    ),
    ("ClaudeChat:weather_fetch", "weather_fetch", "weather by location"),
    ("ClaudeChat:places_search", "places_search", "search Google Places"),
    (
        "ClaudeChat:message_compose_v1",
        "message_compose_v1",
        "drafts email/Slack/text with strategic variants",
    ),
    ("ClaudeCode:NotebookEdit", "NotebookEdit", "edits Jupyter notebook cells"),
    (
        "ClaudeCode:RemoteTrigger",
        "RemoteTrigger",
        "triggers a remote/cloud agent run",
    ),
    ("ClaudeCowork:Skill", "Skill", "invokes a packaged skill (/skill-name)"),
    ("ClaudeCode:DesignSync", "DesignSync", "syncs design assets/state"),
    (
        "ClaudeCode:ReportFindings",
        "ReportFindings",
        "emits structured code-review findings",
    ),
    (
        "ClaudeCode:Enter/ExitPlanMode",
        "EnterPlanMode/ExitPlanMode",
        "toggles planning mode",
    ),
    (
        "ClaudeCode:Enter/ExitWorktree",
        "EnterWorktree/ExitWorktree",
        "creates/switches into and exits an isolated git worktree session",
    ),
    (
        "ClaudeCode:ScheduleWakeup",
        "ScheduleWakeup",
        "schedules a future self-resumption for /loop dynamic mode",
    ),
    (
        "ClaudeCode:CronCreate/Delete/List",
        "CronCreate/CronDelete/CronList",
        "creates, deletes, and lists scheduled cloud agents",
    ),
    (
        "ClaudeCode:Monitor",
        "Monitor",
        "streams events from a background process",
    ),
    ("ClaudeCode:SendMessage", "SendMessage", "messages another agent/session"),
    (
        "ClaudeCowork:Agent",
        "Agent",
        "launches a subagent for multi-step or research tasks",
    ),
    (
        "ClaudeVSC:ListAgents",
        "ListAgents",
        "lists other agents/sessions reachable via SendMessage",
    ),
    (
        "ClaudeCode:TaskCreate",
        "TaskCreate",
        "creates a tracked background task",
    ),
    ("ClaudeCode:TaskGet", "TaskGet", "gets a task's details"),
    ("ClaudeCode:TaskList", "TaskList", "lists tracked tasks"),
    (
        "ClaudeCode:TaskOutput",
        "TaskOutput",
        "fetches output from a background task",
    ),
    ("ClaudeCowork:TaskStop", "TaskStop", "stops a background task"),
    ("ClaudeCode:TaskUpdate", "TaskUpdate", "updates a task's state"),
    (
        "ClaudeVSC:TodoWrite",
        "TodoWrite",
        "maintains a task/todo list for the session",
    ),
)


# Main Entry Point  ############################################################
def register_claude_affordances():
    """
    register every row in ``_AFFORDANCES`` into ``affordance_registry``
    via ``register_affordance``, skipping any ``canonical_name`` already
    registered -- keeps repeated ``setup_claude_cli(...)`` calls within
    one process idempotent instead of raising on the second call
    """
    for canonical_name, display_name, remark in _AFFORDANCES:
        if canonical_name in affordance_registry:
            continue
        register_affordance(canonical_name, display_name, remark=remark)

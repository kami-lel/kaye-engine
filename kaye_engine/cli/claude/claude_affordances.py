"""
claude_affordances.py

define ``_register_claude_affordances`` -- registers every Claude
affordance from ``docs/claude-doc.md`` into ``affordance_registry`` via
``register_affordance``; called automatically from ``setup_claude_cli``,
so no consumer project registers these itself. Per-surface membership is
owned entirely by ``ClaudeSurface`` and is not touched here.
"""

from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    register_affordance,
)

__all__ = ()

_AFFORDANCES = (
    "ClaudeChat:ask_user_input_v0",
    "ClaudeCode:AskUserQuestion",
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
    "ClaudeCode:Artifact",
    "ClaudeCode:SendUserFile",
    "ClaudeCode:PushNotification",
    "ClaudeChat:memory_",
    "ClaudeChat:weather_fetch",
    "ClaudeChat:places_search",
    "ClaudeChat:message_compose_v1",
    "ClaudeCode:NotebookEdit",
    "ClaudeCode:RemoteTrigger",
    "ClaudeCode:Skill",
    "ClaudeCode:DesignSync",
    "ClaudeCode:ReportFindings",
    "ClaudeCode:Enter/ExitPlanMode",
    "ClaudeCode:Enter/ExitWorktree",
    "ClaudeCode:ScheduleWakeup",
    "ClaudeCode:CronCreate/Delete/List",
    "ClaudeCode:Monitor",
    "ClaudeCode:SendMessage",
    "ClaudeCode:Agent",
    "ClaudeCode:ListAgents",
    "ClaudeCode:TaskCreate",
    "ClaudeCode:TaskGet",
    "ClaudeCode:TaskList",
    "ClaudeCode:TaskOutput",
    "ClaudeCode:TaskStop",
    "ClaudeCode:TaskUpdate",
    "ClaudeCode:TodoWrite",
    "git",
    "Claude",
    "ClaudeChat",
    "ClaudeCowork",
    "ClaudeCode",
)


# Main Entry Point  #################################################################

def register_claude_affordances():
    """
    register every name in ``_AFFORDANCES`` into ``affordance_registry``
    via ``register_affordance``, skipping any ``canonical_name`` already
    registered -- keeps repeated ``setup_claude_cli(...)`` calls within
    one process idempotent instead of raising on the second call
    """
    for canonical_name in _AFFORDANCES:
        if canonical_name in affordance_registry:
            continue
        register_affordance(canonical_name)

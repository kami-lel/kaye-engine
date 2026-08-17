# Kaye Engine: affordances

Every affordance Kaye Engine registers for Claude platform tools
(`kaye_engine/cli/claude/claude_affordances.py`), and which surface(s)
each is available on (`kaye_engine/prompt/claude_surface.py`).

Q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md#affordances) for the
underlying `{[canonical_name] Usage}` / `{[canonical_name] Lack}`
mechanism these tables describe.




#### Platform Identity

| affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- |
| `Claude` | ✔️ | ✔️ | ✔️ | ✔️ | any Claude surface is active |
| `ClaudeChat` | ✔️ | ❌ | ❌ | ❌ | running specifically as Claude Chat |
| `ClaudeCowork` | ❌ | ✔️ | ❌ | ❌ | running specifically as Claude Cowork |
| `ClaudeCode` | ❌ | ❌ | ✔️ | ❌ | running specifically as Claude Code |
| `git` | ❌ | ❌ | ❌ | ✔️ | git Bash command permissions have been configured (`claude vs-code-extension` only) |

[^chat]: i.e. Claude.ai.
[^vsc]: i.e. Claude Code VS Code Extension.
[^affordance]: q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md#affordances).




#### User Interaction

| tool | affordance[^affordance] | Chat[^chat] | Cowork | Code | VSC[^vsc] | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `ask_user_input_v0` | `ClaudeChat:ask_user_input_v0` | ✔️ | ❌ | ❌ | ❌ | show tappable multiple-choice questions |
| `AskUserQuestion` | `ClaudeCode:AskUserQuestion` | ❌ | ✔️ | ✔️ | ✔️ | asks the user a clarifying question with selectable options |
| `places_map_display_v0` | `ClaudeChat:places_map_display_v0` | ✔️ | ❌ | ❌ | ❌ | show places on a map |
| `places_list_display_v0` | `ClaudeChat:places_list_display_v0` | ✔️ | ❌ | ❌ | ❌ | show places as a browsable list |
| `recipe_display_v0` | `ClaudeChat:recipe_display_v0` | ✔️ | ❌ | ❌ | ❌ | interactive scalable recipe card |
| `itinerary_display_v0` | `ClaudeChat:itinerary_display_v0` | ✔️ | ❌ | ❌ | ❌ | day-by-day travel itinerary card |
| `step_card_display_v0` | `ClaudeChat:step_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | numbered step-by-step walkthrough card |
| `options_card_display_v0` | `ClaudeChat:options_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | multi-approach options card |
| `comparison_card_display_v0` | `ClaudeChat:comparison_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | side-by-side product comparison card |
| `featured_card_display_v0` | `ClaudeChat:featured_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | single best-pick product card |
| `product_carousel_display_v0` | `ClaudeChat:product_carousel_display_v0` | ✔️ | ❌ | ❌ | ❌ | paged product browsing card |
| `link_preview_display_v0` | `ClaudeChat:link_preview_display_v0` | ✔️ | ❌ | ❌ | ❌ | external link preview cards |
| `visualize:show_widget` | `ClaudeChat:visualize:show_widget` | ✔️ | ❌ | ❌ | ❌ | renders inline SVG/HTML diagram, chart, or widget |
| `Artifact` | `ClaudeCode:Artifact` | ❌ | ❌ | ✔️ | ✔️ | publishes an HTML/Markdown page as a shareable web artifact |
| `SendUserFile` | `ClaudeCode:SendUserFile` | ❌ | ❌ | ✔️ | ✔️ | sends a local file to the user |
| `PushNotification` | `ClaudeCode:PushNotification` | ❌ | ❌ | ✔️ | ✔️ | sends a push notification |




#### Data & Communication

| tool | affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `memory_read`,<br>`memory_write`,<br>`memory_append`,<br>`memory_str_replace`,<br>`memory_delete`,<br>`memory_list` | `ClaudeChat:memory_` | ✔️ | ❌ | ❌ | ❌ | read, write, append, edit, delete, and list memory files |
| `weather_fetch` | `ClaudeChat:weather_fetch` | ✔️ | ❌ | ❌ | ❌ | weather by location |
| `places_search` | `ClaudeChat:places_search` | ✔️ | ❌ | ❌ | ❌ | search Google Places |
| `message_compose_v1` | `ClaudeChat:message_compose_v1` | ✔️ | ❌ | ❌ | ❌ | drafts email/Slack/text with strategic variants |
| `NotebookEdit` | `ClaudeCode:NotebookEdit` | ❌ | ❌ | ✔️ | ✔️ | edits Jupyter notebook cells |
| `RemoteTrigger` | `ClaudeCode:RemoteTrigger` | ❌ | ❌ | ✔️ | ✔️ | triggers a remote/cloud agent run |




#### Development

| tool | affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `Skill` | `ClaudeCode:Skill` | ❌ | ✔️ | ✔️ | ✔️ | invokes a packaged skill (`/skill-name`) |
| `DesignSync` | `ClaudeCode:DesignSync` | ❌ | ❌ | ✔️ | ✔️ | syncs design assets/state |
| `ReportFindings` | `ClaudeCode:ReportFindings` | ❌ | ❌ | ✔️ | ✔️ | emits structured code-review findings |
| `EnterPlanMode`<br>`ExitPlanMode` | `ClaudeCode:Enter/ExitPlanMode` | ❌ | ❌ | ✔️ | ✔️ | toggles planning mode |
| `EnterWorktree`<br>`ExitWorktree` | `ClaudeCode:Enter/ExitWorktree` | ❌ | ❌ | ✔️ | ✔️ | creates/switches into and exits an isolated git worktree session |
| `ScheduleWakeup` | `ClaudeCode:ScheduleWakeup` | ❌ | ❌ | ✔️ | ✔️ | schedules a future self-resumption for `/loop` dynamic mode |
| `CronCreate`,<br>`CronDelete`,<br>`CronList` | `ClaudeCode:CronCreate/Delete/List` | ❌ | ❌ | ✔️ | ✔️ | creates, deletes, and lists scheduled cloud agents |
| `Monitor` | `ClaudeCode:Monitor` | ❌ | ❌ | ✔️ | ✔️ | streams events from a background process |




#### Agents & Tasks

| tool | affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `SendMessage` | `ClaudeCode:SendMessage` | ❌ | ❌ | ✔️ | ✔️ | messages another agent/session |
| `Agent` | `ClaudeCode:Agent` | ❌ | ✔️ | ✔️ | ✔️ | launches a subagent for multi-step or research tasks |
| `ListAgents` | `ClaudeCode:ListAgents` | ❌ | ❌ | ❌ | ✔️ | lists other agents/sessions reachable via `SendMessage` |
| `TaskCreate` | `ClaudeCode:TaskCreate` | ❌ | ❌ | ✔️ | ✔️ | creates a tracked background task |
| `TaskGet` | `ClaudeCode:TaskGet` | ❌ | ❌ | ✔️ | ✔️ | gets a task's details |
| `TaskList` | `ClaudeCode:TaskList` | ❌ | ❌ | ✔️ | ✔️ | lists tracked tasks |
| `TaskOutput` | `ClaudeCode:TaskOutput` | ❌ | ❌ | ✔️ | ✔️ | fetches output from a background task |
| `TaskStop` | `ClaudeCode:TaskStop` | ❌ | ✔️ | ✔️ | ✔️ | stops a background task |
| `TaskUpdate` | `ClaudeCode:TaskUpdate` | ❌ | ❌ | ✔️ | ✔️ | updates a task's state |
| `TodoWrite` | `ClaudeCode:TodoWrite` | ❌ | ❌ | ❌ | ✔️ | maintains a task/todo list for the session |

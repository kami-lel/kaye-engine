# Kaye Engine support for Anthropic Claude

Kaye Engine's integration with Anthropic Claude: exporting corpus blueprints as Claude plugins, skills, and system prompts.













## available CLI commands

`kaye-engine claude` exposes one subcommand per Claude export target:

```bash
kaye-engine claude skill                # export exportables as Skill folders or .zip packages
kaye-engine claude plugin               # export exportables as a plugin folder or .zip package
kaye-engine claude marketplace          # export a marketplace folder for the Claude sidebar
kaye-engine claude code                 # export a plugin plus CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt   # export a blueprint as ~/.claude/CLAUDE.md
kaye-engine claude vs-code-extension    # export CLAUDE.md, marketplace, and settings.json
                                        # into ~/.claude for the Claude Code VS Code Extension
```

> [!TIP]
> Run `kaye-engine claude [SUBCOMMAND] -h` to see full documentation.

> [!NOTE]
>  All (non-internal) exportables in  `exportable_registry` will be rendered





#### Claude Desktop

Generate a plugin package using the Kaye Engine CLI:

```bash
kaye-engine claude plugin --zip
```

----

Upload the generated `.zip` file to [Claude Desktop](https://claude.ai) settings under *Plugins* to enable Kaye Engine integration.





#### Claude Code VS Code Extension

Set up Kaye Engine for the Claude Code VS Code Extension with one command:

```bash
kaye-engine claude vs-code-extension
```

This writes the User System Prompt to `~/.claude/CLAUDE.md`, creates a
`~/.claude/<marketplace folder name>/` folder containing the plugin, and
configures Bash command permissions in `~/.claude/settings.json` —
covering git, system commands (`sudo`, `kill`, `systemctl`), package
managers, `pytest`, and `docker`. Marketplace folder name set via
`setup_claude_cli(~~)`.

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/<marketplace folder name>/` and click
   *Install*.













## Consumer Requirement

A corpus must supply a node at `Agentic` → `Claude Behavior`, and register a Chat blueprint and a Coder blueprint under whatever names the consumer passes to `setup_claude_cli(...)`; `user_prompt/export.py` resolves them via `get_claude_chat_blueprint()`/`get_claude_coder_blueprint()` in `blueprint_name.py`.

----

A `claude`-exporting consumer must call `setup_claude_cli(~~)` before invoking the. The version passed here is the consumer's own, stamped into every `plugin.json`, `marketplace.json`, and `SKILL.md` the CLI writes













## Conditional Sidecar Inclusion

<!--
BUG better surfaced based sidecar org
TODO TODO special kind tool sidecar, w/ sidecar usage/lack
-->

Q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md) for the sidecar node concept and how they're authored in the prompt corpus.



#### User Interaction

| tool | affordance | Chat[^chat] | Cowork | Code | VSC[^vsc] | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `ask_user_input_v0` | `ask_user_input_v0` | ✔️ | ❌ | ❌ | ❌ | show tappable multiple-choice questions |
| `AskUserQuestion` | `AskUserQuestion` | ❌ | ✔️ | ✔️ | ✔️ | asks the user a clarifying question with selectable options |
| `places_map_display_v0` | `places_map_display_v0` | ✔️ | ❌ | ❌ | ❌ | show places on a map |
| `places_list_display_v0` | `places_list_display_v0` | ✔️ | ❌ | ❌ | ❌ | show places as a browsable list |
| `recipe_display_v0` | `recipe_display_v0` | ✔️ | ❌ | ❌ | ❌ | interactive scalable recipe card |
| `itinerary_display_v0` | `itinerary_display_v0` | ✔️ | ❌ | ❌ | ❌ | day-by-day travel itinerary card |
| `step_card_display_v0` | `step_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | numbered step-by-step walkthrough card |
| `options_card_display_v0` | `options_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | multi-approach options card |
| `comparison_card_display_v0` | `comparison_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | side-by-side product comparison card |
| `featured_card_display_v0` | `featured_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | single best-pick product card |
| `product_carousel_display_v0` | `product_carousel_display_v0` | ✔️ | ❌ | ❌ | ❌ | paged product browsing card |
| `link_preview_display_v0` | `link_preview_display_v0` | ✔️ | ❌ | ❌ | ❌ | external link preview cards |
| `visualize:show_widget` | `visualize:show_widget` | ✔️ | ❌ | ❌ | ❌ | renders inline SVG/HTML diagram, chart, or widget |
| `Artifact` | `Artifact` | ❌ | ❌ | ✔️ | ✔️ | publishes an HTML/Markdown page as a shareable web artifact |
| `SendUserFile` | `SendUserFile` | ❌ | ❌ | ✔️ | ✔️ | sends a local file to the user |
| `PushNotification` | `PushNotification` | ❌ | ❌ | ✔️ | ✔️ | sends a push notification |

[^chat]: i.e. Claude.ai.
[^vsc]: i.e. Claude Code VS Code Extension.



#### Data & Communication

| tool | affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `memory_read`,<br>`memory_write`,<br>`memory_append`,<br>`memory_str_replace`,<br>`memory_delete`,<br>`memory_list` | `memory_` | ✔️ | ❌ | ❌ | ❌ | read, write, append, edit, delete, and list memory files |
| `weather_fetch` | `weather_fetch` | ✔️ | ❌ | ❌ | ❌ | weather by location |
| `places_search` | `places_search` | ✔️ | ❌ | ❌ | ❌ | search Google Places |
| `message_compose_v1` | `message_compose_v1` | ✔️ | ❌ | ❌ | ❌ | drafts email/Slack/text with strategic variants |
| `NotebookEdit` | `NotebookEdit` | ❌ | ❌ | ✔️ | ✔️ | edits Jupyter notebook cells |
| `RemoteTrigger` | `RemoteTrigger` | ❌ | ❌ | ✔️ | ✔️ | triggers a remote/cloud agent run |



#### Development

| tool | affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `Skill` | `Skill` | ❌ | ✔️ | ✔️ | ✔️ | invokes a packaged skill (`/skill-name`) |
| `DesignSync` | `DesignSync` | ❌ | ❌ | ✔️ | ✔️ | syncs design assets/state |
| `ReportFindings` | `ReportFindings` | ❌ | ❌ | ✔️ | ✔️ | emits structured code-review findings |
| `EnterPlanMode`<br>`ExitPlanMode` | `Enter/ExitPlanMode` | ❌ | ❌ | ✔️ | ✔️ | toggles planning mode |
| `EnterWorktree`<br>`ExitWorktree` | `Enter/ExitWorktree` | ❌ | ❌ | ✔️ | ✔️ | creates/switches into and exits an isolated git worktree session |
| `ScheduleWakeup` | `ScheduleWakeup` | ❌ | ❌ | ✔️ | ✔️ | schedules a future self-resumption for `/loop` dynamic mode |
| `CronCreate`,<br>`CronDelete`,<br>`CronList` | `CronCreate/Delete/List` | ❌ | ❌ | ✔️ | ✔️ | creates, deletes, and lists scheduled cloud agents |
| `Monitor` | `Monitor` | ❌ | ❌ | ✔️ | ✔️ | streams events from a background process |



#### Agents & Tasks

| tool | affordance | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `SendMessage` | `SendMessage` | ❌ | ❌ | ✔️ | ✔️ | messages another agent/session |
| `Agent` | `Agent` | ❌ | ✔️ | ✔️ | ✔️ | launches a subagent for multi-step or research tasks |
| `ListAgents` | `ListAgents` | ❌ | ❌ | ❌ | ✔️ | lists other agents/sessions reachable via `SendMessage` |
| `TaskCreate` | `TaskCreate` | ❌ | ❌ | ✔️ | ✔️ | creates a tracked background task |
| `TaskGet` | `TaskGet` | ❌ | ❌ | ✔️ | ✔️ | gets a task's details |
| `TaskList` | `TaskList` | ❌ | ❌ | ✔️ | ✔️ | lists tracked tasks |
| `TaskOutput` | `TaskOutput` | ❌ | ❌ | ✔️ | ✔️ | fetches output from a background task |
| `TaskStop` | `TaskStop` | ❌ | ✔️ | ✔️ | ✔️ | stops a background task |
| `TaskUpdate` | `TaskUpdate` | ❌ | ❌ | ✔️ | ✔️ | updates a task's state |
| `TodoWrite` | `TodoWrite` | ❌ | ❌ | ❌ | ✔️ | maintains a task/todo list for the session |

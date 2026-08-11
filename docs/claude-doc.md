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

| tool | sidecar | Chat[^chat] | Cowork | Code | VSC[^vsc] | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `ask_user_input_v0` | `{Claude Chat [ask_user_input_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | show tappable multiple-choice questions |
| `AskUserQuestion` | `{Claude Code [AskUserQuestion] Usage}` | ❌ | ✔️ | ✔️ | ✔️ | asks the user a clarifying question with selectable options |
| `places_map_display_v0` | `{Claude Chat [places_map_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | show places on a map |
| `places_list_display_v0` | `{Claude Chat [places_list_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | show places as a browsable list |
| `recipe_display_v0` | `{Claude Chat [recipe_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | interactive scalable recipe card |
| `itinerary_display_v0` | `{Claude Chat [itinerary_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | day-by-day travel itinerary card |
| `step_card_display_v0` | `{Claude Chat [step_card_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | numbered step-by-step walkthrough card |
| `options_card_display_v0` | `{Claude Chat [options_card_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | multi-approach options card |
| `comparison_card_display_v0` | `{Claude Chat [comparison_card_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | side-by-side product comparison card |
| `featured_card_display_v0` | `{Claude Chat [featured_card_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | single best-pick product card |
| `product_carousel_display_v0` | `{Claude Chat [product_carousel_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | paged product browsing card |
| `link_preview_display_v0` | `{Claude Chat [link_preview_display_v0] Usage}` | ✔️ | ❌ | ❌ | ❌ | external link preview cards |
| `visualize:show_widget` | `{Claude Chat [visualize:show_widget] Uage}` | ✔️ | ❌ | ❌ | ❌ | renders inline SVG/HTML diagram, chart, or widget |
| `Artifact` | `{Claude Code [Artifact] Usage}` | ❌ | ❌ | ✔️ | ✔️ | publishes an HTML/Markdown page as a shareable web artifact |
| `SendUserFile` | `{Claude Code [SendUserFile] Usage}` | ❌ | ❌ | ✔️ | ✔️ | sends a local file to the user |
| `PushNotification` | `{Claude Code [PushNotification] Usage}` | ❌ | ❌ | ✔️ | ✔️ | sends a push notification |

[^chat]: i.e. Claude.ai.
[^vsc]: i.e. Claude Code VS Code Extension.



#### Data & Communication

| tool | sidecar | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `memory_read`,<br>`memory_write`,<br>`memory_append`,<br>`memory_str_replace`,<br>`memory_delete`,<br>`memory_list` | `{Claude Chat [memory_] Usage}` | ✔️ | ❌ | ❌ | ❌ | read, write, append, edit, delete, and list memory files |
| `weather_fetch` | `{Claude Chat [weather_fetch] Usage}` | ✔️ | ❌ | ❌ | ❌ | weather by location |
| `places_search` | `{Claude Chat [places_search] Usage}` | ✔️ | ❌ | ❌ | ❌ | search Google Places |
| `message_compose_v1` | `{Claude Chat [message_compose_v1] Usage}` | ✔️ | ❌ | ❌ | ❌ | drafts email/Slack/text with strategic variants |
| `NotebookEdit` | `{Claude Code [NotebookEdit] Usage}` | ❌ | ❌ | ✔️ | ✔️ | edits Jupyter notebook cells |
| `RemoteTrigger` | `{Claude Code [RemoteTrigger] Usage}` | ❌ | ❌ | ✔️ | ✔️ | triggers a remote/cloud agent run |



#### Development

| tool | sidecar | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `Skill` | `{Claude Code [Skill] Usage}` | ❌ | ✔️ | ✔️ | ✔️ | invokes a packaged skill (`/skill-name`) |
| `DesignSync` | `{Claude Code [DesignSync] Usage}` | ❌ | ❌ | ✔️ | ✔️ | syncs design assets/state |
| `ReportFindings` | `{Claude Code [ReportFindings] Usage}` | ❌ | ❌ | ✔️ | ✔️ | emits structured code-review findings |
| `EnterPlanMode`<br>`ExitPlanMode` | `{Claude Code [Enter/ExitPlanMode:] Usage}` | ❌ | ❌ | ✔️ | ✔️ | toggles planning mode |
| `EnterWorktree`<br>`ExitWorktree` | `{Claude Code [Enter/ExitWorktree] Usage}` | ❌ | ❌ | ✔️ | ✔️ | creates/switches into and exits an isolated git worktree session |
| `ScheduleWakeup` | `{Claude Code [ScheduleWakeup] Usage}` | ❌ | ❌ | ✔️ | ✔️ | schedules a future self-resumption for `/loop` dynamic mode |
| `CronCreate`,<br>`CronDelete`,<br>`CronList` | `{Claude Code [CronCreate/Delete/List] Usage}` | ❌ | ❌ | ✔️ | ✔️ | creates, deletes, and lists scheduled cloud agents |
| `Monitor` | `{Claude Code [Monitor] Usage}` | ❌ | ❌ | ✔️ | ✔️ | streams events from a background process |



#### Agents & Tasks

| tool | sidecar | Chat | Cowork | Code | VSC | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `SendMessage` | `{Claude Code [SendMessage] Usage}` | ❌ | ❌ | ✔️ | ✔️ | messages another agent/session |
| `Agent` | `{Claude Code [Agent] Usage}` | ❌ | ✔️ | ✔️ | ✔️ | launches a subagent for multi-step or research tasks |
| `ListAgents` | `{Claude Code [ListAgents] Usage}` | ❌ | ❌ | ❌ | ✔️ | lists other agents/sessions reachable via `SendMessage` |
| `TaskCreate` | `{Claude Code [TaskCreate] Usage}` | ❌ | ❌ | ✔️ | ✔️ | creates a tracked background task |
| `TaskGet` | `{Claude Code [TaskGet] Usage}` | ❌ | ❌ | ✔️ | ✔️ | gets a task's details |
| `TaskList` | `{Claude Code [TaskList] Usage}` | ❌ | ❌ | ✔️ | ✔️ | lists tracked tasks |
| `TaskOutput` | `{Claude Code [TaskOutput] Usage}` | ❌ | ❌ | ✔️ | ✔️ | fetches output from a background task |
| `TaskStop` | `{Claude Code [TaskStop] Usage}` | ❌ | ✔️ | ✔️ | ✔️ | stops a background task |
| `TaskUpdate` | `{Claude Code [TaskUpdate] Usage}` | ❌ | ❌ | ✔️ | ✔️ | updates a task's state |
| `TodoWrite` | `{Claude Code [TodoWrite] Usage}` | ❌ | ❌ | ❌ | ✔️ | maintains a task/todo list for the session |



#### Fallbacks

Utilize these *fallbacks* sidecars for specific surface:

| sidecar | Chat | Cowork | Code | VSC |
| --- | --- | --- | --- | --- |
| `{Claude Chat Fallback}` | ✔️ | ❌ | ❌ | ❌ |
| `{Claude Cowork Fallback}` | ❌ | ✔️ | ❌ | ❌ |
| `{Claude Code Fallback}` | ❌ | ❌ | ✔️ | ❌ |
| `{Claude Code VSC Extension Fallback}` | ❌ | ❌ | ❌ | ✔️ |

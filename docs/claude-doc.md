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

A corpus must supply a node at `Agent Behavior` → `Claude Behavior`, and register a Chat blueprint and a Coder blueprint under whatever names the consumer passes to `setup_claude_cli(...)`; `user_prompt/export.py` resolves them via `get_claude_chat_blueprint()`/`get_claude_coder_blueprint()` in `blueprint_name.py`.

----

A `claude`-exporting consumer must call `setup_claude_cli(~~)` before invoking the. The version passed here is the consumer's own, stamped into every `plugin.json`, `marketplace.json`, and `SKILL.md` the CLI writes













## Conditional Sidecar Inclusion

<!-- BUG better surfaced based sidecar org  -->

Q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md) for the sidecar node concept and how they're authored in the prompt corpus.

| sidecar name | tool | Chat[^chat] | Cowork | Code | VSC[^vsc] | remark |
| --- | --- | --- | --- | --- | --- | --- |
| `{Claude Chat [memory_] Usage}` | `memory_read`,<br>`memory_write`,<br>`memory_append`,<br>`memory_str_replace`,<br>`memory_delete`,<br>`memory_list` | ✔️ | ❌ | ❌ | ❌ | read, write, append, edit, delete, and list memory files |
| `{Claude Chat [ask_user_input_v0] Usage}` | `ask_user_input_v0` | ✔️ | ❌ | ❌ | ❌ | show tappable multiple-choice questions |
| `{Claude Chat [weather_fetch] Usage}` | `weather_fetch` | ✔️ | ❌ | ❌ | ❌ | weather by location |
| `{Claude Chat [places_search] Usage}` | `places_search` | ✔️ | ❌ | ❌ | ❌ | search Google Places |
| `{Claude Chat [places_map_display_v0] Usage}` | `places_map_display_v0` | ✔️ | ❌ | ❌ | ❌ | show places on a map |
| `{Claude Chat [places_list_display_v0] Usage}` | `places_list_display_v0` | ✔️ | ❌ | ❌ | ❌ | show places as a browsable list |
| `{Claude Chat [recipe_display_v0] Usage}` | `recipe_display_v0` | ✔️ | ❌ | ❌ | ❌ | interactive scalable recipe card |
| `{Claude Chat [itinerary_display_v0] Usage}` | `itinerary_display_v0` | ✔️ | ❌ | ❌ | ❌ | day-by-day travel itinerary card |
| `{Claude Chat [step_card_display_v0] Usage}` | `step_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | numbered step-by-step walkthrough card |
| `{Claude Chat [options_card_display_v0] Usage}` | `options_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | multi-approach options card |
| `{Claude Chat [comparison_card_display_v0] Usage}` | `comparison_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | side-by-side product comparison card |
| `{Claude Chat [featured_card_display_v0] Usage}` | `featured_card_display_v0` | ✔️ | ❌ | ❌ | ❌ | single best-pick product card |
| `{Claude Chat [product_carousel_display_v0] Usage}` | `product_carousel_display_v0` | ✔️ | ❌ | ❌ | ❌ | paged product browsing card |
| `{Claude Chat [link_preview_display_v0] Usage}` | `link_preview_display_v0` | ✔️ | ❌ | ❌ | ❌ | external link preview cards |
| `{Claude Chat [message_compose_v1] Usage}` | `message_compose_v1` | ✔️ | ❌ | ❌ | ❌ | drafts email/Slack/text with strategic variants |
| `{Claude Chat [visualize:show_widget] Uage}` | `visualize:show_widget` | ✔️ | ❌ | ❌ | ❌ | renders inline SVG/HTML diagram, chart, or widget |
| `{Claude Code [Agent] Usage}` | `Agent` | ❌ | ✔️ | ✔️ | ✔️ | launches a subagent for multi-step or research tasks |
| `{Claude Code [ListAgents] Usage}` | `ListAgents` | ❌ | ❌ | ❌ | ✔️ | lists other agents/sessions reachable via `SendMessage` |
| `{Claude Code [AskUserQuestion] Usage}` | `AskUserQuestion` | ❌ | ✔️ | ✔️ | ✔️ | asks the user a clarifying question with selectable options |
| `{Claude Code [Artifact] Usage}` | `Artifact` | ❌ | ❌ | ✔️ | ✔️ | publishes an HTML/Markdown page as a shareable web artifact |
| `{Claude Code [ReportFindings] Usage}` | `ReportFindings` | ❌ | ❌ | ✔️ | ✔️ | emits structured code-review findings |
| `{Claude Code [ScheduleWakeup] Usage}` | `ScheduleWakeup` | ❌ | ❌ | ✔️ | ✔️ | schedules a future self-resumption for `/loop` dynamic mode |
| `{Claude Code [SendUserFile] Usage}` | `SendUserFile` | ❌ | ❌ | ✔️ | ✔️ | sends a local file to Kami |
| `{Claude Code [Skill] Usage}` | `Skill` | ❌ | ✔️ | ✔️ | ✔️ | invokes a packaged skill (`/skill-name`) |
| `{Claude Code [ToolSearch] Usage}` | `ToolSearch` | ❌ | ✔️ | ✔️ | ✔️ | fetches full schemas for deferred tools by name or keyword |
| `{Claude Code [Write] Usage}` | `Write` | ❌ | ✔️ | ✔️ | ✔️ | creates or overwrites a file on local disk |
| `{Claude Code [CronCreate/Delete/List] Usage}` | `CronCreate`,<br>`CronDelete`,<br>`CronList` | ❌ | ❌ | ✔️ | ✔️ | creates, deletes, and lists scheduled cloud agents |
| `{Claude Code [DesignSync] Usage}` | `DesignSync` | ❌ | ❌ | ✔️ | ✔️ | syncs design assets/state |
| `{Claude Code [Enter/ExitPlanMode:] Usage}` | `EnterPlanMode`<br>`ExitPlanMode` | ❌ | ❌ | ✔️ | ✔️ | toggles planning mode |
| `{Claude Code [Enter/ExitWorktree] Usage}` | `EnterWorktree`<br>`ExitWorktree` | ❌ | ❌ | ✔️ | ✔️ | creates/switches into and exits an isolated git worktree session |
| `{Claude Code [Monitor] Usage}` | `Monitor` | ❌ | ❌ | ✔️ | ✔️ | streams events from a background process |
| `{Claude Code [NotebookEdit] Usage}` | `NotebookEdit` | ❌ | ❌ | ✔️ | ✔️ | edits Jupyter notebook cells |
| `{Claude Code [PushNotification] Usage}` | `PushNotification` | ❌ | ❌ | ✔️ | ✔️ | sends a push notification |
| `{Claude Code [RemoteTrigger] Usage}` | `RemoteTrigger` | ❌ | ❌ | ✔️ | ✔️ | triggers a remote/cloud agent run |
| `{Claude Code [SendMessage] Usage}` | `SendMessage` | ❌ | ❌ | ✔️ | ✔️ | messages another agent/session |
| `{Claude Code [TaskCreate] Usage}` | `TaskCreate` | ❌ | ❌ | ✔️ | ✔️ | creates a tracked background task |
| `{Claude Code [TaskGet] Usage}` | `TaskGet` | ❌ | ❌ | ✔️ | ✔️ | gets a task's details |
| `{Claude Code [TaskList] Usage}` | `TaskList` | ❌ | ❌ | ✔️ | ✔️ | lists tracked tasks |
| `{Claude Code [TaskOutput] Usage}` | `TaskOutput` | ❌ | ❌ | ✔️ | ✔️ | fetches output from a background task |
| `{Claude Code [TaskStop] Usage}` | `TaskStop` | ❌ | ✔️ | ✔️ | ✔️ | stops a background task |
| `{Claude Code [TaskUpdate] Usage}` | `TaskUpdate` | ❌ | ❌ | ✔️ | ✔️ | updates a task's state |
| `{Claude Code [TodoWrite] Usage}` | `TodoWrite` | ❌ | ❌ | ❌ | ✔️ | maintains a task/todo list for the session |

[^chat]: i.e. Claude.ai.
[^vsc]: i.e. Claude Code VS Code Extension.

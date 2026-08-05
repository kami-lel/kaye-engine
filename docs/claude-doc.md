# Kaye Engine support for Anthropic Claude

Kaye Engine's integration with Anthropic Claude: exporting corpus blueprints as Claude plugins, skills, and system prompts.













## available CLI commands

`kaye-engine claude` exposes one subcommand per Claude export target:

```bash
kaye-engine claude skill                # export blueprints as Skill folders or .zip packages
kaye-engine claude plugin               # export blueprints as a plugin folder or .zip package
kaye-engine claude marketplace          # export a marketplace folder for the Claude sidebar
kaye-engine claude code                 # export a plugin plus CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt   # export a blueprint as ~/.claude/CLAUDE.md
kaye-engine claude vs-code-extension    # export CLAUDE.md, marketplace, and settings.json
                                        # into ~/.claude for the Claude Code VS Code Extension
```

> [!TIP]
> Run `kaye-engine claude [SUBCOMMAND] -h` to see full documentation.





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
`~/.claude/kaye_marketplace/` folder containing the kaye plugin, and
configures git command permissions in `~/.claude/settings.json`.
<!-- FIXME gap review: understates scope — permission_cmds.jsonc also
     covers sudo/kill/systemctl, package managers, and pytest, not just git -->

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/kaye_marketplace/` and click *Install*.













## Corpus Requirements

A corpus must supply a node at `Agent Behavior` → `Claude Behavior`, and register a Chat blueprint and a Coder blueprint under whatever names the host passes to `set_claude_using_blueprint(chat_bp_name, coder_bp_name)`; `user_prompt/export.py` resolves them via `get_claude_chat_blueprint()`/`get_claude_coder_blueprint()` in `blueprint_name.py`.

`{for claude code}` sidecar nodes are optional; when present, `CONTAINING_SIDECARS` auto-includes them in every Claude export.

Q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md).

----

`kaye-engine claude plugin`, `claude marketplace`, `claude code`, and `claude vs-code-extension` all name the exported plugin/marketplace folder after the value read back by `get_plugin_marketplace_name()`. A host project must call `set_claude_plugin_marketplace_name(name)` (exposed at the top level, e.g. `kaye_engine.set_claude_plugin_marketplace_name("kaye-vault")`) before invoking the CLI, or `get_plugin_marketplace_name()` logs `logger.critical` and raises `SystemExit(1)`.

`claude user-system-prompt`, `claude code`, and `claude vs-code-extension` likewise resolve the Chat and Coder blueprints by name. A host project must call `set_claude_using_blueprint(chat_bp_name, coder_bp_name)` (exposed at the top level, e.g. `kaye_engine.set_claude_using_blueprint("chat", "coder")`) before invoking the CLI, or `get_claude_chat_blueprint()`/`get_claude_coder_blueprint()` log `logger.critical` and raise `SystemExit(1)` — both when unset and when the configured name is not a registered blueprint.


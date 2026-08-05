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

`{for claude code}` sidecar nodes are optional; when present, `CONTAINING_SIDECARS` auto-includes them in every Claude export.

Q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md).

----

A `claude`-exporting consumer must call `setup_claude_cli(~~)` before invoking the. The version passed here is the consumer's own, stamped into every `plugin.json`, `marketplace.json`, and `SKILL.md` the CLI writes


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

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/kaye_marketplace/` and click *Install*.













## Corpus Requirements

A corpus must supply a node at `Agent Behavior` → `Claude Behavior`, and register blueprints under the keys `"chat"`, `"rapid"`, and `"coder"` — both hardcoded lookups in `user_prompt/export.py`.

`{for claude code}` and `{prerequisite}` sidecar nodes are optional; when present, `CONTAINING_SIDECARS` auto-includes them in every Claude export.

Q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md).

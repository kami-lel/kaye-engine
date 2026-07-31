# Using Kaye Engine with Claude

## Claude Desktop

Generate a plugin package using the Kaye Engine CLI:

```bash
kaye-engine claude plugin --zip  # or
kaye-engine a p -z
```

----

Upload the generated `.zip` file to [Claude Desktop](https://claude.ai) settings under *Plugins* to enable Kaye Engine integration.

## Claude Code VS Code Extension

Set up Kaye Engine for the Claude Code VS Code Extension with one command:

```bash
kaye-engine claude vs-code-extension  # or
kaye-engine a v
```

This writes the User System Prompt to `~/.claude/CLAUDE.md`, creates a
`~/.claude/kaye_marketplace/` folder containing the kaye plugin, and
configures git command permissions in `~/.claude/settings.json`.

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/kaye_marketplace/` and click *Install*.

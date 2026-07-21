# Using Kaye with Claude

## Claude Desktop

Generate a plugin package using the Kaye CLI:

```bash
kaye claude plugin --zip  # or
kaye a p -z
```

----

Upload the generated `.zip` file to [Claude Desktop](https://claude.ai) settings under *Plugins* to enable Kaye integration.

## Claude Code VS Code Extension

Set up Kaye for the Claude Code VS Code Extension with one command:

```bash
kaye claude vs-code-extension  # or
kaye a v
```

This writes the User System Prompt to `~/.claude/CLAUDE.md`, creates a
`~/.claude/kaye_marketplace/` folder containing the kaye plugin, and
configures git command permissions in `~/.claude/settings.json`.

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/kaye_marketplace/` and click *Install*.

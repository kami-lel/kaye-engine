# Kaye Engine support for Anthropic Claude

Kaye Engine's integration with Anthropic Claude: exporting corpus blueprints as Claude plugins, skills, and system prompts.













## available CLI commands

`kaye-engine claude` exposes one subcommand per Claude export target:

```bash
kaye-engine claude skill                # export exportables as Skill folders or .zip packages
kaye-engine claude plugin               # export exportables as a plugin folder or .zip package
kaye-engine claude marketplace          # export a marketplace folder for the Claude sidebar
kaye-engine claude code                 # export a plugin plus CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt   # print the User System Prompt
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

A corpus must register a Chat exportable and a merged Coder exportable under whatever names it passes to `setup_claude_cli(...)` as `chat_exportable_name`/`merged_coder_exportable_name`; `user_prompt/export.py` resolves them via `get_claude_chat_exportable()`/`get_claude_merged_coder_exportable()` in `exportable_name.py`.

The merged Coder exportable (`merged_coder_exportable_name`) is expected to carry the Chat exportable as a `dependencies=[...]` entry, so its render carries the Chat persona alongside the coder content; it is what builds the final `-c` prompt used by `usp -c`, `claude code`, and `claude vs-code-extension`. Both Chat and the merged Coder may also double as their own standalone exportable Skills (e.g. a consumer package may register the same exportable under `"chat"` and `"coder"` names of its own choosing).

----

A `claude`-exporting consumer must call `setup_claude_cli(~~)` before invoking the CLI. The version passed here is the consumer's own, stamped into every `plugin.json`, `marketplace.json`, and `SKILL.md` the CLI writes.













## Surfaces

A **surface** is a named target Kaye Engine renders for — `chat`, `code`, the VS Code extension, and so on. Different surfaces support different tools, so the same corpus should render differently for each: a Bash-capable surface gets the Bash usage sidecar, a surface without file access does not.

A consumer defines its surfaces as a `dict[str, RenderProfile]` and passes it to `setup_claude_cli(surface_profiles=...)`. Each `RenderProfile` bundles the `variants` (which registered affordance variants that surface supports) and `conditional_sidecars` (which named sidecars it checkmarks) for one surface:

```python
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

SURFACE_PROFILES = {
    "chat": RenderProfile(
        variants=("ClaudeChat:ask_user_input_v0", ...),
        conditional_sidecars=("[ClaudeChat]", "[Claude]"),
    ),
    "code": RenderProfile(
        variants=("ClaudeCode:AskUserQuestion", ...),
        conditional_sidecars=("[ClaudeCode]", "[Claude]"),
    ),
}

setup_claude_cli(..., surface_profiles=SURFACE_PROFILES)
```

Every rendering command (`blueprint generate`, `claude skill`, `claude plugin`, `claude user-system-prompt`, ...) then accepts `--surface NAME` (`-u`), combinable, to render for one or more of those surfaces at once — `--surface chat --surface code` merges both profiles via `RenderProfile.merge()`. `--surface` is left out of the CLI entirely for a consumer that never configures `surface_profiles`.

`--variant` (q.v. [`affordance-doc.md`](affordance-doc.md)) and `--conditional-sidecar` (q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md)) union additively on top of whatever `--surface` derives, so a render can name extra variants or sidecars beyond a surface's defaults without losing them. Full flag table and merge semantics: `AGENTS.md` and `CONTEXT.md`.

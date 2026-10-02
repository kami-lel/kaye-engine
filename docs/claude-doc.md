# Kaye Engine: support for Anthropic Claude

<!-- FIXME mpv support for anthropic claude -->

Kaye Engine's integration with Anthropic Claude: exporting corpus blueprints as Claude plugins and system prompts and exporting every exportable as Agent Skills into Claude's skills folder (`claude skills`); exporting chosen Agent Skills into any folder is the top-level `kaye-engine skill` command.

> [!NOTE]
> All (non-internal) exportables in `exportable_registry` will be rendered

## available CLI commands

`kaye-engine claude` (alias `a`) exposes one subcommand per Claude export target. Every subcommand needs a consumer project to call `setup_claude_cli(...)` first (q.v. [Consumer Requirement](#consumer-requirement)); without it the command logs an error instead of writing files.

> [!TIP]
> Run `kaye-engine claude [SUBCOMMAND] -h` any time to see the live flags.

> [!NOTE]
> `claude skills` (plural) exports ALL skills and assumes a folder. To export chosen skills into a folder you name, use the top-level `kaye-engine skill NAME... FOLDER` (or `--all`), which is not Claude-specific.

### Choose a Subcommand

| Goal | Command | Alias |
| --- | --- | --- |
| Upload a plugin to Claude Desktop | `claude plugin -z` | `claude p` |
| Get a plugin folder to load locally | `claude plugin` | `claude p` |
| Export every skill into `~/.claude/skills` | `claude skills` | `claude s` |
| Get an installable marketplace folder | `claude marketplace` | `claude m` |
| Set up Claude Code in the terminal | `claude code` | `claude c` |
| Set up the Claude Code VS Code Extension | `claude vs-code-extension` | `claude v` |
| Print the User System Prompt | `claude user-system-prompt` | `claude usp` |

### plugin

Writes one plugin, with one `SKILL.md` per exportable.

```bash
kaye-engine claude plugin              # ~/.claude/plugins/PLUGIN_NAME/
kaye-engine claude plugin FOLDER       # FOLDER/PLUGIN_NAME/
kaye-engine claude plugin -z           # upload-ready .zip in the current directory
kaye-engine claude plugin -z -N ZIPS   # ZIPS/, filename without the version
```

```text
FOLDER/                      (default: ~/.claude/plugins/)
└── PLUGIN_NAME/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        └── <canonical_name>/
            └── SKILL.md
```

- `-z`, `--zip`: create an upload-ready `.zip` for Claude Desktop instead of a folder; FOLDER then defaults to the current directory
- `-N`, `--no-version`: leave the version out of the `.zip` filename, `.zip` only

#### Claude Desktop

Generate the package with `kaye-engine claude plugin --zip`, then upload the `.zip` to [Claude Desktop](https://claude.ai) settings under *Plugins* to enable Kaye Engine integration.

### skills

Writes one `SKILL.md` per exportable as its own skill folder, ready for Claude to read.

```bash
kaye-engine claude skills              # ~/.claude/skills/
kaye-engine claude skills FOLDER       # FOLDER/
kaye-engine claude skills -z           # one .zip per skill in the current directory
kaye-engine claude skills -z ZIPS      # ZIPS/
```

```text
FOLDER/                      (default: ~/.claude/skills/)
└── <canonical_name>/
    └── SKILL.md
```

- `-z`, `--zip`: create a `.zip` per skill instead of folders; FOLDER then defaults to the current directory

For a chosen subset, or a folder that is not Claude's, use `kaye-engine skill NAME... FOLDER` instead; FOLDER is required there.

### marketplace

Wraps the plugin in a marketplace that Claude can add as a source.

```bash
kaye-engine claude marketplace         # ~/.claude/<marketplace folder name>/
kaye-engine claude marketplace FOLDER
```

```text
MARKETPLACE/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── PLUGIN_NAME/          (same layout as plugin)
```

Add the resulting folder in Claude's marketplace settings.

### code

Sets up Claude Code in one step: writes `CLAUDE.md` as the User System Prompt (the Chat blueprint plus the Coder blueprint), and exports the plugin into `plugins/`.

```bash
kaye-engine claude code                # into ~/.claude
kaye-engine claude code CLAUDE_FOLDER  # into another .claude/ folder
```

```text
CLAUDE_FOLDER/               (default: ~/.claude)
├── CLAUDE.md
└── plugins/
    └── PLUGIN_NAME/
```

### vs-code-extension

Does what `code` does for the Claude Code VS Code Extension, but wraps the plugin in a marketplace and also updates `settings.json`.

```bash
kaye-engine claude vs-code-extension
kaye-engine claude vs-code-extension CLAUDE_FOLDER
```

```text
CLAUDE_FOLDER/               (default: ~/.claude)
├── CLAUDE.md                (User System Prompt)
├── settings.json            (updated)
└── <marketplace folder name>/
    ├── .claude-plugin/
    │   └── marketplace.json
    └── plugins/
        └── PLUGIN_NAME/
```

The marketplace folder name is set via `setup_claude_cli(~~)`. `settings.json` gains Bash command permissions covering git, system commands (`sudo`, `kill`, `systemctl`), package managers, `pytest`, and `docker`.

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/<marketplace folder name>/` and click *Install*.

> [!WARNING]
> `settings.json` is edited in place. Its Bash command permissions are updated, so check the result if you keep your own rules there.

### user-system-prompt

Prints the Chat blueprint to stdout; nothing is written to disk unless you redirect it.

```bash
kaye-engine claude usp > ~/.claude/CLAUDE.md
kaye-engine claude usp -c > ~/.claude/CLAUDE.md   # also append the Coder blueprint
```

Here `-c` means `--coder`, unlike the other subcommands, where `-c` means `--comment`. This command spells out `--comment`/`--no-comment` instead.

### Shared Render Flags

Every subcommand except `user-system-prompt` writes files, and all of them take the same render flags. Q.v. [`render-profile-doc.md`](render-profile-doc.md) for the full meaning.

- `-s`, `--sparseness`: blank-line policy for the rendered prompt
- `-c`/`-C`, `--comment`/`--no-comment`: show or omit comment nodes
- `--variant`: variant names to include
- `-i`, `--conditional-sidecar`: conditional-sidecar names to include
- `--reverse-order`: reverse sibling order at every level
- `--surface`, `-u`: present only when the consumer configured surfaces; each subcommand preselects its own surface when omitted
- `-n`, `--dry-run`: report every file, directory, and archive step with the `dry` badge and write nothing
- `-v`, `-q`, `-V`, `-Q`: verbosity

## Consumer Requirement

A corpus must register a Chat exportable and a merged Coder exportable under whatever names it passes to `setup_claude_cli(...)` as `chat_exportable_name`/`merged_coder_exportable_name`; `user_prompt/export.py` resolves them via `get_claude_chat_exportable()`/`get_claude_merged_coder_exportable()` in `exportable_name.py`.

The merged Coder exportable (`merged_coder_exportable_name`) is expected to carry the Chat exportable as a `dependencies=[...]` entry, so its render carries the Chat persona alongside the coder content; it is what builds the final `-c` prompt used by `usp -c`, `claude code`, and `claude vs-code-extension`. Both Chat and the merged Coder may also double as their own standalone exportable Skills (e.g. a consumer package may register the same exportable under `"chat"` and `"coder"` names of its own choosing).

----

A `claude`-exporting consumer must call `setup_claude_cli(~~)` before invoking the CLI. It supplies the plugin name, the marketplace folder name, the Chat and merged Coder exportable names, and the version, which is the consumer's own and is stamped into every `plugin.json`, `marketplace.json`, and `SKILL.md` the CLI writes.

## Surfaces

A **surface** is a named target Kaye Engine renders for — `chat`, `code`, the VS Code extension, and so on. Different surfaces support different tools, so the same corpus should render differently for each: a Bash-capable surface gets the Bash usage sidecar, a surface without file access does not.

A consumer defines its surfaces as a `dict[str, RenderProfile]` and passes it to `setup_claude_cli(surface_profiles=...)`; every rendering command then accepts `--surface NAME` (`-u`) to render for one or more of them. How surfaces are configured, selected, and merged with `--variant` and `--conditional-sidecar` is documented in [`render-profile-doc.md`](render-profile-doc.md#surfaces).

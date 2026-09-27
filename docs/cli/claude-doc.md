# Guide: The claude Command

This guide walks through the `kaye-engine claude` subcommands (alias `a`): what each one writes, where, and which one to pick. For the flat reference, q.v. [`claude-doc.md`](../claude-doc.md).

> [!NOTE]
> Exporting Agent Skills is no longer a `claude` subcommand. It moved up to the top-level `kaye-engine skill` command (alias `s`).

## Before You Start

Every `claude` subcommand needs a consumer project to call `setup_claude_cli(...)` first. It supplies the plugin name, the marketplace folder name, the version stamped into every generated file, and the Chat and merged Coder exportable names. Without it the command logs an error instead of writing files.

Run `kaye-engine claude SUBCOMMAND -h` any time to see the live flags.

## Choose a Subcommand

| Goal | Command | Alias |
| --- | --- | --- |
| Upload a plugin to Claude Desktop | `claude plugin -z` | `claude p` |
| Get a plugin folder to load locally | `claude plugin` | `claude p` |
| Get an installable marketplace folder | `claude marketplace` | `claude m` |
| Set up Claude Code in the terminal | `claude code` | `claude c` |
| Set up the Claude Code VS Code Extension | `claude vs-code-extension` | `claude v` |
| Print the User System Prompt | `claude user-system-prompt` | `claude usp` |

## plugin

Writes one plugin, with one `SKILL.md` per exportable.

```bash
kaye-engine claude plugin              # ~/.claude/plugins/PLUGIN_NAME/
kaye-engine claude plugin FOLDER       # FOLDER/PLUGIN_NAME/
kaye-engine claude plugin -z           # upload-ready .zip in the current directory
kaye-engine claude plugin -z -n ZIPS   # ZIPS/, filename without the version
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
- `-n`, `--no-version`: leave the version out of the `.zip` filename, `.zip` only

Upload the `.zip` in Claude Desktop under *Plugins*.

## marketplace

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

## code

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

## vs-code-extension

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

Then, in VS Code, open the *Claude* sidebar, go to *Settings* → *Marketplaces*, add the marketplace folder's path and click *Install*.

> [!WARNING]
> `settings.json` is edited in place. Its Bash command permissions are updated, so check the result if you keep your own rules there.

## user-system-prompt

Prints the Chat blueprint to stdout; nothing is written to disk unless you redirect it.

```bash
kaye-engine claude usp > ~/.claude/CLAUDE.md
kaye-engine claude usp -c > ~/.claude/CLAUDE.md   # also append the Coder blueprint
```

Here `-c` means `--coder`, unlike the other subcommands, where `-c` means `--comment`. This command spells out `--comment`/`--no-comment` instead.

## Shared Render Flags

Every subcommand except `user-system-prompt` writes files, and all of them take the same render flags. Q.v. [`render-profile-doc.md`](../render-profile-doc.md) for the full meaning.

- `-s`, `--sparseness`: blank-line policy for the rendered prompt
- `-c`/`-C`, `--comment`/`--no-comment`: show or omit comment nodes
- `--variant`: variant names to include
- `-i`, `--conditional-sidecar`: conditional-sidecar names to include
- `--reverse-order`: reverse sibling order at every level
- `--surface`, `-u`: present only when the consumer configured surfaces; each subcommand preselects its own surface when omitted
- `-v`, `-q`, `-V`, `-Q`: verbosity

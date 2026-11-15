# Kaye Engine: Support for Anthropic Claude

Export your corpus to Claude as plugins, Agent Skills, or a system prompt with `kaye-engine claude` (alias `a`). Every non-internal exportable is rendered.

## Choose a Subcommand

| Goal | Command | Alias |
| --- | --- | --- |
| Upload a plugin to Claude Desktop | `claude plugin -z` | `claude p` |
| Get a plugin folder to load locally | `claude plugin` | `claude p` |
| Export every skill into `~/.claude/skills` | `claude skills` | `claude s` |
| Get an installable marketplace folder | `claude marketplace` | `claude m` |
| Set up Claude Code in the terminal | `claude code` | `claude c` |
| Set up the Claude Code VS Code Extension | `claude vs-code-extension` | `claude v` |
| Print the User System Prompt | `claude user-system-prompt` | `claude usp` |

> [!NOTE]
> To export chosen skills into a folder you name, use the top-level `kaye-engine skill NAME... FOLDER` (or `--all`) instead of `claude skills`.

### plugin

Writes one plugin per consumer, with one skill per exportable.

```bash
kaye-engine claude plugin              # ~/.claude/plugins/PLUGIN_NAME/
kaye-engine claude plugin FOLDER       # FOLDER/PLUGIN_NAME/
kaye-engine claude plugin -z           # one .zip per consumer
kaye-engine claude plugin -z . NAME    # only consumer NAME's zip
```

- `-z`, `--zip`: write upload-ready zips instead of folders
- `--no-version`: drop the version from the zip name, giving `NAME-claude.zip`

### skills

Writes every exportable as its own skill folder.

```bash
kaye-engine claude skills              # ~/.claude/skills/
kaye-engine claude skills FOLDER
kaye-engine claude skills -z           # one .zip per skill
```

### marketplace

Wraps every consumer's plugin in one marketplace named `kaye-engine`. Add the resulting folder in Claude's marketplace settings.

```bash
kaye-engine claude marketplace         # ~/.claude/kaye-engine/
kaye-engine claude marketplace FOLDER
```

### code

Sets up Claude Code: writes `CLAUDE.md` (the User System Prompt) and every consumer's plugin.

```bash
kaye-engine claude code                # into ~/.claude
kaye-engine claude code CLAUDE_FOLDER
```

### vs-code-extension

Does what `code` does for the VS Code extension, but wraps plugins in a marketplace, registers it, and enables its plugins; steps in [Use in the Claude Code VS Code Extension](https://github.com/kami-lel/kaye-library/blob/dev/docs/claude-usage-doc.md#use-in-the-claude-code-vs-code-extension).

```bash
kaye-engine claude vs-code-extension
kaye-engine claude vs-code-extension CLAUDE_FOLDER
```

### user-system-prompt

Prints the Chat prompt to stdout; nothing is written unless you redirect it.

```bash
kaye-engine claude usp > ~/.claude/CLAUDE.md
kaye-engine claude usp -c > ~/.claude/CLAUDE.md   # also append the Coder prompt
```

Here `-c` means `--coder`; the comment toggle is long-form only (`--comment`/`--no-comment`).

## Build GitHub Release Assets

`build-github-release` is a top-level command, not a `claude` subcommand. One run writes every release asset of the consumer project into `OUTPUT`, for a release workflow to attach to a GitHub Release. Run it from the consumer's console script, which registers the consumers, the repo name, and the repo version:

```bash
CONSUMER_CLI build-github-release dist
```

- `OUTPUT`: the one required argument, the destination folder; there is no `-o` and no consumer argument
- one Claude Desktop plugin `.zip` per plugin consumer of the process, built as `claude plugin -z` builds it
- the VS Code installer for Windows (`.zip`) and for Linux (`.run`): one click puts the current `CLAUDE.md` and every plugin into `~/.claude/`, registers the marketplace, and enables the plugins, with no Kaye Engine on the user's machine; the steps are in [Installer Algorithm](installer-algorithm-doc.md#claude-vs-code-plugin). Windows: extract the zip, double-click `Install.cmd`. Linux: `bash NAME.run`. Both take no option. To remove: delete the `kaye-engine/` folder and its keys in `settings.json`
- the installers always render for the `claude-vsc` surface; `--surface` applies to the zips only
- `--dry-run` lists every asset and writes nothing
- it takes the [render flags](#render-flags) below

Every file is named `REPO-VERSION-TYPE[-CONSUMER|-OS].ext`:

| part | value |
| --- | --- |
| `REPO`, `VERSION` | the repo name and version the consumer project registered with `set_repo_name` and `set_repo_version` |
| `TYPE` | `claude-desktop-plugin` or `claude-vsc-installer` |
| `-CONSUMER` | a plugin zip only; left out for the default consumer (`set_default_consumer`), so the name never repeats the repo name |
| `-OS` | an installer only: `Win` (`.zip`) or `linux` (`.run`) |

An unset repo name, repo version, or default consumer exits 1 before anything is written. `claude plugin` takes an optional `CONSUMER` after `FOLDER`; absent means the default consumer, and an unknown name exits 1 listing the valid ones (`claude plugin -z . NAME` still works).

## Render Flags

Every subcommand takes the same render flags, explained in [render-profile-doc.md](render-profile-doc.md); `user-system-prompt` lacks only `-n`, since it writes nothing:

- `-s`, `--sparseness`: blank-line policy
- `--comment`/`--no-comment`: show or omit the generated-by comment
- `--variant`, `-i`/`--conditional-sidecar`: extra variants and sidecars to include
- `--reverse-order`: reverse sibling order
- `-u`, `--surface`: render profile to target, see [Surfaces](#surfaces)
- `-n`, `--dry-run`: report every write, write nothing
- `-v`, `-q`, `-V`, `-Q`: verbosity

## Surfaces

A **surface** is a target Kaye Engine renders for, since different apps offer different tools. Claude has 2: `claude` for the chat apps and Claude Code in the terminal, and `claude-vsc` for the VS Code extension. Each subcommand picks its own surface unless you pass `--surface`; see [render-profile-doc.md](render-profile-doc.md#surfaces).

## Setup for Consumer Packages

Every command needs the consumer package to register itself first; without it, the command logs a critical error and exits 1.

- Consumer: call `register_consumer(display_name, canonical_name, version)` once. The canonical name is the plugin name and must equal the installed distribution name
- Console command: call `set_entry_consumer(canonical_name)` and `setup_claude_cli(...)` during setup
- Release and `claude plugin`: call `set_repo_name(name)`, `set_repo_version(version)`, and `set_default_consumer(canonical_name)`; `build-github-release` and a bare `claude plugin` exit 1 without them
- Chat and Coder: `code`, `vs-code-extension`, and `user-system-prompt` also need the Chat and merged Coder exportable names passed to `setup_claude_cli(...)`; the merged Coder should list Chat as a dependency

## Editing the Corpus

1. Edit a corpus Markdown file in the consumer package.
2. Run `kaye-engine blueprint validate`.
3. Export again with the `claude` subcommand you use.

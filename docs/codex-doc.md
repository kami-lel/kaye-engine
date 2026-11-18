# Kaye Engine: Support for OpenAI Codex

Export your corpus to Codex as plugins, a marketplace, Agent Skills, or a global prompt with `kaye-engine codex` (alias `o`). Every non-internal exportable is rendered for the `codex` [surface](#surface).

## Choose a Subcommand

| Goal | Command | Alias |
| --- | --- | --- |
| Get a plugin folder per consumer | `codex plugin` | `codex p` |
| Get a marketplace Codex can add | `codex marketplace` | `codex m` |
| Export every skill into `~/.agents/skills` | `codex skills` | `codex s` |
| Print the global prompt for `~/.codex/AGENTS.md` | `codex user-system-prompt` | `codex usp` |

> [!NOTE]
> Codex installs plugins only from a marketplace, never from a zip; to publish one by URL, see [Marketplace Repo](#marketplace-repo).

### plugin

Writes one plugin per consumer, with one skill per exportable.

```bash
kaye-engine codex plugin               # ~/plugins/PLUGIN_NAME/
kaye-engine codex plugin FOLDER        # FOLDER/PLUGIN_NAME/
kaye-engine codex plugin . NAME        # only consumer NAME's plugin
```

Each plugin carries 2 manifests:

- `plugin.json`: the portable Agent Plugins manifest (`$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `keywords`)
- `.codex-plugin/plugin.json`: the same fields plus `skills` and the OpenAI `interface` (`displayName`, `shortDescription`, `developerName`, `category`)

`CONSUMER` follows `FOLDER`; absent means the default consumer, and an unknown name exits 1 listing the valid ones.

### marketplace

Writes `.agents/plugins/marketplace.json` at `ROOT` and every consumer's plugin into `ROOT/plugins/`. The default `ROOT`, your home folder, is the personal marketplace Codex reads; any other folder can be added by hand.

```bash
kaye-engine codex marketplace          # ~/.agents/plugins/marketplace.json, ~/plugins/
kaye-engine codex marketplace ROOT
codex plugin marketplace add ROOT      # then, for a ROOT outside ~
```

The marketplace is named after the repo (`set_repo_name`); each entry is a local plugin, `AVAILABLE` to install, category `Productivity`.

### skills

Writes every exportable as its own skill folder, no plugin.

```bash
kaye-engine codex skills               # ~/.agents/skills/
kaye-engine codex skills FOLDER
```

### user-system-prompt

Prints the Chat prompt to stdout; nothing is written unless you redirect it.

```bash
kaye-engine codex usp > ~/.codex/AGENTS.md
kaye-engine codex usp -c > ~/.codex/AGENTS.md   # also append the Coder prompt
```

Here `-c` means `--coder`; the comment toggle is long-form only (`--comment`/`--no-comment`).

## Marketplace Repo

`build-github-marketplace` is a top-level command, not a `codex` subcommand. One run writes a marketplace repo root that both Claude and Codex add by URL, for a release workflow to push to a public repo. Run it from the consumer's console script:

```bash
CONSUMER_CLI build-github-marketplace market
```

```text
market/
├── .claude-plugin/marketplace.json     # Claude
├── .agents/plugins/marketplace.json    # Codex
└── plugins/
    ├── claude/PLUGIN_NAME/             # rendered for surface claude
    └── codex/PLUGIN_NAME/              # rendered for surface codex
```

- `OUTPUT`: the one required argument; there is no consumer argument
- the marketplace is named `REPO-marketplace` from `set_repo_name`, so it never clashes with the local marketplace, named `REPO`; the default consumer's metadata describes and owns it
- only `.claude-plugin/`, `.agents/` and `plugins/` are written; a `README.md` or any other root file is left alone
- `--surface` is refused, since each half renders its own surface; the other render flags apply to both
- `--dry-run` lists every write and writes nothing

Once pushed, users add it by URL:

```bash
codex plugin marketplace add OWNER/REPO-marketplace
```

```text
/plugin marketplace add OWNER/REPO-marketplace
/plugin install PLUGIN_NAME@REPO-marketplace
```

## Render Flags

Every subcommand takes the same render flags, explained in [render-profile-doc.md](render-profile-doc.md); `user-system-prompt` lacks only `-n`, since it writes nothing:

- `-s`, `--sparseness`: blank-line policy
- `--comment`/`--no-comment`: show or omit the generated-by comment
- `--variant`, `-i`/`--conditional-sidecar`: extra variants and sidecars to include
- `--reverse-order`: reverse sibling order
- `-u`, `--surface`: render profile to target, default `codex`
- `-n`, `--dry-run`: report every write, write nothing
- `-v`, `-q`, `-V`, `-Q`: verbosity

## Surface

The `codex` surface carries the Codex tool variants (`Codex:shell`, `Codex:apply_patch`, `Codex:update_plan`, `Codex:request_user_input`, `Codex:web_search`, `Codex:view_image`), `git`, and the image model, plus the `[for Codex]` identity sidecar. It carries no Claude variant, so content written for a Claude-only tool renders its Fallback; see [render-profile-doc.md](render-profile-doc.md#surfaces).

## Setup for Consumer Packages

Every command needs the consumer package to register itself first; without it, the command logs a critical error and exits 1.

- Consumer: call `register_consumer(display_name, canonical_name, version)` once; the canonical name is the plugin name and must equal the installed distribution name
- Console command: call `set_entry_consumer(canonical_name)` and `setup_codex_cli(chat, merged_coder)` during setup; only `user-system-prompt` needs the 2 names
- `codex plugin` and `build-github-marketplace`: call `set_default_consumer(canonical_name)`; the marketplace repo also needs `set_repo_name(name)`

## Design

Codex and Claude plugins come from one exporter. `PluginPlatform` (`kaye_engine/cli/plugin_platform/platform.py`) is a Strategy holding what differs per platform: manifest files, marketplace file and entry shape, default surface. The template exporters in `kaye_engine/cli/plugin_platform/export.py` run the shared steps and call those hooks; `ClaudePlatform` and `CodexPlatform` are the 2 platforms, and `build-github-marketplace` runs both into one root.

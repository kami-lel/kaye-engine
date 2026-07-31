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
> Run `kaye-engine claude <subcommand> -h` to see full documentation.

Once exported, upload a plugin `.zip` to [Claude Desktop](https://claude.ai)
settings under *Plugins*, or, for the VS Code Extension, open the *Claude*
sidebar → *Settings* → *Marketplaces* and add the path to
`~/.claude/kaye_marketplace/`.













## Corpus Contract

`kaye_engine/cli/claude/` is generic over `blueprint_registry`, but three
things it hardcodes mean a corpus (whether `kaye-vault`'s or a second
vault-like project's) must be shaped a specific way for Claude exports to
work:

- **Required node path.** The loaded corpus tree must contain a node at
  `Agent Behavior` → `Claude Behavior`. `user_prompt/export.py` indexes this
  path unconditionally regardless of which base blueprint is chosen —
  missing it breaks `claude user-system-prompt`, `claude code`, and `claude
  vs-code-extension`.
- **Required blueprint registry keys.** A `blueprint_registrations.py`-style
  module, imported for its side effect before the CLI dispatches, must
  register exactly the keys `"chat"`, `"rapid"`, and `"coder"` via
  `blueprint_registry` — hardcoded literals in `user_prompt/export.py`.
  Any entry meant to become a Skill additionally needs
  `skill_exportable=True` and a `display_name` that survives
  `to_skill_name()`'s kebab-case conversion into Anthropic's skill-name
  grammar.
- **Package metadata is not overridable.** `plugin/export_folder.py` and
  `marketplace/export.py` read `importlib.metadata.metadata(PROGRAM_NAME)`,
  where `PROGRAM_NAME` is `kaye_engine.PROGRAM_NAME`, hardcoded to
  `"kaye-engine"` inside the engine itself. Every exported plugin
  folder/manifest carries the engine's own installed-package identity
  (name, author, homepage) — a second vault-like project cannot rebrand
  this without an engine change.

Loading order matters for the first two points: the corpus must be loaded
via `load_corpus_tree(tree_name, file_path, is_default_tree=True)` as a side
effect of the project's own `<pkg>/__init__.py` (not a lazily-called
function), and the blueprint registrations module must be imported before
`cli_parser.parse_args()` runs — the same pattern `kaye_vault/__init__.py`
and `kaye_vault/blueprint_registrations.py` follow.

## Sidecar Nodes

Two sidecar node names are recognized by Claude exports specifically; see
[`sidecar-node-doc.md`](sidecar-node-doc.md) for the full sidecar node
mechanism.

- **`{for claude code}`** — Claude-specific instructions spliced into the
  rendered prompt whenever their parent node is checkmarked and rendering
  passes `contains_sidecars=("for claude code",)`.
- **`{prerequisite}`** — prerequisite instructions auto-included alongside
  an already-checkmarked parent node, not specific to Claude but combined
  with the entry above for every Claude export.

`kaye_engine.cli.claude.CONTAINING_SIDECARS = ("for claude code",
"prerequisite")` combines both names and is passed to `generate_prompt()`
for every Claude skill, plugin, marketplace, and user-system-prompt export.
Unlike the required node path and registry keys above, this vocabulary is
optional — a corpus without `{for claude code}` or `{prerequisite}` nodes
still exports correctly, just without any conditional content spliced in.

----
name: kaye-engine AGENTS.md
alwaysApply: true
----

# kaye-engine AGENTS

Guidance for AI coding agents working in the **kaye-engine** repository.
Read this file alongside `CONTEXT.md` before making changes, and follow the
exact commands and conventions below.

**kaye-engine ships mechanism only.** It bundles no prompt corpus, no
abbreviation database, and no blueprint registrations — a host package such
as `kaye-vault` supplies all three. Never add that content here to make
something work; fix the mechanism or fix the host.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

`claude` exports read installed distribution metadata — run against an
installed package, not a bare checkout.

## Testing

**Always run tests selectively** — scope each run to the files that mirror
the changed source. Run the full suite only when asked, or right before a
merge.

| changed source | test scope |
|---|---|
| `kaye_engine/prompt/` | `tests/prompt/` |
| `kaye_engine/abbr_collection/` | `tests/abbr/` |
| `kaye_engine/cli/` | `tests/cli/` |
| `dify_studio/` | `tests/dify/` |

```bash
pytest tests/prompt/
pytest tests/prompt/bp/
pytest tests/prompt/bp/prompt-bp-merge_test.py
pytest tests/prompt/bp/prompt-bp-merge_test.py::TestMerge::test1_1
```

`tests/cli/` covers only what runs without a corpus — version resolution and
`SKILL.md` rendering. The exporters themselves need a corpus to produce
output, so the host package's suite covers those; do not scaffold corpus
fixtures here to widen the directory.

**Do not parallelize** — no `pytest-xdist`, no `-n auto`. The suite is
already fast, worker startup cancels out any gain, and splitting across
workers breaks tests that depend on run order.

Full suite — **only for merge or when explicitly asked**:

```bash
pytest
```

## CLI

The editable install registers a `kaye-engine` console script, so
`kaye-engine ...` and `python -m kaye_engine ...` are equivalent — prefer
the shorter form. **Two** subcommands exist, `prompt` and `claude`:

```bash
kaye-engine --help                          # show CLI usage
kaye-engine prompt ls                       # list registered blueprint names
kaye-engine prompt show BLUEPRINT           # preview a blueprint's structure
kaye-engine prompt generate BLUEPRINT       # render a concrete prompt
kaye-engine claude skill SKILLS_FOLDER      # export blueprints as Skill folders
kaye-engine claude skill -z ZIPS_FOLDER     # create .zip Skill packages
kaye-engine claude plugin PLUGINS_FOLDER    # export blueprints as plugin folder
kaye-engine claude plugin -z PLUGINS_FOLDER # .zip package (-n drops version)
kaye-engine claude marketplace              # to ~/.claude/kaye_marketplace
kaye-engine claude marketplace MARKETPLACE  # to a custom folder
kaye-engine claude code                     # plugin + CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt       # Chat blueprint as CLAUDE.md
kaye-engine claude user-system-prompt -r    # use Rapid blueprint instead
kaye-engine claude user-system-prompt -c    # append Kaye Peer Coder content
kaye-engine claude vs-code-extension        # CLAUDE.md + marketplace + settings
```

Aliases: `prompt` → `p`; `prompt generate` → `p g`; `claude` →
`anthropic`, `a`; `claude code` → `claude c`; `claude marketplace` →
`claude m`; `claude plugin` → `claude p`; `claude skill` → `claude s`;
`claude user-system-prompt` → `claude usp`; `claude vs-code-extension` →
`claude v`.

`claude vs-code-extension` also writes `permissions` (`allow`/`ask`/`deny`
Bash command patterns) into `settings.json`, sourced from
`kaye_engine/cli/claude/permission_cmds.jsonc` (parsed with `json5`, so
comments are allowed).

`kaye_engine/cli/cli_continue/` is **deprecated and unreachable** —
`cli_main.py` never registers it, so no `continue` subcommand exists. Do not
document it, invoke it, or wire it back in without being asked.

`claude user-system-prompt`, `claude code`, and `claude vs-code-extension`
look up blueprints `"chat"`/`"rapid"`/`"coder"`, so they need a host corpus.
On a bare checkout each subcommand logs a setup-guard warning (no default
corpus tree, empty `blueprint_registry`), then exits `1` on the missing
`"chat"`/`"rapid"` lookup — expected, not a bug.

A `claude`-exporting host must call `set_claude_plugin_marketplace_name(name)`
before invoking the CLI, or `get_plugin_marketplace_name()` logs
`logger.critical` and raises `SystemExit(1)`.

## Code Conventions

- follow **PEP 8**; keep lines within **80 characters**
- use **Sphinx**-style docstrings written in **reStructuredText**
- public methods must have docstrings; private methods (`_` prefix) only
  when the name is not self-explanatory
- test files end with `_test.py` and mirror the source tree under `tests/`
- test classes are grouped as `TestStructure`, `TestHeader`, `TestContent`
- use comment section headings (`#`, `=`, `*`, `+`, `-`) only for long files

## Registering a Blueprint

`register_blueprint()` in `kaye_engine/prompt/blueprint/registry.py` is the
only gate — every exporter reads `blueprint_registry` directly. **Calls
live in the host package**, not here.

Export policy — five independent flags, no allow-list constant:

| flag | default | effect |
|---|---|---|
| `skill_exportable` | `False` | export as a Claude Agent Skill |
| `continue_exportable` | `False` | export as a Continue AI rule |
| `always_apply` | `False` | apply unconditionally, skipping relevance |
| `user_invokable` | `True` | a human may invoke it by name |
| `llm_invokable` | `True` | the assistant may surface it unprompted |

## Abbreviation Data

`get_exportable_abbrs()` rebuilds every group on each call, so there is no
import-order constraint — populate the abbreviation database at any point
before an export actually runs. An unpopulated database still exports, as
one empty skill folder per group.

## Security

- do not commit secrets, credentials, or tokens
- `.git`, `venv/`, build artifacts, and generated prompts are git-ignored;
  keep them out of commits
- clear a stale `build/` before packaging — setuptools does not, and its
  leftovers are copied into the wheel

## Documentation Maintenance

After meaningful changes, keep these in sync:

- `README.md` — human-facing overview and quick start
- `docs/` — programmatic API, corpus format, sidecar and dynamic nodes,
  abbreviations, Claude and Dify integration
- `CONTEXT.md` — architecture, entities, boundaries
- `CHANGELOG.md` — record notable changes per release
- this `AGENTS.md` — update agent-specific rules as structure evolves

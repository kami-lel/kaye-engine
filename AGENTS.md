----
name: kaye-engine AGENTS.md
alwaysApply: true
----

# kaye-engine AGENTS

Guidance for AI coding agents working in the **kaye-engine** repository.
Read this file alongside `CONTEXT.md` before making changes, and follow the
exact commands and conventions below.

**kaye-engine ships mechanism only.** It bundles no prompt corpus, no
abbreviation database, and no blueprint registrations — a consumer package
such as `kaye-vault` supplies all three. Never add that content here to make
something work; fix the mechanism or fix the consumer.

**kaye-engine is consumed by multiple projects.** Never name any specific
consumer project anywhere in this repository's content (code, comments,
docs, or tests) — doing so would leak one consumer's identity into a
mechanism meant to stay consumer-agnostic.

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

```bash
pytest tests/prompt/
pytest tests/prompt/bp/
pytest tests/prompt/bp/prompt-bp-merge_test.py
pytest tests/prompt/bp/prompt-bp-merge_test.py::TestMerge::test1_1
```

`tests/cli/` covers only what runs without a corpus — the setup guard,
exportable-abbr registration, `dynamic-node` parsing, and `SKILL.md`
rendering. The exporters themselves need a corpus to produce output, so the
consumer package's suite covers those; do not scaffold corpus fixtures here
to widen the directory. The `blueprint` and `export` subcommand parsers
currently have no dedicated tests — a known gap, not an intentional
exclusion like the exporters above.

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
the shorter form. **Four** subcommands exist, `blueprint`, `claude`,
`dynamic-node`, and `export`:

```bash
kaye-engine --help                          # show CLI usage
kaye-engine blueprint ls                    # list registered blueprint names
kaye-engine blueprint show BLUEPRINT        # preview a blueprint's structure
kaye-engine blueprint show < FILE           # preview from stdin (BLUEPRINT omitted)
kaye-engine blueprint generate BLUEPRINT    # render a concrete prompt
kaye-engine blueprint generate < FILE       # render from stdin (BLUEPRINT omitted)
kaye-engine dynamic-node NODE...            # render 1+ dynamic nodes merged into one blueprint/output; NODE is "today"/"shorthand", any simple AbbrTags kebab slug (eg "emoji", "single-character"), or any known abbr glossary name
kaye-engine dynamic-node NODE -t THRESHOLD  # for a glossary NODE, hide entries with priority > THRESHOLD
kaye-engine dynamic-node NODE -s SPARSENESS # blank-line policy, v.i.
kaye-engine dynamic-node ls                 # list every available NODE value: today, shorthand, every AbbrTags-derived name, then glossary names alphabetically
kaye-engine claude skill SKILLS_FOLDER      # export blueprints as Skill folders
kaye-engine claude skill -z ZIPS_FOLDER     # create .zip Skill packages
kaye-engine claude plugin PLUGINS_FOLDER    # export blueprints as plugin folder
kaye-engine claude plugin -z PLUGINS_FOLDER # .zip package (-n drops version)
kaye-engine claude marketplace              # to ~/.claude/<marketplace folder>
kaye-engine claude marketplace MARKETPLACE  # to a custom folder
kaye-engine claude code                     # plugin + CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt       # print Chat blueprint to stdout
kaye-engine claude user-system-prompt -c    # append Coder blueprint content
kaye-engine claude user-system-prompt --no-show-comment # omit trailing comment
kaye-engine claude vs-code-extension        # CLAUDE.md + marketplace + settings
kaye-engine export EXPORTABLE               # print an exportable's content
kaye-engine export ls                       # list every registered exportable name
```

Aliases: `blueprint` → `bp`; `blueprint show` → `bp s`; `blueprint
generate` → `bp gen`/`bp g`; `dynamic-node` → `dn`; `claude` →
`anthropic`, `a`; `claude code` → `claude c`; `claude marketplace` →
`claude m`; `claude plugin` → `claude p`; `claude skill` → `claude s`;
`claude user-system-prompt` → `claude usp`; `claude vs-code-extension`
→ `claude v`; `export` → `x`.

`blueprint generate` and `dynamic-node` both take `-s`/`--sparseness SPARSENESS`
(shared parser in `kaye_engine/cli/sparseness_parser.py`) to control
blank-line collapsing in the rendered output: `-1` joins everything into one
line, `0` (default) strips all blank lines, `1` collapses every run to a
single blank line, up through `99` which disables trimming entirely. The
default lives in `DEFAULT_SPARSENESS` (`kaye_engine/cli/__init__.py`) and is
shared by `sparseness_parser`, `SKILL.md` export, `user-system-prompt`, and
`vs-code-extension` alike, unless a caller overrides it.

`claude vs-code-extension` also writes `permissions` (`allow`/`ask`/`deny`
Bash command patterns) into `settings.json`, sourced from
`kaye_engine/cli/claude/permission_cmds.jsonc` (parsed with `json5`, so
comments are allowed).

`kaye_engine/cli/cli_continue/` is **deprecated and unreachable** —
`cli_main.py` never registers it, so no `continue` subcommand exists. Do not
document it, invoke it, or wire it back in without being asked.

Every `claude` subcommand needs a consumer to call
`setup_claude_cli(plugin_name, display_name, marketplace_name, chat_bp_name,
coder_bp_name, version, marketplace_folder_name)` before invoking the CLI —
there is no default for any of the seven. `display_name` is stamped into
`plugin.json`'s `display_name` field by `claude plugin export`; it replaces
the former hardcoded `DISPLAY_NAME` constant in `kaye_engine/__init__.py`. On
a bare checkout, or when `setup_claude_cli(...)` was never called,
`get_plugin_name()`, `get_claude_cli_display_name()`,
`get_marketplace_name()`, `get_claude_chat_blueprint()`,
`get_claude_coder_blueprint()`, `get_claude_cli_consumer_version()`, and
`get_marketplace_folder_name()` each log `logger.critical` and raise
`SystemExit(1)`; the blueprint getters do the same when the configured name
is not a registered blueprint — expected, not a bug.

`kaye-engine --version` reports the installed distribution's version via
`importlib.metadata.version(PACKAGE_NAME)` — run against an installed
package, not a bare checkout.

Every `claude` export subcommand also takes `--surface SURFACE [SURFACE
...]` (shared parser in `kaye_engine/cli/claude/surface_parser.py`),
combinable member names of the `ClaudeSurface` enum.Flag (`chat`,
`cowork`, `code`, `vsc`) — the affordance names available on those
surfaces get checkmarked in the rendered output. Each subcommand defines
its own default surface set when the flag is omitted.

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
live in the consumer package**, not here.

Export policy — one gate plus three independent flags, no allow-list
constant:

| flag | default | effect |
|---|---|---|
| `is_exportable` | `True` | `False` excludes it from `exportable_registry` entirely — never export as a Claude Agent Skill |
| `always_apply` | `False` | apply unconditionally, skipping relevance |
| `user_invokable` | `True` | a human may invoke it by name |
| `llm_invokable` | `True` | the assistant may surface it unprompted |

## Abbreviation Data

`get_exportable_abbrs()` rebuilds every glossary on each call, so there is no
import-order constraint — populate the abbreviation database at any point
before an export actually runs. An unpopulated database logs an error and
returns an empty list, so no skill folders are exported. Check
`bool(get_abbr_data())` to test for an empty singleton directly.

Every glossary name an entry's `glossaries` array uses must be registered via
`register_abbr_glossary(name, ...)` before that entry loads, or `ValueError`
is raised — `tests/conftest.py` registers every glossary name the test suite
references, module-level, so it runs at collection time before any test
module builds `AbbrData`. Register a new glossary there when adding one.

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

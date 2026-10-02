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
| `kaye_engine/prompt/` | `tests/prompt/` (`tests/prompt/tree/` for the loader, `tests/prompt/index/` for `CorpusIndex`, `tests/prompt/bp/data/` for `Blueprint` and its functions) |
| `kaye_engine/prompt/blueprint/render/` | `tests/prompt/`, plus `tests/cli/export_image_prompt_parser_test.py` (asserts rendered negative-prompt text) |
| `kaye_engine/abbr_collection/` | `tests/abbr/` |
| `kaye_engine/cli/` | `tests/cli/` |
| `kaye_engine/cli/blueprint/` | `tests/cli/blueprint/` (drives the real parsers over a small inline corpus; `aux_input_test.py`, `aux_output_test.py` for the helpers) |
| `kaye_engine/cli/continue_ai/` | `tests/cli/continue_ai/` |
| `kaye_engine/cli/hermes/` | `tests/cli/hermes/` |
| `kaye_engine/cli/open_webui/` | `tests/cli/open_webui/` |
| `kaye_engine/cli/skill/` | `tests/cli/skill/` |
| `kaye_engine/cli/claude/skills/` | `tests/cli/cli_main_test.py`, `tests/cli/dry_run_test.py` |
| `kaye_engine/skill/` | `tests/skill/`, plus `tests/cli/open_webui/skill_form_test.py` (reads `Skill`) |
| `kaye_engine/exportable/` | `tests/exportable_test.py`, `tests/image_prompt_export_test.py` |

```bash
pytest tests/prompt/
pytest tests/prompt/bp/
pytest tests/prompt/bp/data/prompt-bp-edit_test.py
pytest tests/prompt/bp/data/prompt-bp-edit_test.py::TestCreateFromNode
```

`tests/cli/` covers only what runs without a vault-sized corpus — the setup guard,
exportable-abbr registration, `dynamic-node` parsing, and `SKILL.md`
rendering. The exporters themselves need a corpus to produce output, so the
consumer package's suite covers those; do not scaffold corpus fixtures here
to widen the directory. Known test gaps are tracked in `CONTEXT.md`.

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
the shorter form. **Fourteen** top-level subcommands exist: `blueprint`,
`claude`, `continue`, `hermes`, `export-image-prompt`, `dynamic-node`, `dynamic-substitution`,
`exportable`, `export-json`, `affordance`, `variant`,
`glossary`, `skill`, and `sync-open-webui-skills`:

```bash
kaye-engine --help                          # show CLI usage
kaye-engine blueprint list                  # list registered blueprint names; alias ls
kaye-engine blueprint preview BLUEPRINT     # preview a blueprint's structure, dependencies included
kaye-engine blueprint preview BLUEPRINT -D  # own nodes only; flags -l -w -t tune the tree
kaye-engine blueprint render BLUEPRINT      # render a concrete prompt, dependencies included
kaye-engine blueprint render BLUEPRINT -D   # own nodes only
kaye-engine blueprint validate BLUEPRINT    # exit 0 if sound, 1 with the reason if not
kaye-engine blueprint show BLUEPRINT        # summary of meta, node count, dependencies
kaye-engine blueprint show BLUEPRINT -d     # one field: -a display name, -d description, -D description node, -w when-to-use, -W when-to-use node, -n nodes, -t subtrees, -g globs, -p dependencies
kaye-engine blueprint preview < FILE        # any blueprint command reads stdin when BLUEPRINT is omitted
kaye-engine dynamic-node NODE...            # render 1+ dynamic nodes merged into one blueprint/output; NODE is "today"/"decode-only-abbr", any simple AbbrTags kebab slug (eg "emoji", "single-character"), or any known abbr glossary name
kaye-engine dynamic-node NODE -t THRESHOLD  # for a glossary NODE, hide entries with priority > THRESHOLD
kaye-engine dynamic-node ls                 # list every available NODE value: today, decode-only-abbr, every AbbrTags-derived name, then glossary names alphabetically
kaye-engine dynamic-substitution NAME       # print a registered dynamic substitution's content
kaye-engine dynamic-substitution ls         # list every registered dynamic substitution name
kaye-engine skill NAME... FOLDER            # export the named Agent Skills into FOLDER (required)
kaye-engine skill --all FOLDER              # export every Agent Skill; -a short
kaye-engine skill -z NAME... FOLDER         # create .zip Agent Skill packages
kaye-engine claude skills                   # export all skills into ~/.claude/skills
kaye-engine claude skills FOLDER            # to a custom folder
kaye-engine claude skills -z                # .zip per skill in the current directory
kaye-engine claude plugin PLUGINS_FOLDER    # export blueprints as plugin folder
kaye-engine claude plugin -z PLUGINS_FOLDER # .zip package (-N drops version)
kaye-engine claude marketplace              # to ~/.claude/<marketplace folder>
kaye-engine claude marketplace MARKETPLACE  # to a custom folder
kaye-engine claude code                     # plugin + CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt       # print Chat blueprint to stdout
kaye-engine claude user-system-prompt -c    # append Coder blueprint content
kaye-engine claude vs-code-extension        # CLAUDE.md + marketplace + settings
kaye-engine continue                        # export rules + prompts to ~/.continue
kaye-engine continue FOLDER                 # export to a custom Continue folder
kaye-engine hermes FOLDER                   # SOUL.md, profiles/, skills/ into a Hermes home
kaye-engine hermes FOLDER -n                # report every write without touching disk
kaye-engine export-image-prompt FOLDER          # write every image-prompt-subset exportable to FOLDER
kaye-engine exportable EXPORTABLE           # print an exportable's content
kaye-engine exportable ls                   # list every registered exportable name
kaye-engine export-json              # export exportable_registry as flat JSON
kaye-engine export-json -f FILE      # write to FILE instead of the default
kaye-engine affordance                 # list affordance_registry names, sorted
kaye-engine variant                    # list variant_registry canonical names, sorted
kaye-engine glossary GLOSSARY               # print a glossary's content
kaye-engine glossary ls                     # list every registered glossary name
OWU_API_KEY=sk-... kaye-engine sync-open-webui-skills  # push every exportable into Open WebUI as a skill
kaye-engine o -n                            # report create/update/skip without writing
kaye-engine o --prune --base-url URL        # also delete remote-only skills; custom server
```

Aliases: `blueprint` → `bp`; `blueprint list` → `bp ls`; `blueprint
preview` → `bp p`; `blueprint render` → `bp r`; `blueprint validate` →
`bp v`; `blueprint show` → `bp s`; `continue` → `c`; `hermes` → `m`; `export-image-prompt` → `img`; `dynamic-node` →
`dn`; `dynamic-substitution` → `ds`; `claude` → `a`; `claude code`
→ `claude c`; `claude
marketplace` → `claude m`; `claude plugin` → `claude p`; `claude skills` → `claude s`; `skill`
→ `s`; `claude user-system-prompt` → `claude usp`;
`claude vs-code-extension` → `claude v`; `exportable` → `x`;
`export-json` → `json`; `affordance` → `afd`; `variant`
→ `var`; `glossary` → `g`; `sync-open-webui-skills` → `o`.

**Rendering commands** — any subcommand that reaches
`render_prompt(...)`, directly or via
`Exportable.content()` (`blueprint render`, `dynamic-node`,
`exportable`, `skill`, `claude skills`, `claude plugin`,
`claude marketplace`,
`claude user-system-prompt`, `claude vs-code-extension`, `claude
code`) — all expose the same 6 options via one shared parent parser
and one aux function, `build_render_profile_parent_parser`/
`resolve_render_profile` (`kaye_engine/cli/render_profile_parser.py`),
the latter returning a `RenderProfile` rather than a kwargs dict:

| flag | short | effect |
|---|---|---|
| `--surface` | `-u` | Claude surface(s) to checkmark variants for; combinable |
| `--comment`/`--no-comment` | `-c`/`-C` | show/omit the trailing generated-by comment |
| `--conditional-sidecar` | `-i` | conditional-sidecar name(s), unioned with `--surface` |
| `--variant` | none | variant name(s), unioned with `--surface` |
| `--sparseness` | `-s` | blank-line policy, v.i. |
| `--reverse-order` | none | reverse sibling order at every level of the tree walk |

`--variant`/`--conditional-sidecar` union additively with whatever
`--surface` derives; omitting a flag keeps that subcommand's own default
rather than clobbering a `register_blueprint()` entry's own
`render_profile`. Merge semantics live in `CONTEXT.md`. `claude
user-system-prompt` already owns `-c` for `--coder`, so
`--comment`/`--no-comment` are long-form only there. `kaye-engine
blueprint preview` is not a rendering command but shares the
`--comment`/`--no-comment` toggle (`-c`/`-C` included there).

`--sparseness SPARSENESS` controls blank-line collapsing in the
rendered output: `-1` joins everything into one line, `0` strips all
blank lines, `1` collapses every run to a single blank line, up through
`99` which disables trimming entirely. The default lives in
`DEFAULT_SPARSENESS` (`kaye_engine/cli/__init__.py`) unless a caller
overrides it. Blank lines inside a fenced code block are never collapsed
or stripped by any sparseness level, including `-1`.

`claude vs-code-extension` also writes `permissions` (`allow`/`ask`/`deny`
Bash command patterns) into `settings.json`, sourced from
`kaye_engine/cli/claude/permission_cmds.jsonc` (parsed with `json5`, so
comments are allowed).

Every `claude` subcommand needs a consumer to call
`setup_claude_cli(plugin_name, display_name, marketplace_name,
chat_exportable_name, merged_coder_exportable_name, version,
marketplace_folder_name)` before invoking the CLI — no default exists for
any of the seven. On a bare checkout, or when it was never called, the
getters log `logger.critical` and raise `SystemExit(1)` — expected, not a
bug. Full getter list and rationale in `CONTEXT.md`.

`kaye-engine --version` reports the installed distribution's version via
`importlib.metadata.version(PACKAGE_NAME)` — run against an installed
package, not a bare checkout.

`--surface` takes combinable names keyed into the consumer-supplied
`surface_profiles` dict, and is omitted entirely from the parser when no
consumer project configures it. Mechanics in `CONTEXT.md`.

## Code Conventions

- follow **PEP 8**; keep lines within **80 characters**
- use **Sphinx**-style docstrings written in **reStructuredText**
- public methods must have docstrings; private methods (`_` prefix) only
  when the name is not self-explanatory
- test files end with `_test.py` and mirror the source tree under `tests/`
- test classes are grouped as `TestStructure`, `TestHeader`, `TestContent`
- use comment section headings (`#`, `=`, `*`, `+`, `-`) only for long files
- log through the `kamilog` package (`import kamilog`; a dependency, not
  vendored): report every file or directory action as a deed
  (`with logger.track.create_file(path)`, `pack_files`, `mv_file`,
  `save_config`, ...) rather than a hand-built string, and mark a run mode
  with a badge (`badges="dry"`); keep `done` for a whole-export summary

## Registering a Blueprint

`register_blueprint()` in `kaye_engine/prompt/blueprint/registry.py` is the
only gate — every exporter reads `blueprint_registry` directly. **Calls
live in the consumer package**, not here. The signature is
`register_blueprint(canonical_name, blueprint, *, display_name="", ...)`: the
entry's name is `blueprint.meta.display_name`, and `display_name=` only backs
it when the meta name is empty.

Export policy — one gate plus three independent flags, no allow-list
constant:

| flag | default | effect |
|---|---|---|
| `is_exportable` | `True` | `False` excludes it from `exportable_registry` entirely — never export as an Agent Skill |
| `is_user_invokable` | `True` | a human may invoke it by name |
| `llm_invokable` | `True` | the assistant may surface it unprompted |
| `always_apply` | `False` | unconditionally relevant; `continue` exports it as an always-apply rule, the Agent Skill exporter ignores it |

`render_profile` (a `RenderProfile`, default `RenderProfile()`) sets
this entry's own default render settings — including
`conditional_sidecars`/`variants` — merged (not clobbered) by
`BlueprintRegistry.content()` with any caller-supplied `profile=`
via `RenderProfile.merge()`.

`register_image_prompt_exportable(canonical_name)`
(`kaye_engine/exportable/image_prompt_export.py`) marks an already-registered
`exportable_registry` entry as a member of the image-prompt export subset
(`image_prompt_exportable_registry`) that `export-image-prompt`/`img` reads.
**Calls live in the consumer package**, same as `register_blueprint()`;
it raises `KeyError` if `canonical_name` is not already registered,
`ValueError` on a duplicate.

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
  affordances, abbreviations, exportable registry, Claude integration, Open WebUI export
- `CONTEXT.md` — architecture, entities, boundaries
- `CHANGELOG.md` — record notable changes per release
- this `AGENTS.md` — update agent-specific rules as structure evolves

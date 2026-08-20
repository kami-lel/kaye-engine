# kaye-engine CONTEXT

**Last updated:** 2026-08-18

System knowledge for the **kaye-engine** repository — architecture,
entities, and boundaries. Read this alongside `AGENTS.md` before making
changes. Implementation detail lives in `docs/`, linked per topic below.

## Project Overview

**kaye-engine** parses one structured Markdown file into a tree, then
renders selected subsets of that tree as scenario-ready prompts, exposed
through a Python API and a CLI.

| aspect | value |
|---|---|
| language | Python `>=3.11` |
| distribution / import name | `kaye-engine` / `kaye_engine` |
| dependencies | `anytree`, `json5`, `pyahocorasick`, `pyyaml` |
| entry point | `kaye-engine` console script → `kaye_engine.__main__:main` |
| CLI subcommands | `blueprint`, `claude`, `dynamic-node`, `exportable`, `affordance`, `glossary` |

## Personalization Boundary

`kaye-engine` is a public mechanism package, extended by a separate private
repository that supplies the actual identity content, abbreviations, and
blueprint registrations the mechanism operates on. The dependency runs one
direction only: a personalized consumer project depends on `kaye-engine`;
`kaye-engine` must build, test, and export with no knowledge of what any
such project supplies.

Three things are therefore absent by design — a corpus file, an
`abbrs.json`, and any `register_blueprint()` call. Absence is the contract,
not a gap to fill.

## Domain Model

| entity | what it is |
|---|---|
| **Prompt Corpus** | a Markdown file; the authoritative source of truth |
| **Prompt Tree** | the parsed corpus; every heading a `BasePromptNode` |
| **Blueprint** | a selection spec marking which tree nodes render |
| **Blueprint Registry** | name → blueprint plus its export policy |
| **Exportable** | common base for anything `exportable_registry` holds — `BlueprintRegistry` and `ExportableAbbr` are its two implementers |
| **Role** | a task-specific behavior profile held inside the corpus |
| **Sidecar Node** | a `{name}` subnode; metadata or conditional content |
| **Dynamic Node** | a `(name)` node (canonical kebab-case `NAME`) whose content is generated at render |
| **Affordance** | a named platform capability, tracked in `affordance_registry` |
| **RenderProfile** | a `kw_only` dataclass bundling render settings (`conditional_sidecars`, `affordances`, `sparseness`, ...); `.merge()` overrides scalar fields and unions the collection fields |

Heading syntax carries node type: plain text is an ordinary corpus node,
`{braces}` a sidecar, `(parentheses)` a dynamic node.

```
corpus.md ──load_corpus_tree()──> Prompt Tree ─┐
                                               ├─generate_prompt()─> text
blueprint text ──PromptBlueprint.parse()───────┘
```

Rendering takes a `sparseness` parameter governing how runs of blank lines
collapse in the output, from `-1` (whole output joined onto one line) through
`99` (no trimming); descriptor sidecar rendering always renders at `-1` so a
multi-line description or when-to-use collapses to one string.

Sidecars split by usage rather than by class. *Descriptor* sidecars
(`{description}`, `{when_to_use}`, `{globs}`) are consumed as blueprint
metadata and never rendered; every other name is a *conditional* sidecar,
real content spliced in only when its name is on a `RenderProfile`'s
`conditional_sidecars`, or matched via that same profile's `affordances`
field against `affordance_registry`. Q.v. [sidecar node
documentation](docs/sidecar-node-doc.md).

`affordance_registry` tracks platform capabilities as `Affordance` entries
and derives each one's Usage/Lack sidecar names; a Kaye-specific,
consumer-supplied `surface_profiles` dict (`dict[str, RenderProfile]`,
passed to `setup_claude_cli(...)` — kaye-vault owns the actual Claude
surface data, q.v. `kaye_vault/claude_render_profiles.py`) maps a surface
name to the `RenderProfile` carrying that surface's affordances/
conditional-sidecars. Every **rendering command** — any CLI subcommand
that reaches `PromptBlueprint.generate_prompt(...)`, directly or via
`Exportable.content()` — exposes the same 5 options (`--surface`,
`--comment`/`--no-comment`, `--conditional-sidecar`, `--affordance`,
`--sparseness`) via one shared parent parser and one aux function,
`build_render_profile_parent_parser`/`resolve_render_profile`
(`kaye_engine/cli/render_profile_parser.py`); `resolve_render_profile`
returns a single `RenderProfile` (not a kwargs dict), built by merging
each selected surface's profile with one built from the explicit
`--affordance`/`--conditional-sidecar`/`--sparseness`/`--comment` flags
via `RenderProfile.merge()` -- `--affordance`/`--conditional-sidecar`
union additively with whatever `--surface` derives, so rendered prompts
auto-checkmark the sidecars real on that surface plus any named
explicitly. `--surface` itself is omitted entirely from the parser when
no consumer project configures `surface_profiles`. Each subcommand keeps
its own pre-existing default for `--comment`/`--no-comment` and
`--sparseness` when the flags are omitted (via
`build_sparseness_parent_parser(default=...)`, a per-call builder). The
resolved `RenderProfile` is carried as a single `profile=` object from
parser down through every `claude` export chain (skill/plugin/
marketplace/vs-code/code/user-prompt), instead of threading
`surface`/`sparseness`/`show_comment` as separate params at each layer.
A `RenderProfile()` default (no explicit `--surface`/`--affordance`/
`--conditional-sidecar`) carries `affordances=None`/
`conditional_sidecars=()`, which `RenderProfile.merge()` treats as a
no-op contribution, so a `register_blueprint()` entry's own
`render_profile` defaults still apply -- `BlueprintRegistry.content()`
merges them in via `self.render_profile.merge(profile)` whenever the
caller (`blueprint generate`, `Skill.from_exportable()`) passes a
`profile=`. Q.v. [Claude documentation](docs/claude-doc.md) and
[sidecar node documentation](docs/sidecar-node-doc.md).

Dynamic nodes auto-attach to every tree at load time — no authored
heading required for existence — and cover today's date plus the
abbreviation glossaries; an authored `(name)` heading, at any depth,
fixes the node's preface and tree location in place of the heading
itself, else it falls back to a direct child of root. A second,
independent mechanism, inline `(((name)))` substitution, resolves the
same canonical names anywhere inside rendered prompt text at
`generate_prompt()` time. Q.v. [dynamic node
documentation](docs/dynamic-content-doc.md) and [abbreviation
collection documentation](docs/abbrs-doc.md).

## Public API

```python
from kaye_engine import (
    PACKAGE_NAME, LOGGER_NAME,
    load_corpus_tree, get_default_corpus_tree,
    AbbrData,
    register_abbr_glossary,
    register_blueprint,
    setup_claude_cli,
)
```

`get_abbr_data`, `get_abbr_glossary`, `get_blueprint`, and `get_corpus_tree`
are not exported at this top level — reach them through their owning
submodule (`kaye_engine.abbr_collection`, `kaye_engine.prompt`) instead.
`Exportable`, `exportable_registry`, `register_exportable_entry`, and
`get_exportable` (`kaye_engine.exportable`) round out the registry every
`BlueprintRegistry` and `ExportableAbbr` entry is inserted into.

A caller loads and caches a corpus by name; one tree may be flagged the
process default, which is what a blueprint resolves against when given no
explicit tree. A consumer that exports through `claude` subcommands must also
call `setup_claude_cli(plugin_name, display_name, marketplace_name,
chat_exportable_name, chat_coder_exportable_name, version,
marketplace_folder_name)` — none of the seven has a default; `display_name` replaces the former hardcoded
`DISPLAY_NAME` constant, letting each consumer stamp its own
`plugin.json` `display_name`. Q.v. [Kaye Engine: `prompt` module
Documentation](docs/prompt-doc.md).

Every CLI subcommand entrypoint calls a setup guard
(`check_corpus_setup_for_cli()`, or `check_setup_for_claude_cli()` for
`claude` subcommands) that logs an error — never raises — when a consumer
hasn't loaded a default corpus tree or registered any blueprints. It exists
to surface a bare-checkout misuse early, not to enforce the boundary. The
plugin name, display name, marketplace name, Chat/Coder blueprint names,
version, and marketplace folder name are enforced separately, each by its own
getter (`get_plugin_name()`, `get_claude_cli_display_name()`,
`get_marketplace_name()`, `get_claude_chat_exportable()`,
`get_claude_chat_coder_exportable()`, `get_claude_cli_consumer_version()`,
`get_marketplace_folder_name()`), which logs `logger.critical` and raises
`SystemExit(1)` when unset — or, for the blueprint getters, when the
configured name is not in `blueprint_registry` — rather than letting `None`
or an unresolved name reach path, manifest, or prompt building.

## Repository Layout

```
kaye_engine/
├── prompt/              parse, model, select, render
│   ├── blueprint/       PromptBlueprint, registry, rendering
│   │   └── render_profile.py   RenderProfile: layerable render-kwargs bundle
│   ├── dynamic_nodes/   render-time generated node types
│   └── affordance_registry.py  Affordance entries, Usage/Lack sidecar names
├── abbr_collection/     abbreviation entries, store, JSON loader
├── exportable/           Exportable base, exportable_registry
├── cli/
│   ├── blueprint/       `blueprint`/`bp` subcommand: ls, show, generate
│   ├── claude/          skills, plugins, marketplaces, CLAUDE.md
│   │   ├── setup.py               setup_claude_cli(...); registers
│   │   │                          consumer-supplied affordance_names,
│   │   │                          stores surface_profiles
│   │   └── surface_parser.py      shared `--surface` parent parser --
│   │                              choices from consumer's surface_profiles
│   ├── dynamic_node/    `dynamic-node`/`dn` subcommand: multi-node render
│   ├── affordance_parser.py  `affordance` subcommand (no alias): list affordance_registry
│   ├── glossary_parser.py    `glossary`/`g` subcommand: print/list glossaries
│   ├── comment_parser.py     shared `--comment`/`--no-comment` parent parser
│   ├── render_profile_parser.py  shared 5-option parent parser + aux fn
│   └── exportable_parser.py  `exportable`/`x` subcommand: print, list exportables
└── kamilog.py           logging, shared across the package
docs/                    per-topic reference, linked above
tests/                   prompt/, abbr/, cli/ — mirrors the source
```

The `prompt` layer is pure: it knows nothing of Claude or any export
target. Every export target is a leaf under `cli/`, and each reads
the same `blueprint_registry` rather than holding its own list.

## Testing Strategy

`pytest`, 690 tests, run **serially by design** — cases are cheap in-process
assertions, so worker startup costs more than a split saves, and shared
fixtures carry run-order assumptions. `pytest-xdist` is deliberately absent
from the `dev` extra.

Tests mirror the source tree: `tests/prompt/` for the engine, `tests/abbr/`
for the abbreviation collection. `tests/cli/` stays deliberately thin — it
holds only the corpus-independent pieces (setup guard, exportable-abbr
registration, `dynamic-node` parsing, `SKILL.md` rendering), because the
exporters need a corpus to produce output and the consumer package covers
those. `exportable`, `affordance`, and `glossary` parser tests are now
covered; the `blueprint` subcommand parser still has no dedicated tests.

## Maintaining This File

Update `CONTEXT.md` in the same change as the architecture change, and
refresh `Last updated` whenever content changes. Revisit it when entities or
node types are added, when a boundary moves, when the public API changes, or
when the test layout shifts.

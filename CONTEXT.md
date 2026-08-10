# kaye-engine CONTEXT

**Last updated:** 2026-08-10

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
| CLI subcommands | `blueprint`, `claude`, `dynamic-node`, `export` |

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
| **Dynamic Node** | a `(Name)` node whose content is generated at render |

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
real content spliced in only when its name is passed to `contains_sidecars`.
Q.v. [sidecar node documentation](docs/sidecar-node-doc.md).

Dynamic nodes are attached to the tree at load time and cover today's date
plus the abbreviation glossaries. Q.v. [dynamic node
documentation](docs/dynamic-node-doc.md) and [abbreviation collection
documentation](docs/abbrs-doc.md).

## Public API

```python
from kaye_engine import (
    PACKAGE_NAME, DISPLAY_NAME, LOGGER_NAME,
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
call `setup_claude_cli(plugin_name, marketplace_name, chat_bp_name,
coder_bp_name, version, marketplace_folder_name)` — none of the six has a
default. Q.v. [Kaye Engine: `prompt` module Documentation](docs/prompt-doc.md).

Every CLI subcommand entrypoint calls a setup guard
(`check_corpus_setup_for_cli()`, or `check_setup_for_claude_cli()` for
`claude` subcommands) that logs an error — never raises — when a consumer
hasn't loaded a default corpus tree or registered any blueprints. It exists
to surface a bare-checkout misuse early, not to enforce the boundary. The
plugin name, marketplace name, Chat/Coder blueprint names, version, and
marketplace folder name are enforced separately, each by its own getter
(`get_plugin_name()`, `get_marketplace_name()`, `get_claude_chat_blueprint()`,
`get_claude_coder_blueprint()`, `get_claude_cli_consumer_version()`,
`get_marketplace_folder_name()`), which logs `logger.critical` and raises
`SystemExit(1)` when unset — or, for the blueprint getters, when the
configured name is not in `blueprint_registry` — rather than letting `None`
or an unresolved name reach path, manifest, or prompt building.

## Repository Layout

```
kaye_engine/
├── prompt/              parse, model, select, render
│   ├── blueprint/       PromptBlueprint, registry, rendering
│   └── dynamic_nodes/   render-time generated node types
├── abbr_collection/     abbreviation entries, store, JSON loader
├── exportable.py        Exportable base, exportable_registry
├── cli/
│   ├── blueprint/       `blueprint`/`bp` subcommand: ls, show, generate
│   ├── claude/          skills, plugins, marketplaces, CLAUDE.md
│   ├── dynamic_node/    `dynamic-node`/`dn` subcommand: multi-node render
│   └── exportable_parser.py  `export`/`x` subcommand: print, list exportables
└── kamilog.py           logging, shared across the package
docs/                    per-topic reference, linked above
tests/                   prompt/, abbr/, cli/ — mirrors the source
```

The `prompt` layer is pure: it knows nothing of Claude or any export
target. Every export target is a leaf under `cli/`, and each reads
the same `blueprint_registry` rather than holding its own list.

## Testing Strategy

`pytest`, 667 tests, run **serially by design** — cases are cheap in-process
assertions, so worker startup costs more than a split saves, and shared
fixtures carry run-order assumptions. `pytest-xdist` is deliberately absent
from the `dev` extra.

Tests mirror the source tree: `tests/prompt/` for the engine, `tests/abbr/`
for the abbreviation collection. `tests/cli/` stays deliberately thin — it
holds only the corpus-independent pieces (setup guard, exportable-abbr
registration, `dynamic-node` parsing, `SKILL.md` rendering), because the
exporters need a corpus to produce output and the consumer package covers
those. The `blueprint` and `export` subcommand parsers currently have no
dedicated tests.

## Maintaining This File

Update `CONTEXT.md` in the same change as the architecture change, and
refresh `Last updated` whenever content changes. Revisit it when entities or
node types are added, when a boundary moves, when the public API changes, or
when the test layout shifts.

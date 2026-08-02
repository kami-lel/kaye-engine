# kaye-engine CONTEXT

**Last updated:** 2026-08-02

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
| CLI subcommands | `prompt`, `claude` |

## Personalization Boundary

`kaye-engine` is a public mechanism package, extended by a separate private
repository that supplies the actual identity content, abbreviations, and
blueprint registrations the mechanism operates on. The dependency runs one
direction only: a personalized project depends on `kaye-engine`;
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

Sidecars split by usage rather than by class. *Descriptor* sidecars
(`{description}`, `{when_to_use}`, `{globs}`) are consumed as blueprint
metadata and never rendered; every other name is a *conditional* sidecar,
real content spliced in only when its name is passed to `contains_sidecars`.
Q.v. [sidecar node documentation](docs/sidecar-node-doc.md).

Dynamic nodes are attached to the tree at load time and cover today's date
plus the abbreviation groups. Q.v. [dynamic node
documentation](docs/dynamic-node-doc.md) and [abbreviation collection
documentation](docs/abbr-collection-doc.md).

## Public API

```python
from kaye_engine import (
    PACKAGE_NAME, DISPLAY_NAME, LOGGER_NAME,
    load_corpus_tree, get_corpus_tree, get_default_corpus_tree,
    AbbrData, get_abbr_data,
    register_blueprint, get_blueprint,
    set_claude_plugin_marketplace_name,
)
```

A caller loads and caches a corpus by name; one tree may be flagged the
process default, which is what a blueprint resolves against when given no
explicit tree. A host that exports through `claude` subcommands must also
call `set_claude_plugin_marketplace_name()` to name the plugin/marketplace
for Anthropic's tooling. Q.v. [programmatic API
documentation](docs/programmatic-api-doc.md).

Every CLI subcommand entrypoint calls a setup guard
(`check_corpus_setup_for_cli()`, or `check_setup_for_claude_cli()` for
`claude` subcommands) that logs a warning — never raises — when a host
hasn't loaded a default corpus tree or registered any blueprints. It exists
to surface a bare-checkout misuse early, not to enforce the boundary. The
plugin/marketplace name is enforced separately: any `claude` export
subcommand that needs it calls `get_plugin_marketplace_name()`, which logs
`logger.critical` and raises `SystemExit(1)` when unset, rather than letting
`None` reach path or manifest building.

## Repository Layout

```
kaye_engine/
├── prompt/              parse, model, select, render
│   ├── blueprint/       PromptBlueprint, registry, rendering
│   └── dynamic_nodes/   render-time generated node types
├── abbr_collection/     abbreviation entries, store, JSON loader
├── cli/
│   ├── prompt/          `prompt` subcommand: ls, show, generate
│   ├── claude/          skills, plugins, marketplaces, CLAUDE.md
│   └── cli_continue/    deprecated; never registered, unreachable
└── kamilog.py           logging, shared across the package
dify_studio/             Dify workflow node sources, outside the package
docs/                    per-topic reference, linked above
examples/                standalone scripts, outside the package
tests/                   prompt/, abbr/, cli/, dify/ — mirrors the source
```

The `prompt` layer is pure: it knows nothing of Claude, Continue, or any
export target. Every export target is a leaf under `cli/`, and each reads
the same `blueprint_registry` rather than holding its own list.

## Testing Strategy

`pytest`, 692 tests, run **serially by design** — cases are cheap in-process
assertions, so worker startup costs more than a split saves, and shared
fixtures carry run-order assumptions. `pytest-xdist` is deliberately absent
from the `dev` extra.

Tests mirror the source tree: `tests/prompt/` for the engine, `tests/abbr/`
for the abbreviation collection, `tests/dify/` for the `dify_studio/`
workflow nodes. `tests/cli/` stays deliberately thin — it holds only the
corpus-independent pieces, version resolution and `SKILL.md` rendering,
because the exporters need a corpus to produce output and the host package
covers those.

## Maintaining This File

Update `CONTEXT.md` in the same change as the architecture change, and
refresh `Last updated` whenever content changes. Revisit it when entities or
node types are added, when a boundary moves, when the public API changes, or
when the test layout shifts.

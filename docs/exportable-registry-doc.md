# `exportable` Documentation

<!-- FIXME review this doc -->

`exportable` treats everything a consumer might want exported — a `PromptBlueprint`, an abbreviation/glossary group — as one collection, `exportable_registry`, keyed by the exact name it exports under.




## Programmatic API

`Exportable` is the abstract base class every exportable kind implements directly — `BlueprintRegistry` and `ExportableAbbr` (q.v. [`abbr-collection-doc.md`](abbr-collection-doc.md)) each subclass it, so a registry entry *is* the `Exportable`, never a copy. `exportable_registry` is the plain `dict`, `canonical_name -> Exportable`, populated via `register_exportable_entry` and read via `get_exportable`.

`register_blueprint` creates a `BlueprintRegistry` (adding `blueprint` and `is_internal`) and inserts it into `blueprint_registry`, plus `exportable_registry` unless `is_internal`; `get_blueprint` looks it back up. `register_exportable_abbrs` recomputes every abbr/glossary group fresh and (re-)inserts each into `exportable_registry` — unlike blueprints, these must be re-run whenever `AbbrData` changes.

Q.v. each function's docstring for full parameters and usage examples.




## usages

Q.v. [registered abbr groups](abbr-collection-doc.md#registered-abbr-groups) for which glossaries a given consumer actually registers and exports.

### `claude` CLI

`Skill.from_exportable(exportable, version="")` (`kaye_engine.cli.claude.skill.skill_md`) is the Claude-specific translation layer, dispatching on the concrete `Exportable` implementer to build a `SKILL.md`. `export_skills_as_folders(parent_folder, *, version)` registers every abbr group, then writes one skill folder per `exportable_registry` entry.

Q.v. [`claude-doc.md`](claude-doc.md) for the full Claude CLI surface (`kaye-engine claude skill|plugin|marketplace|code|...`).

### `export` CLI

A generic, Claude-agnostic CLI command (alias `x`) that prints any exportable's `content()` straight to stdout, or lists every registered canonical name — structured like `kaye-engine dynamic-node`/`dn` (q.v. [`dynamic-node-doc.md`](dynamic-node-doc.md)).

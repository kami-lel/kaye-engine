# `exportable` Documentation

`exportable` treats everything a consumer might want exported — a `PromptBlueprint`, an abbreviation/glossary group — as one collection, `exportable_registry`, keyed by the exact name it exports under.













## Programmatic API

`Exportable` is the abstract base class every exportable kind implements directly — `BlueprintRegistry` and `ExportableAbbr` (q.v. [`abbr-collection-doc.md`](abbr-collection-doc.md)) each subclass it, so a registry entry *is* the `Exportable`, never a copy. `exportable_registry` is the plain `dict`, `canonical_name -> Exportable`, populated via `register_exportable_entry` and read via `get_exportable`.

`register_blueprint` creates a `BlueprintRegistry` (adding `blueprint` and `is_internal`) and inserts it into `blueprint_registry`, plus `exportable_registry` unless `is_internal`; `get_blueprint` looks it back up. `register_exportable_abbrs` recomputes every abbr/glossary group fresh and (re-)inserts each into `exportable_registry` — unlike blueprints, these must be re-run whenever `AbbrData` changes.













## Registration and Usage

Registration:

- blueprints: each consumer registers its own, via `register_blueprint`
- abbr/glossary groups: registered via `register_exportable_abbrs`, q.v. [registered abbr groups](abbr-collection-doc.md#registered-abbr-groups)

Usage:

- `claude` CLI: q.v. [`claude-doc.md`](claude-doc.md) for the full Claude CLI surface (`kaye-engine claude skill|plugin|marketplace|code|...`)
- `export` CLI: `kaye-engine export`

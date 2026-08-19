# Kaye Engine: `Exportable` registry

`exportable` treats everything a consumer might want exported — a `PromptBlueprint`, an abbreviation/glossary group — as one collection, `exportable_registry`, keyed by the exact name it exports under.













## Programmatic API

`Exportable` is the abstract base class every exportable kind implements directly — `BlueprintRegistry` and `ExportableAbbr` (q.v. [`abbrs-doc.md`](abbrs-doc.md)) each subclass it, so a registry entry *is* the `Exportable`, never a copy. `exportable_registry` is the plain `dict`, `canonical_name -> Exportable`, populated via `register_exportable_entry` and read via `get_exportable`.

`register_blueprint` creates a `BlueprintRegistry` (adding `blueprint` and `is_exportable`) and inserts it into `blueprint_registry`, plus `exportable_registry` when `is_exportable`; `get_blueprint` looks it back up. `register_exportable_abbrs` recomputes every abbr/glossary group fresh and (re-)inserts each into `exportable_registry` — unlike blueprints, these must be re-run whenever `AbbrData` changes.

Concrete `Exportable` kinds each define their own `.merge(other)` — combining two compatible exportables into a new, unregistered instance; `Exportable` itself declares no shared `merge`/`|` contract, since a merge's meaning is kind-specific. `BlueprintRegistry.merge()` unions both blueprints' checkmarked nodes (via `PromptBlueprint.merge()`/`|`) and merges `render_profile` (via `RenderProfile.merge`), keeping every other field (name, invokability, ...) from `self`; it raises `TypeError` when merged against a different `Exportable` kind. A concrete kind with no sensible merge, e.g. `ExportableAbbr`, raises `NotImplementedError` instead.













## Registration and Usage

Two kinds of exportable registration feed `exportable_registry`:

- [engine registered exportable](#engine-registered-exportable):
  always registered, by the engine;
  generate during runtime, all abbrs later added will also be rendered

- **consumer registered exportable**

  - blueprint: `register_blueprint()`
    will automatically register the blueprint into `exportable_registry`
  - glossary: `register_abbr_glossary()` registers the glossary's name
    and settings into `abbr_glossary_registry`; `register_exportable_abbrs()`
    (re-run whenever `AbbrData` changes) is what actually inserts the
    glossary's group into `exportable_registry`

Usage:

- `exportable` CLI (alias `x`): `kaye-engine exportable EXPORTABLE` prints that exportable's `content()`; `kaye-engine exportable ls` lists every registered exportable name, sorted alphabetically
- `claude` CLI: q.v. [`claude-doc.md`](claude-doc.md) for the full Claude CLI surface (`kaye-engine claude skill|plugin|marketplace|code|...`)













## Engine Registered Exportable

Abbreviation Group by Tag:

| canonical name | display name | user_invokable | llm_invokable |
| --- | --- | --- | --- |
| `abbr-single-character` | Abbr Single Character | ❌ | ✔️ |
| `abbr-emoji` | Abbr Emoji | ❌ | ✔️ |

Abbreviation Group by Wrap:

| canonical name | display name | user_invokable | llm_invokable |
| --- | --- | --- | --- |
| `abbr-prefixes` | Abbr Prefixes | ❌ | ✔️ |
| `abbr-suffixes` | Abbr Suffixes | ❌ | ✔️ |
| `abbr-symbols` | Abbr Symbols | ❌ | ✔️ |

Abbreviation *Starts-With*:

| canonical name | display name | user_invokable | llm_invokable |
| --- | --- | --- | --- |
| `abbr-starts-with-digits-0-9` | Abbr Starts with Digits 0~9 | ❌ | ✔️ |
| `abbr-starts-with-a` | Abbr Starts with A | ❌ | ✔️ |
| `abbr-starts-with-b` | Abbr Starts with B | ❌ | ✔️ |
| `abbr-starts-with-c` | Abbr Starts with C | ❌ | ✔️ |
| `abbr-starts-with-d` | Abbr Starts with D | ❌ | ✔️ |
| `abbr-starts-with-e` | Abbr Starts with E | ❌ | ✔️ |
| `abbr-starts-with-f` | Abbr Starts with F | ❌ | ✔️ |
| `abbr-starts-with-g` | Abbr Starts with G | ❌ | ✔️ |
| `abbr-starts-with-h` | Abbr Starts with H | ❌ | ✔️ |
| `abbr-starts-with-i` | Abbr Starts with I | ❌ | ✔️ |
| `abbr-starts-with-j` | Abbr Starts with J | ❌ | ✔️ |
| `abbr-starts-with-k` | Abbr Starts with K | ❌ | ✔️ |
| `abbr-starts-with-l` | Abbr Starts with L | ❌ | ✔️ |
| `abbr-starts-with-m` | Abbr Starts with M | ❌ | ✔️ |
| `abbr-starts-with-n` | Abbr Starts with N | ❌ | ✔️ |
| `abbr-starts-with-o` | Abbr Starts with O | ❌ | ✔️ |
| `abbr-starts-with-p` | Abbr Starts with P | ❌ | ✔️ |
| `abbr-starts-with-q` | Abbr Starts with Q | ❌ | ✔️ |
| `abbr-starts-with-r` | Abbr Starts with R | ❌ | ✔️ |
| `abbr-starts-with-s` | Abbr Starts with S | ❌ | ✔️ |
| `abbr-starts-with-t` | Abbr Starts with T | ❌ | ✔️ |
| `abbr-starts-with-u` | Abbr Starts with U | ❌ | ✔️ |
| `abbr-starts-with-v` | Abbr Starts with V | ❌ | ✔️ |
| `abbr-starts-with-w` | Abbr Starts with W | ❌ | ✔️ |
| `abbr-starts-with-x` | Abbr Starts with X | ❌ | ✔️ |
| `abbr-starts-with-y` | Abbr Starts with Y | ❌ | ✔️ |
| `abbr-starts-with-z` | Abbr Starts with Z | ❌ | ✔️ |
| `abbr-starts-with-non-alphanumeric` | Abbr Starts with Non-Alphanumeric | ❌ | ✔️ |

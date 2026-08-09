# `exportable` Documentation

<!-- FIXME review this doc -->

`exportable` is the module that lets kaye-engine treat every thing a consumer might want exported — a `PromptBlueprint`, an abbreviation/glossary group — as one collection, `exportable_registry`, keyed by the exact name it should be exported under.

Before this module existed, blueprints lived in `blueprint_registry` (keyed by an arbitrary internal slug, e.g. `"date-time"`) and abbr/glossary groups were only ever computed on demand via `get_exportable_abbrs()`, never registered anywhere. Two collections meant no single place to answer "what does this consumer export," and the internal slug was disconnected from the name actually written to disk. `exportable_registry` fixes both: one dict, and its key *is* the exported name.




















## `Exportable`

`Exportable` is an **abstract base class** — a template every exportable kind implements directly, not a wrapper that holds a reference to one. `BlueprintRegistry` (q.v. [`programmatic-api-doc.md`](programmatic-api-doc.md), "blueprint registry" — predates this module, its `register_blueprint` signature shown there is stale) and `ExportableAbbr` (q.v. [`abbr-collection-doc.md`](abbr-collection-doc.md)) each subclass it, so the registry entry or abbr group stored in `exportable_registry` *is* the `Exportable` — never a copy of its data, never a second object standing in front of it.

```python
from dataclasses import dataclass
from kaye_engine.exportable import Exportable

@dataclass(kw_only=True)
class MyExportable(Exportable):
    payload: str

    def content(self):
        return self.payload
```

Every `Exportable` carries five fields:

- `canonical_name`: kebab-case name, used directly as the exported skill name — no separate derivation step
- `display_name`: human-readable name
- `always_apply`: whether this entry is unconditionally relevant, rather than surfaced only when judged relevant
- `user_invokable`: whether a human may deliberately invoke this entry by name
- `llm_invokable`: whether the assistant may bring this entry into play on its own judgment

...and one abstract method:

- `content()`: this exportable's generic, non-Claude-specific displayable content — the rendered prompt for a blueprint, the markdown abbr list for an abbr group

> [!NOTE]
> `Exportable` is `@dataclass(kw_only=True)`. That is what lets a subclass add its own *required* field (`BlueprintRegistry.blueprint`, below) *after* this base class's defaulted fields, without dataclass's usual "non-default argument follows default argument" error.

`ExportableAbbr` additionally subclasses `list`, since an abbr group is also a plain iterable of `AbbrEntry`. Because `Exportable` is a dataclass and `list` is not, `ExportableAbbr.__init__` calls both parents explicitly (`list.__init__(self, entries)`, `Exportable.__init__(self, ...)`) rather than relying on cooperative `super()`.




















## `exportable_registry`

```python
from kaye_engine.exportable import exportable_registry

for name, exportable in sorted(exportable_registry.items()):
    print(name, "->", exportable.display_name)
```

A plain `dict`, `canonical_name -> Exportable`, exactly mirroring `blueprint_registry`'s shape.




#### `register_exportable_entry(exportable)`

Insert `exportable` under its own `canonical_name`.

```python
from kaye_engine.exportable import register_exportable_entry

register_exportable_entry(my_exportable)
```

Raises `ValueError` if `canonical_name` is already registered.




#### `get_exportable(canonical_name)`

```python
from kaye_engine.exportable import get_exportable

get_exportable("coder")
```

Raises `KeyError` if nothing is registered under `canonical_name`.




















## `BlueprintRegistry`

`BlueprintRegistry(Exportable)` adds exactly two fields on top of the inherited five:

- `blueprint`: the underlying `PromptBlueprint`
- `is_internal`: never export this blueprint as a Claude Agent Skill; defaults to `False`

```python
reg.content()  # == reg.blueprint.generate_prompt(sparseness=0)
```

`is_internal` generalizes what used to be `skill_exportable` (inverted): a blueprint meant only to be a top-level system prompt or a building block for other blueprints — `rapid`, `chat`, `style` in a typical consumer — sets `is_internal=True` and never reaches `exportable_registry`.




#### `register_blueprint(canonical_name, display_name, blueprint, *, is_internal=False, always_apply=False, user_invokable=True, llm_invokable=True)`

Creates a `BlueprintRegistry` and inserts it into `blueprint_registry` under `canonical_name`; unless `is_internal`, the *same instance* is also inserted into `exportable_registry` via `register_exportable_entry` — one object, two lookup paths.

```python
from kaye_engine import register_blueprint

register_blueprint("coder", "Kaye Peer Coder", coder_blueprint, always_apply=True)
register_blueprint("chat", "Chat", chat_blueprint, is_internal=True)
```

Raises `ValueError` if `canonical_name` is already registered in `blueprint_registry`.

> [!IMPORTANT]
> `canonical_name` is now the *only* name that matters — it is simultaneously the `blueprint_registry`/`exportable_registry` key and the exported skill's folder name. There is no separate "internal slug vs. display-name-derived skill name" step to keep in sync.




#### `get_blueprint(canonical_name)`

```python
from kaye_engine import get_blueprint

get_blueprint("coder")
```

Raises `KeyError` if nothing is registered under `canonical_name`.




















## abbr/glossary groups

`ExportableAbbr` (defined in `kaye_engine.cli.exportable_abbr`, q.v. [`abbr-collection-doc.md`](abbr-collection-doc.md) for the underlying `AbbrData`/`AbbrEntry` it groups) implements `Exportable` directly, the same way `BlueprintRegistry` does — no separate wrapper class exists for either kind.

```python
group.content()  # == group.as_md_list()
```

#### `register_exportable_abbrs()`

```python
from kaye_engine.cli.exportable_abbr import register_exportable_abbrs

register_exportable_abbrs()
```

Computes every exportable abbr/glossary group fresh (via `get_exportable_abbrs()`) and registers each one into `exportable_registry`, replacing any previously-registered entry under the same key.

> [!NOTE]
> Unlike blueprints, which register once and stay put, abbr groups are recomputed on every call — this function must run again whenever `AbbrData` may have changed, before anything reads `exportable_registry` for abbr content.




















## Claude export

`kaye_engine.cli.claude.skill.skill_md.Skill.from_exportable(exportable, version="")` is the Claude-specific translation layer: it dispatches on the concrete `Exportable` implementer via `isinstance`, reading whichever fields that kind needs to build a `SKILL.md` (a blueprint's `sidecars`/`generate_prompt(...)`, or an abbr group's `as_md_list()`). This `isinstance` check lives here, deliberately, rather than as a method on `Exportable` itself, so `Exportable` stays Claude-agnostic and reusable by non-Claude consumers.

`export_skills_as_folders(parent_folder, *, version)` (`kaye_engine.cli.claude.skill.export_folders`) calls `register_exportable_abbrs()` once, then loops over every `exportable_registry` value — the entire `kaye-engine claude skill` export surface is now driven by this one collection.

Q.v. [`claude-doc.md`](claude-doc.md) for the full Claude CLI surface (`kaye-engine claude skill|plugin|marketplace|code|...`).




















## `kaye-engine export`

A generic, Claude-agnostic CLI command (alias `x`) that prints any exportable's `content()` straight to stdout, or lists every registered canonical name.

```bash
kaye-engine export coder                # print one exportable's content
kaye-engine x coder                     # same, via the short alias
kaye-engine export ls                   # list every registered canonical name, sorted
```

Structured like `kaye-engine dynamic-node`/`dn` (q.v. [`dynamic-node-doc.md`](dynamic-node-doc.md)): one flat parser, no nested sub-subcommand, with `ls` handled as a reserved positional value rather than a separate subcommand.

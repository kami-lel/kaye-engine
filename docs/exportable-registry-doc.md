# Kaye Engine: `Exportable` registry

`kaye_engine.exportable` treats everything a consumer might want exported, a `Blueprint` or an abbreviation or glossary group, as one collection, `exportable_registry`, keyed by the exact name it exports under.


































## Programmatic API

The package exports `Exportable`, `exportable_registry`, `register_exportable_entry`, `get_exportable`, `image_prompt_exportable_registry` and `register_image_prompt_exportable`.













### Exportable

`Exportable` is the abstract base class every exportable kind implements directly. `BlueprintRegistry` and `ExportableAbbr` (see [`abbrs-doc.md`](abbrs-doc.md#exportable-groups)) each subclass it, so a registry entry *is* the `Exportable`, never a copy. It is a keyword-only dataclass:

| Field | Default | Meaning |
| --- | --- | --- |
| `canonical_name` | required | kebab-case name, used directly as the exported skill name |
| `display_name` | `""` | human-readable name; an implementer may derive it, as `BlueprintRegistry` does from its blueprint's meta |
| `is_user_invokable` | `True` | a human may invoke it by name |
| `llm_invokable` | `True` | the assistant may bring it into play on its own judgment |
| `always_apply` | `False` | the entry is unconditionally relevant and always applied, rather than surfaced only when judged relevant |
| `render_profile` | `RenderProfile()` | the entry's own default render settings, merged with a caller's profile, not replaced by it |

Its one abstract method is `content(**kwargs)`, the generic, non-Claude-specific displayable content: the rendered prompt for a blueprint, or the Markdown list for an abbreviation group. A blueprint entry forwards the keyword arguments to `render_prompt()`; an abbreviation group ignores them.

The Agent Skill exporter ignores `always_apply`; the `continue` command turns it into an always-apply rule, see [`continue-doc.md`](continue-doc.md).

`Exportable` declares no `merge` or `|` contract, and none of its kinds define one. The `merge_blueprints()` function merges two `Blueprint` values, and `render_prompt()` and `preview_blueprint()` resolve `.dependencies` internally, see [`prompt-doc.md`](prompt-doc.md).













### The Registry

`exportable_registry` is the plain `dict` of `canonical_name` to `Exportable`:

- `register_exportable_entry(exportable)`: inserts the entry under its `canonical_name` and returns it; a name already registered raises `ValueError`
- `get_exportable(canonical_name)`: returns the entry; an unknown name raises `KeyError`













### Negative Prompt

The negative prompt is not a separate method. Pass a render profile with `RenderMode.NEGATIVE` to `content()` itself, see [`render-profile-doc.md`](render-profile-doc.md#negative-prompt), [`prompt-doc.md`](prompt-doc.md#generate-negative-prompt) and [`sidecar-doc.md`](sidecar-doc.md#negative-instruction-sidecar). Whether an `Exportable` kind can render one at all is the plain class attribute `supports_negative_content`: `False` by default, `True` on `BlueprintRegistry`, since only it carries a `.blueprint` to render one from. A caller that wants to handle any `Exportable` uniformly checks that flag instead of duck-typing a method, as `export-image-prompt` does.


































## Registration and Usage

Two kinds of exportable registration feed `exportable_registry`:

- [engine registered exportable](#engine-registered-exportable): registered by the engine itself, from the abbreviation data
- **consumer registered exportable**:
  - blueprint: `register_blueprint(name, blueprint)` creates a `BlueprintRegistry`, inserts it into `blueprint_registry`, and, when `is_exportable` is true (the default), into `exportable_registry` too. Its display name comes from `blueprint.meta.display_name`, with the optional `display_name=` argument as fallback, else `""`. It accepts `is_user_invokable`, `llm_invokable`, `always_apply` and `render_profile`, see [`prompt-doc.md`](prompt-doc.md#blueprint-registry)
  - glossary: `register_abbr_glossary()` registers the glossary's name and settings into `abbr_glossary_registry`; with `is_exportable=True`, its group is inserted into `exportable_registry` the next time the abbreviation groups are registered, as `glossary-NAME`. Its `is_user_invokable` flag decides whether a human may invoke that group
  - image-prompt subset: `register_image_prompt_exportable(canonical_name)` marks a name already in `exportable_registry` as a member of the image-prompt export subset, appending it to `image_prompt_exportable_registry`. It never creates an exportable itself: an unregistered `canonical_name` raises `KeyError`, and a name already in the subset raises `ValueError`

Usage:

- `exportable` CLI (alias `x`): `kaye-engine exportable EXPORTABLE` prints that exportable's `content()`, rendered with the shared render options and without the trailing comment by default, see [`render-profile-doc.md`](render-profile-doc.md#cli-options); `kaye-engine exportable ls` lists every registered exportable name, sorted alphabetically
- `export-json` CLI (alias `json`): `kaye-engine export-json` writes every entry in `exportable_registry` to a flat `{canonical_name: content}` JSON object, sorted by key and indented by 2 spaces, each `content()` rendered with `RenderProfile(sparseness=0, conditional_sidecars=("avoid",))` merged on top of the entry's own `render_profile`, see [`render-profile-doc.md`](render-profile-doc.md). `{avoid}` content is folded inline into each value. `--output-file`/`-f` sets the output path, defaulting to `exportable-as-json.json` in the current directory, and an existing file is overwritten. `--dry-run` renders every entry and reports the file without writing it
- `export-image-prompt` CLI (alias `img`): `kaye-engine export-image-prompt FOLDER` creates `FOLDER` when missing and writes every entry in `image_prompt_exportable_registry` to it, one `<canonical_name>.md` file per entry holding its `content()` rendered with `RenderProfile(sparseness=0, mode=RenderMode.IMAGE)`, where `IMAGE` itself forces `sparseness=1`, see [`render-profile-doc.md`](render-profile-doc.md#render-modes). Wherever an entry has `supports_negative_content` set and its negative render has real content, a `<canonical_name>-AVOID.md` sibling is written too, rendered as `NEGATIVE | IMAGE`, i.e. bare `{avoid}` content with no title lines. The positive file never carries `{avoid}` content. `--dry-run` writes nothing
- `continue` CLI (alias `c`): `kaye-engine continue [FOLDER]` writes every entry as a Continue rule or prompt, see [`continue-doc.md`](continue-doc.md)
- `skill` CLI (alias `s`): `kaye-engine skill NAME... FOLDER` exports the named exportables as Agent Skills into `FOLDER`, and `kaye-engine skill --all FOLDER` (`-a`) exports every one. `FOLDER` is required, `-z` makes one `.zip` per skill, and an unknown name aborts before anything is written. A blueprint skill takes its description, when-to-use and globs from the blueprint's meta, and an abbreviation group takes its display name as the description. The skill writers live in `kaye_engine.skill`, independent of any one agent product
- `claude` CLI: see [`claude-doc.md`](claude-doc.md) for the full Claude CLI surface (`kaye-engine claude plugin|marketplace|code|...`); `kaye-engine claude skills` exports every exportable as Agent Skills into `~/.claude/skills`


































## Engine Registered Exportable

The engine registers abbreviation groups from `get_abbr_data()`, as `ExportableAbbr` entries defined in `kaye_engine/cli/exportable_abbr.py`. `populate_abbr_data_with_json_file()` calls `register_exportable_abbrs()` itself, which recomputes every group fresh and re-inserts each, replacing any earlier entry under the same name. Call it yourself only after adding entries by hand with `add_entry`. While the abbreviation data is empty, no group is registered.

Every engine group is llm-only: `is_user_invokable` is `False` and `llm_invokable` is `True`. A glossary group is the one exception, following its glossary's own flag.

Abbreviation Group by Tag:

| canonical name | display name |
| --- | --- |
| `abbr-single-character` | Abbr Single Character |
| `abbr-emoji` | Abbr Emoji |

Abbreviation Group by Wrap:

| canonical name | display name |
| --- | --- |
| `abbr-prefixes` | Abbr Prefixes |
| `abbr-suffixes` | Abbr Suffixes |
| `abbr-symbols` | Abbr Symbols |

Abbreviation *Starts-With*:

| canonical name | display name |
| --- | --- |
| `abbr-starts-with-digits-0-9` | Abbr Starts with Digits 0~9 |
| `abbr-starts-with-a` to `abbr-starts-with-z` | Abbr Starts with A to Abbr Starts with Z, one per letter |
| `abbr-starts-with-non-alphanumeric` | Abbr Starts with Non-Alphanumeric |

Abbreviation Group by Glossary, one per glossary registered with `is_exportable=True`:

| canonical name | display name |
| --- | --- |
| `glossary-NAME` | Glossary NAME |

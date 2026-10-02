# Kaye Engine: `Exportable` registry

<!-- FIXME mpv doc exportable  -->

`exportable` treats everything a consumer might want exported — a `Blueprint`, an abbreviation/glossary group — as one collection, `exportable_registry`, keyed by the exact name it exports under.













## Programmatic API

`Exportable` is the abstract base class every exportable kind implements directly — `BlueprintRegistry` and `ExportableAbbr` (q.v. [`abbrs-doc.md`](abbrs-doc.md)) each subclass it, so a registry entry *is* the `Exportable`, never a copy. `exportable_registry` is the plain `dict`, `canonical_name -> Exportable`, populated via `register_exportable_entry` and read via `get_exportable`.

`register_blueprint` creates a `BlueprintRegistry` (adding `blueprint` and `is_exportable`) and inserts it into `blueprint_registry`, plus `exportable_registry` when `is_exportable`; `get_blueprint` looks it back up. `register_exportable_abbrs` recomputes every abbr/glossary group fresh and (re-)inserts each into `exportable_registry` — unlike blueprints, these must be re-run whenever `AbbrData` changes.

Every `Exportable` carries three export-policy flags: `is_user_invokable` (default `True`; a human may invoke it by name), `llm_invokable` (default `True`; the assistant may bring it into play on its own judgment), and `always_apply` (default `False`; the entry is unconditionally relevant and always applied rather than surfaced only when judged relevant). `register_blueprint` accepts all three; abbreviation groups keep the defaults except `is_user_invokable=False`. The Agent Skill exporter ignores `always_apply`; the `continue` command turns it into an always-apply rule (q.v. [`continue-doc.md`](continue-doc.md)).

`Exportable` declares no `merge`/`|` contract, and none of its kinds define one — `BlueprintRegistry.merge()` was removed; the `merge_blueprints()` function (q.v. [`prompt-doc.md`](prompt-doc.md)) merges two `Blueprint` values, and `render_prompt()`/`preview_blueprint()` resolve `.dependencies` internally, not something the registry entry itself exposes.

The negative prompt is no longer a separate method: pass a render profile with `RenderMode.NEGATIVE` to `content()` itself (q.v. [`render-profile-doc.md`](render-profile-doc.md#negative-prompt), [`prompt-doc.md`](prompt-doc.md#generate-negative-prompt) and [`sidecar-node-doc.md`](sidecar-node-doc.md#negative-instruction-sidecar)). Whether an `Exportable` kind can render one at all is the plain class attribute `supports_negative_content` (`False` by default, `True` on `BlueprintRegistry` — only it carries a `.blueprint` to render one from); a caller that wants to handle any `Exportable` uniformly checks that flag instead of duck-typing a method, as `export-image-prompt` does.













## Registration and Usage

Two kinds of exportable registration feed `exportable_registry`:

- [engine registered exportable](#engine-registered-exportable):
  always registered, by the engine;
  generate during runtime, all abbrs later added will also be rendered

- **consumer registered exportable**

  - blueprint: `register_blueprint(name, blueprint)`
    will automatically register the blueprint into `exportable_registry`;
    its display name comes from `blueprint.meta.display_name`, with the
    optional `display_name=` argument as fallback, else `""`
  - glossary: `register_abbr_glossary()` registers the glossary's name
    and settings into `abbr_glossary_registry`; `register_exportable_abbrs()`
    (re-run whenever `AbbrData` changes) is what actually inserts the
    glossary's group into `exportable_registry`
  - image-prompt subset: `register_image_prompt_exportable(canonical_name)` marks
    a name already sitting in `exportable_registry` as a member of the
    image-prompt export subset, appending it to `image_prompt_exportable_registry`.
    It never creates or registers an exportable itself: an unregistered
    `canonical_name` raises `KeyError`, and a name already in the subset
    raises `ValueError`.

Usage:

- `exportable` CLI (alias `x`): `kaye-engine exportable EXPORTABLE` prints that exportable's `content()`; `kaye-engine exportable ls` lists every registered exportable name, sorted alphabetically
- `export-json` CLI (alias `json`): `kaye-engine export-json` writes every entry in `exportable_registry` to a flat `{canonical_name: content}` JSON object, each `content()` rendered with `RenderProfile(sparseness=0, conditional_sidecars=("avoid",))` merged on top of the entry's own `render_profile` (q.v. [`render-profile-doc.md`](render-profile-doc.md)); `--output-file`/`-f` sets the output path, defaulting to `exportable-as-json.json` in the current directory. Run `kaye-engine export-json -h` for the full command help
- `export-image-prompt` CLI (alias `img`): `kaye-engine export-image-prompt FOLDER` writes every entry in `image_prompt_exportable_registry` to `FOLDER`, one `<canonical_name>.md` file per entry holding its `content()` (`RenderProfile(sparseness=0, mode=RenderMode.IMAGE)`, where `IMAGE` itself forces `sparseness=1`; q.v. [`render-profile-doc.md`](render-profile-doc.md#render-modes)), plus a `<canonical_name>-AVOID.md` sibling wherever `content(profile=... RenderMode.NEGATIVE)` renders real content for an entry with `supports_negative_content` set — so the positive field never carries `{avoid}` content; that goes to the sibling file instead, rendered as `NEGATIVE | IMAGE`, i.e. bare `{avoid}` content with no title lines
- `continue` CLI (alias `c`): `kaye-engine continue [FOLDER]` writes every entry as a Continue rule or prompt; q.v. [`continue-doc.md`](continue-doc.md)
- `skill` CLI (alias `s`): `kaye-engine skill NAME... FOLDER` exports the named exportables as Agent Skills into `FOLDER`, `kaye-engine skill --all FOLDER` exports every one; FOLDER is required, `-z` makes one `.zip` per skill, and an unknown name aborts before anything is written. The skill writers live in `kaye_engine.skill`, independent of any one agent product
- `claude` CLI: q.v. [`claude-doc.md`](claude-doc.md) for the full Claude CLI surface (`kaye-engine claude plugin|marketplace|code|...`); `kaye-engine claude skills` exports every exportable as Agent Skills into `~/.claude/skills`













## Engine Registered Exportable

Abbreviation Group by Tag:

| canonical name | display name | is_user_invokable | llm_invokable |
| --- | --- | --- | --- |
| `abbr-single-character` | Abbr Single Character | ❌ | ✔️ |
| `abbr-emoji` | Abbr Emoji | ❌ | ✔️ |

Abbreviation Group by Wrap:

| canonical name | display name | is_user_invokable | llm_invokable |
| --- | --- | --- | --- |
| `abbr-prefixes` | Abbr Prefixes | ❌ | ✔️ |
| `abbr-suffixes` | Abbr Suffixes | ❌ | ✔️ |
| `abbr-symbols` | Abbr Symbols | ❌ | ✔️ |

Abbreviation *Starts-With*:

| canonical name | display name | is_user_invokable | llm_invokable |
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

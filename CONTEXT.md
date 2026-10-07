# kaye-engine CONTEXT

**Last updated:** 2026-10-06

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
| CLI subcommands | `blueprint`, `claude`, `continue`, `hermes`, `export-image-prompt`, `dynamic-node`, `dynamic-substitution`, `exportable`, `export-json`, `affordance`, `variant`, `glossary`, `skill`, `sync-open-webui-skills` |

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
| **Prompt Corpus** | a structured Markdown document (one file, or several sources concatenated by `load_corpus_tree`); a process holds one; the authoritative source of truth |
| **Prompt Tree** | the parsed corpus; every heading a `BasePromptNode` |
| **Blueprint** | a frozen value (`Blueprint`) recording which tree nodes render, by path (`nodes`, `subtrees`), plus `meta` and `dependencies`; pure data, edited only through functions that return a new one |
| **Corpus Index** | `CorpusIndex`, derived once per process from the one loaded tree: pre-order node arrays, paths, depths, child indexes, subtree and sidecar masks, static content blocks |
| **Blueprint Selection** | `BlueprintSelection`, a blueprint bound to the index as one bitmask; what the renderers walk |
| **Blueprint Registry** | name → blueprint plus its export policy |
| **Exportable** | common base for anything `exportable_registry` holds — `BlueprintRegistry` and `ExportableAbbr` are its two implementers |
| **Role** | a task-specific behavior profile held inside the corpus |
| **Sidecar Node** | a `{name}` subnode; metadata or conditional content |
| **Dynamic Node** | a `(name)` node (canonical kebab-case `NAME`) whose content is generated at render |
| **Dynamic Substitution** | a directly-registered `DynamicSubstitution` held in `dynamic_substitution_registry`, resolved by a `(((name)))` placeholder ahead of the dynamic-node/glossary universe |
| **Affordance** | a conceptual capability family, tracked in `affordance_registry`; auto-created on first `register_variant()` call naming it |
| **Variant** | one concrete implementation of an affordance, tracked in `variant_registry` via `register_variant(canonical_name, affordance_name)` |
| **RenderProfile** | a `kw_only` dataclass bundling render settings (`conditional_sidecars`, `variants`, `sparseness`, ...); `.merge()` overrides scalar fields and unions the collection fields |
| **Image-Prompt Export Subset** | `image_prompt_exportable_registry`, a list of `exportable_registry` canonical names opted into image-prompt export via `register_image_prompt_exportable(canonical_name)` |

Heading syntax carries node type: plain text is an ordinary corpus node,
`{braces}` a sidecar, `(parentheses)` a dynamic node.

```
sources ────load_corpus_tree()──> Prompt Tree ──> CorpusIndex ─┐
                                                                ├─render_prompt()─> text
blueprint text ──parse_blueprint_tree()──> Blueprint ───────────┘
```

The process holds exactly one corpus tree: `load_corpus_tree(sources)`
raises `ValueError` on a second call, `get_corpus_tree()` raises before a
load, and `clear_corpus_tree()` drops the tree together with everything
derived from it (the `CorpusIndex`, bound selections) through clear hooks.

`render_prompt()`/`preview_blueprint()` are the dependency-resolving
entry points: each first resolves the blueprint's selection with the full
transitive closure of its `.dependencies` (`resolve_selection()`, a bitmask
OR, so a diamond dependency converges without duplicating shared content),
then delegates to the own-content-only `render_prompt_without_dependencies()`/
`preview_blueprint_without_dependencies()` below. A `dependencies` entry
may be a `Blueprint` value or a `str`; each `str` is resolved to the
blueprint registered under that name at render time (late binding), and
`register_blueprint()` validates every name at registration. A cycle or
unknown name raises `ValueError`.

Rendering takes a `sparseness` parameter governing how runs of blank lines
collapse in the output, from `-1` (whole output joined onto one line) through
`99` (no trimming); descriptor sidecar rendering always renders at `-1` so a
multi-line description or when-to-use collapses to one string. Blank lines
inside a fenced code block are exempt from collapsing everywhere fenced
content might get compressed, via the shared `compute_fenced_line_mask`
(`kaye_engine/prompt/md_fence.py`) that `apply_sparseness`, the corpus-tree
heading parser (`_split_sections` in `prompt_corpus_node.py`), and the
load-time blank-line cleanup in `load_corpus_tree`
(`_collapse_unfenced_blank_runs` in `prompt_corpus_loader.py`) all rely on
to stay out of fenced regions.
`render_prompt()` applies `sparseness` last: it renders
the tree unsparse, then `apply_dynamic_substitutions()`, then applies the
caller's `sparseness` to the substituted result, so a substitution's own
blank lines are shaped by the same policy. Because that unsparse render
hides the real `sparseness`, the generated-by comment's compact form
(one `↵`-joined line iff `sparseness == -1`) travels as an explicit
`is_comment_compact` keyword to the line renderers. The comment
(`render/comment.py`) is default lines (`blueprint: NAME` when
`display_name` is set, then `Kaye Engine vX`) plus client lines from
`register_comment_line()`, and is appended after image-mode heading
flattening. `BlueprintRegistry.content()` fills an empty `display_name`
from the entry's own, which `BlueprintRegistry` reads live from
`blueprint.meta.display_name`, else its explicit fallback, else `""`.

Sidecars split by usage rather than by class. *Descriptor* sidecars
(`{description}`, `{when_to_use}`, `{globs}`) are consumed as blueprint
metadata and never rendered; every other name is a *conditional* sidecar,
real content spliced in only when its name is on a `RenderProfile`'s
`conditional_sidecars`, or matched via that same profile's `variants`
field against `variant_registry`. `{avoid}` (negative-instruction/example
content) is neither: it carries no `BlueprintMeta` field and is never
manually spliced by name, but is discovered automatically, at any depth,
by `render.render_negative_prompt_lines()`, reached via the single
`RenderMode`-driven entry point — `RenderProfile(mode=RenderMode.NEGATIVE)`
passed to `render_prompt()`/`render_prompt_without_dependencies()` (or
merged into a caller's profile) picks it in place of the positive
`render_prompt_lines()`, at every layer: the render functions,
`BlueprintRegistry.content()`, and any other `Exportable.content()`.
A node's own `{avoid}` child contributes only when that node itself is
checkmarked, under its own heading (never the literal `{avoid}`
heading); descendants are always walked regardless of an ancestor's
own checkmark, so a checkmarked descendant several levels below an
unchecked ancestor still contributes. A node with no `{avoid}` content
of its own is transparent: its contributing descendants' rendered
blocks splice in directly, with no heading of this node's own, even
though the node is checkmarked and the walk still visits it. A branch
with no `{avoid}` content anywhere in it is omitted entirely. A 3rd
`RenderMode` member, `POST_ORDER`, reorders every
subtree to children-before-parent — each child's full subtree first
(recursively, same rule), siblings kept in their original relative
order, then the node's own heading and content last — with no other
change (`sparseness` and heading markdown are untouched). A 4th member,
`REVERSE_ORDER`, reverses sibling order at every level of the walk
instead (independent of `POST_ORDER`; wired into all 4 walk paths
`render_prompt_lines`/`render_negative_prompt_lines` can take — plain
pre-order and `POST_ORDER`, positive and negative). `IMAGE` is a
*composite* built from `POST_ORDER` | `REVERSE_ORDER` plus a private
flatten-heading flag (`IMAGE = POST_ORDER | REVERSE_ORDER | _IMAGE`,
mirroring the `WORD_CHARACTER`/`ASCII` composite pattern in
`AbbrTags`): it flattens every heading line to a
bare `title:` (regardless of nesting depth), forces `sparseness=1`, and
(via the bits it carries) also reorders to post-order with reversed
siblings. Every
`RenderMode` member composes freely (`RenderMode.NEGATIVE |
RenderMode.POST_ORDER`, `RenderMode.NEGATIVE | RenderMode.IMAGE`, ...).
`NEGATIVE | IMAGE` alone prints no title at any depth — only `{avoid}`
content remains, blocks still blank-line separated
(`render_negative_prompt_lines()` passes `is_title_shown=False` to its
recursive helpers).
`Exportable.supports_negative_content` (class
attribute, `False` by default, `True` on `BlueprintRegistry`) is the
explicit capability flag `export-image-prompt`'s `_avoid_content()` checks
before calling `content(profile=... RenderMode.NEGATIVE)` to build each
`<canonical_name>-AVOID.md` sibling. Q.v. [sidecar node
documentation](docs/sidecar-doc.md).

`affordance_registry`/`variant_registry` form a two-level model: an
`Affordance` is a conceptual capability family, a `Variant` one concrete
implementation of it, registered via the single `register_variant
(canonical_name, affordance_name)` entry point (auto-creating its
affordance on first use). Each variant derives its own `[{name}] Usage`
sidecar (checkmarked when that variant is present) plus a mirror
`[{name}] Lack` sidecar (checkmarked when it is absent); each affordance
derives its own `[{name}] Usage` sidecar (checkmarked when at least one
of its registered variants is present) plus a `[{name}] Fallback`
sidecar, checkmarked when every variant registered under that affordance
is absent (and the affordance has ≥1 registered variant). Q.v.
[affordance documentation](docs/sidecar-doc.md#affordance). A Kaye-specific,
consumer-supplied
`surface_profiles` dict (`dict[str, RenderProfile]`, passed to
`setup_claude_cli(...)` — kaye-vault owns the actual Claude surface data,
q.v. `kaye_vault/claude_render_profiles.py`) maps a surface name to the
`RenderProfile` carrying that surface's variants/conditional-sidecars.
Every **rendering command** (see `AGENTS.md` for the list and flags) shares
one parent parser and one aux function,
`build_render_profile_parent_parser`/`resolve_render_profile`
(`kaye_engine/cli/render_profile_parser.py`). `resolve_render_profile`
returns one `RenderProfile`, merging each selected surface's profile with one
built from the explicit flags via `RenderProfile.merge()`.
`--variant`/`--conditional-sidecar` union additively with what `--surface`
derives; `--reverse-order` ORs `RenderMode.REVERSE_ORDER` into the profile's
`mode` before the final merge, because `mode` is a scalar field the merge
would otherwise let clobber (the pattern `_avoid_content()` in
`export_image_prompt_parser.py` uses for `NEGATIVE | IMAGE`). `--surface`
keys into the consumer-supplied `surface_profiles` dict
(`dict[str, RenderProfile]`, passed to `setup_claude_cli(...)`) and is
omitted from the parser when none is configured. An omitted flag keeps the
subcommand's own `--comment` and `--sparseness` default
(`build_sparseness_parent_parser(default=...)`). The resolved profile
travels as one `profile=` object through every `claude` export chain and the
top-level `skill`. A default `RenderProfile()` carries
`variants=None`/`conditional_sidecars=()`, a no-op under `merge()`, so a
`register_blueprint()` entry's own `render_profile` still applies:
`BlueprintRegistry.content()` merges it via
`self.render_profile.merge(profile)`. Q.v. [Claude
documentation](docs/claude-doc.md) and [sidecar node
documentation](docs/sidecar-doc.md).

### CLI Flag Surface

Several subcommands print rendered or registry content without the
render-profile options: `export-json` and `export-image-prompt` use a
hardcoded `RenderProfile`; `dynamic-substitution` and `glossary` print raw
registry content; `sync-open-webui-skills` renders per skill with no exposed
profile; `affordance`/`variant` are list-only.

`blueprint preview` is the one asymmetric case inside the rendering set:
it pulls only `build_comment_parent_parser()` out of the bundle (its
own `-c`/`--comment`, `-C`/`--no-comment`), plus its own
`-l/--preview-line-count`, `-w/--preview-line-width`,
`-t/--show-full-tree` — no `--surface`/`--variant`/`--sparseness`,
since it renders a preview tree, not a prompt.

`-z/--zip` is genuinely shared behavior (`claude plugin`, `claude skills`,
`skill`) but
is hand-duplicated per parser rather than pulled into its own builder,
unlike the render-profile options. `-n` means `--dry-run` on every
write command; `claude plugin` spells `--no-version` as `-N`.

`--dry-run` on the write commands comes from `cli/dry_run.py`: a shared
`-n/--dry-run` parent parser, plus a run-wide switch (`enable_dry_run()`,
`is_dry_run()`) that also stamps the `dry` badge on the five engine
loggers. Writers keep their deed lines (`kaye_engine/deed.py`, a local stand-in for
the deed feature kamilog 3.0 removed) and skip only the filesystem call
under `is_dry_run()`; the zip exports skip the temporary build and log
the pack and move deeds directly. `sync-open-webui-skills` keeps its own
`-n`/`--dry-run` and threads `is_dry_run` as a parameter instead.

Dynamic nodes auto-attach to every tree at load time — no authored
heading required for existence — and cover today's date plus the
abbreviation glossaries; an authored `(name)` heading, at any depth,
fixes the node's preface and tree location in place of the heading
itself, else it falls back to a direct child of root. A second,
independent mechanism, inline `(((name)))` substitution, resolves
canonical names anywhere inside rendered prompt text at
`render_prompt_without_dependencies()` (and, transitively,
`render_prompt()`) time, against two sources in order: first
`dynamic_substitution_registry` (populated via
`register_dynamic_substitution(name, substitution)`, where
`substitution` is a `DynamicSubstitution` — commonly
`StringDynamicSubstitution` wrapping a fixed string), then
`resolve_dynamic_node_factory(name, require_substitution_flag=True)`,
the same dynamic-node universe the tree mechanism draws on but with
glossary names admitted only when `register_abbr_glossary(name, ...,
is_dyn_substitution=True)` opted in — the tree mechanism
itself resolves glossary names unconditionally, since the opt-in gate
applies to placeholder substitution only. Q.v. [dynamic node
documentation](docs/dynamic-content-doc.md) and [abbreviation
collection documentation](docs/abbrs-doc.md).

## Public API

```python
from kaye_engine import (
    PACKAGE_NAME, LOGGER_NAME,
    load_corpus_tree,
    AbbrData,
    DynamicSubstitution, StringDynamicSubstitution,
    register_abbr_glossary,
    register_blueprint,
    register_comment_line,
    register_consumer,
    register_dynamic_substitution,
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
call `register_consumer(display_name, canonical_name, version)` and
`setup_claude_cli(chat_exportable_name, merged_coder_exportable_name)` — none
has a default; `display_name` is stamped into `plugin.json`, and the kebab
`canonical_name` doubles as plugin, marketplace, and marketplace folder
name. Q.v. [Kaye Engine: `prompt` module
Documentation](docs/prompt-doc.md).

Every CLI subcommand entrypoint calls a setup guard
(`check_corpus_setup_for_cli()`, or `check_setup_for_claude_cli()` for
`claude` subcommands) that logs an error — never raises — when a consumer
hasn't loaded a default corpus tree or registered any blueprints. It exists
to surface a bare-checkout misuse early, not to enforce the boundary. The
consumer identity and the Chat/Coder blueprint names are enforced
separately, each by its own getter (`get_consumer_display_name()`,
`get_consumer_canonical_name()`, `get_consumer_version()`,
`get_claude_chat_exportable()`, `get_claude_merged_coder_exportable()`; the
plugin, marketplace, and marketplace folder getters `get_plugin_name()`,
`get_marketplace_name()`, `get_marketplace_folder_name()` return the canonical
name), which logs `logger.critical` and raises
`SystemExit(1)` when unset — or, for the blueprint getters, when the
configured name is not in `blueprint_registry` — rather than letting `None`
or an unresolved name reach path, manifest, or prompt building.

## Blueprint API Verbs

Every blueprint function takes exactly one input type and returns exactly
one output type: no format sniffing, no union inputs, no mode flag that
changes the output type. A verb names one kind of operation everywhere:

| verb | meaning | functions |
|---|---|---|
| parse | text → `Blueprint` | `parse_blueprint_tree`, `parse_blueprint_json` |
| decode / encode | dict ↔ `Blueprint` | `decode_blueprint`, `encode_blueprint` |
| load / save | JSON file ↔ `Blueprint` | `load_blueprint`, `save_blueprint` |
| dump | `Blueprint` → JSON text | `dump_blueprint` |
| validate | same `Blueprint`, or `ValueError` | `validate_blueprint` |
| resolve / trace | direct / transitive dependencies as values | `resolve_dependencies`, `trace_dependencies` |
| merge / diff | two blueprints → one / their node difference | `merge_blueprints`, `diff_blueprints` |
| show | read one field or a summary | `show_blueprint`, `show_description`, `show_when_to_use`, `show_description_and_when_to_use`, `show_globs`, `show_dependencies` |
| preview | preview tree | `preview_blueprint`, `preview_blueprint_without_dependencies`, `preview_selection` |
| render | prompt | `render_prompt`, `render_prompt_without_dependencies` |

The CLI (`kaye_engine/cli/blueprint/`) only composes these. Format
detection (JSON when the first non-blank character is `{`, otherwise a
preview tree) lives in `aux_input.py`, never in the API; a registered name
renders through its registry entry (`BlueprintRegistry.resolve_profile()`),
a blueprint read from stdin renders plain. `run_cmd` turns a `ValueError`,
`KeyError`, or `FileNotFoundError` into one critical log line and exit
code 1.

## Repository Layout

```
kaye_engine/
├── prompt/              parse, model, select, render
│   ├── blueprint/       Blueprint value (data/edit/parser), CorpusIndex
│   │                    (index), selection binding, registry, rendering
│   │   ├── render_mode.py      RenderMode: NORMAL/NEGATIVE/POST_ORDER/
│   │   │                        REVERSE_ORDER/IMAGE flag enum
│   │   ├── render_profile.py   RenderProfile: layerable render-kwargs bundle
│   │   └── render/             render_*_lines()/preview_selection(),
│   │       split by concern (tree/lines/sidecar_splice/util)
│   ├── dynamic_nodes/   render-time generated node types
│   └── affordance_registry.py  Affordance/Variant two-level registry,
│                                Usage/Lack/Fallback sidecar names
├── abbr_collection/     abbreviation entries, store, JSON loader
├── consumer.py          register_consumer: display name, canonical name,
│                        version; getters read by claude and hermes
├── deed.py              track(logger): fixed-wording file/dir action lines
├── exportable/           Exportable base, exportable_registry
│   └── image_prompt_export.py  image_prompt_exportable_registry,
│                            register_image_prompt_exportable
├── skill/               Agent Skills standard, agent-neutral: `Skill`
│                        document, folder/.zip writers, `select_exportables`
├── cli/
│   ├── blueprint/       `blueprint`/`bp` subcommand: list, preview, render,
│   │                    validate, show; `aux_input.py`/`aux_output.py`
│   │                    hold the glue (stdin, format detection, formatting)
│   ├── claude/          plugins, marketplaces, CLAUDE.md
│   │   ├── setup.py               setup_claude_cli(...); registers
│   │   │                          consumer-supplied affordance_groups,
│   │   │                          stores surface_profiles
│   │   ├── skills/                `claude skills`/`claude s`: every skill
│   │   │                          into ~/.claude/skills (`-z` for .zips)
│   │   └── surface_parser.py      shared `--surface` parent parser --
│   │                              choices from consumer's surface_profiles
│   ├── skill/           `skill`/`s` subcommand: named Agent Skills into a
│   │                    required FOLDER (`--all` for every one)
│   ├── continue_ai/    `continue`/`c` subcommand: rules/ + prompts/ for Continue
│   │   ├── rule_md.py       ContinueRule frontmatter doc + factory
│   │   ├── export_rules.py  classify_exportable, export_continue_folder
│   │   └── parser.py        parser + handler
│   ├── hermes/          `hermes`/`m` subcommand: a Hermes home directory
│   │   ├── setup.py     setup_hermes_cli + getters (consumer configuration)
│   │   ├── export.py    export_hermes_folder: SOUL.md files + skills/
│   │   └── parser.py    parser + handler
│   ├── open_webui/      `sync-open-webui-skills`/`o` subcommand: push
│   │   │                exportables into Open WebUI as skills
│   │   ├── skill_form.py  build_skill_form: Exportable -> SkillForm dict
│   │   ├── client.py      urllib client + OpenWebUIError
│   │   ├── plan.py        plan_skill_sync: create/update/skip/prune
│   │   ├── sync.py        sync_skills executor + SyncSummary
│   │   └── parser.py      parser + handler
│   ├── dynamic_node/    `dynamic-node`/`dn` subcommand: multi-node render
│   ├── dynamic_substitution_parser.py  `dynamic-substitution`/`ds`
│   │                                    subcommand: print/list
│   │                                    dynamic_substitution_registry
│   ├── list_affordance_parser.py  `affordance`/`afd` subcommand: list affordance_registry
│   ├── list_variant_parser.py     `variant`/`var` subcommand: list variant_registry
│   ├── glossary_parser.py    `glossary`/`g` subcommand: print/list glossaries
│   ├── comment_parser.py     shared `--comment`/`--no-comment` parent parser
│   ├── render_profile_parser.py  shared 6-option parent parser + aux fn
│   ├── exportable_parser.py  `exportable`/`x` subcommand: print, list exportables
│   ├── exportable_as_json_parser.py  `export-json`/`json`
│   │                                  subcommand: export
│   │                                  exportable_registry as flat JSON
│   └── export_image_prompt_parser.py  `export-image-prompt`/`img` subcommand:
│                                    write the image-prompt subset as
│                                    `<name>.md`/`<name>-AVOID.md` pairs
docs/                    per-topic reference, linked above
tests/                   prompt/, abbr/, cli/ — mirrors the source
```

The `prompt` layer is pure: it knows nothing of Claude or any export
target. Every export target is a leaf under `cli/`, and each reads
the same `blueprint_registry` rather than holding its own list.

`continue` reads `exportable_registry` and classifies each entry by its
export-policy flags: `always_apply` forces a rule (`alwaysApply: true`),
otherwise `llm_invokable` gives a rule, `is_user_invokable` alone gives an
invokable prompt, and an entry with neither is skipped. Files are named
`<canonical_name>.md` under `rules/` or `prompts/`. The `--surface` flag
has no default there.

`hermes` is configured through `register_consumer(...)` and
`setup_hermes_cli(...)`, which checks every name against
`blueprint_registry` and exits 1 on an unknown one. It renders the soul and
profile blueprints from `blueprint_registry` (so non-exportable entries work)
into `SOUL.md` and `profiles/<name>/SOUL.md`, and delegates `skills/<canonical name>/`
to `export_skills_as_folders`, which only ever sees `exportable_registry`.
The skill version comes from `register_consumer`. Comments are hidden by default.

## Testing Strategy

`pytest`, run **serially by design** — cases are cheap in-process
assertions, so worker startup costs more than a split saves, and shared
fixtures carry run-order assumptions. `pytest-xdist` is deliberately absent
from the `dev` extra.

Tests mirror the source tree: `tests/prompt/` for the engine, `tests/abbr/`
for the abbreviation collection. `tests/cli/` stays deliberately thin — it
holds only the corpus-independent pieces (setup guard, exportable-abbr
registration, `dynamic-node` parsing, `SKILL.md` rendering, the Open WebUI sync with a
fake client, the deed lines of the zip exports, manifests, and
`FrontmatterDoc.write` (`tests/deed_test.py` covers the helper)), because the
exporters need a corpus to produce output and the consumer package covers
those.

## Maintaining This File

Update `CONTEXT.md` in the same change as the architecture change, and
refresh `Last updated` whenever content changes. Revisit it when entities or
node types are added, when a boundary moves, when the public API changes, or
when the test layout shifts.

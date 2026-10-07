# Kaye Engine: Abbreviations Documentation

`kaye_engine.abbr_collection` is the package that deals with **abbreviations**: the entry data structures, the store, the glossary registry, and the loader that populates the store from an `abbrs.json` file.

`kaye_engine` bundles no abbreviation database. A consumer package supplies the JSON file and registers its glossaries.

Every abbreviation-related *dynamic node* reads through this store rather than parsing the file or holding its own copy of the data. The same store also feeds the exportable abbreviation groups, see [Exportable Groups](#exportable-groups).


































## `abbr_collection` module

The package exports `AbbrData`, `AbbrEntry`, `AbbrMeaning`, `AbbrTags`, `AbbrWrap`, `AbbrGlossaryRegistry`, `abbr_glossary_registry`, `get_abbr_data`, `get_abbr_glossary`, `populate_abbr_data_with_json_file` and `register_abbr_glossary`. The `kaye_engine` package itself re-exports `AbbrData`, `populate_abbr_data_with_json_file` and `register_abbr_glossary`.













### `get_abbr_data()`

Return the single, always-present `AbbrData` singleton. It may still be empty: test it with `bool(get_abbr_data())`.

```python
from kaye_engine.abbr_collection import get_abbr_data

data = get_abbr_data()
for entry in data.abbrs:
    print(entry.as_md_list_entry())
```

An `AbbrData` holds:

- `.abbrs`: every `AbbrEntry`, in insertion order
- `.meanings`: every distinct `AbbrMeaning`
- `.automaton`: an Aho-Corasick automaton over the lower-cased abbreviations, used to scan a query





#### adding entries by hand

To add entries directly, open the singleton as a context manager and call `add_entry` for each one:

```python
from kaye_engine.abbr_collection import get_abbr_data, AbbrMeaning

data = get_abbr_data()
with data:
    mean = AbbrMeaning("for example", remark=None)
    data.add_entry(mean, "e.g.", {"priority": 5, "tags": [], "wrap": "word"})
```

`add_entry` raises `ValueError` for a malformed entry, for an entry duplicating one already added (same abbreviation and meaning), and for an entry whose `tags` name a glossary that was never registered.

> [!IMPORTANT]
> The `with` block matters: entries added inside it are not searchable until the block exits cleanly, since that is when the lookup automaton is rebuilt. A block that exits with an exception does not rebuild it.





#### `populate_abbr_data_with_json_file(file_path)`

Parse a `.json` file and add every entry it contains into `get_abbr_data()`.

```python
from kaye_engine.abbr_collection import populate_abbr_data_with_json_file

populate_abbr_data_with_json_file("abbrs.json")
```

The automaton is rebuilt once, after the whole file is applied. The function then re-registers every exportable abbreviation group, so callers need not do that themselves, see [Exportable Groups](#exportable-groups). See [entries `json` file schema](#entries-json-file-schema) for the file's format.

The function raises `json.JSONDecodeError` for malformed JSON, `TypeError` when a meaning or `abbrs` value is not an object, and `ValueError` for a meaning without `abbrs`, a malformed entry, or a duplicate entry.

> [!IMPORTANT]
> Every glossary name any entry's `tags` array uses (any item that is not a fixed `AbbrTags` value) must already be registered via `register_abbr_glossary` before that entry is added. Otherwise `add_entry` and `populate_abbr_data_with_json_file` raise `ValueError`.





#### `register_abbr_glossary(name, is_exportable, ...)`

Register a glossary name so entries may reference it via `tags`, and set that glossary's default rendering behavior for its `GlossaryNode`:

- `name`: the canonical glossary name, as it appears in an entry's `tags` and in the `(name)` corpus heading
- `is_exportable`: whether this glossary's group is inserted into `exportable_registry`, see [`exportable-registry-doc.md`](exportable-registry-doc.md)
- `is_user_invokable`: whether a human may deliberately invoke this glossary's exportable group directly, such as a skill; unlike the engine's fixed tag, wrap and starts-with groups, which are always llm-only, this is configurable per glossary; defaults to `True`
- `is_numbered_list`: render entries with numbered markers (`"1. ..."`) instead of bullets (`"- ..."`); defaults to `False`
- `is_sorted`: render entries ordered by ascending `priority` instead of insertion order; defaults to `False`
- `is_remark_disabled`: omit the `(...)` remark suffix from every entry in this glossary by default; defaults to `False`
- `is_term_definition_forced`: render every entry as a term definition (the meaning alone, no `abbr:` prefix), regardless of whether it carries the `term_definition` tag; defaults to `False`
- `is_dyn_substitution`: whether the glossary is reachable as a `(((name)))` dynamic substitution placeholder, see [Dynamic Substitution](dynamic-content-doc.md#dynamic-substitution); defaults to `False`

```python
from kaye_engine.abbr_collection import register_abbr_glossary

register_abbr_glossary("coding-terms", True)
register_abbr_glossary(
    "plan-step-by-step-abbr", True, is_numbered_list=True, is_sorted=True
)
```

It returns the created `AbbrGlossaryRegistry` entry, and raises `ValueError` if `name` is already registered. `abbr_glossary_registry` is the dictionary of every entry, and `get_abbr_glossary(name)` retrieves one, raising `KeyError` for an unknown name.

The four rendering flags are also render-time overrides, see [`GlossaryNode`](#abbreviation-dynamic-nodes).

Priority-based filtering is not a registration concern. The caller supplies it at generation time through `glossary_priority_threshold`.

> [!NOTE]
> `glossary_priority_threshold` only filters rendering. An entry whose `priority` exceeds the threshold is still added to `AbbrData`: its glossary membership is still validated, and it is still findable through `get_abbr_data()`. It simply never appears in a rendered `GlossaryNode`.


































## Abbreviation Dynamic Nodes

Every abbreviation-related [dynamic node](dynamic-content-doc.md) lives in `kaye_engine/prompt/dynamic_nodes/` and reads through `get_abbr_data()`. All of them log an error and render no entries while the store is empty.

| Node | Heading | Source | Behavior |
| --- | --- | --- | --- |
| `DecodeOnlyAbbrNode` | `(decode-only-abbr)` | `decode_only_abbr_node.py` | scans a `query=` string against `get_abbr_data().automaton`, verifying each raw match with `AbbrEntry.verify_found` before including it, and lists the matches sorted by abbreviation; falls back to every `always_understand`-tagged entry when `query` is omitted or empty |
| `AbbrTagNode` | `(tag-slug)`, such as `(emoji)` | `abbr_tag_node.py` | every entry carrying that single `AbbrTags` member |
| `GlossaryNode` | `(glossary-name)` | `glossary_node.py` | every entry whose `tags` name that glossary |

`AbbrTagNode` and `GlossaryNode` are not fixed engine types, but are created per name:

- one `AbbrTagNode` per single-bit `AbbrTags` member except `always_understand`, which `DecodeOnlyAbbrNode` already covers; the slug is the member name in kebab case, such as `single_character` to `single-character`
- one `GlossaryNode` per glossary registered via `register_abbr_glossary`, never enumerated in `kaye_engine` code itself

Both auto-attach to the corpus tree, see [Dynamic Node Documentation](dynamic-content-doc.md) for the heading resolution order.

A `GlossaryNode` renders by its glossary's registered flags: bullets or numbered markers, insertion order or sorted by `priority`, whether the `(...)` remark suffix appears, and whether every entry is forced into term-definition form. All four may be overridden per render via `content_lines(is_sorted=..., is_numbered_list=..., is_remark_disabled=..., is_term_definition_forced=...)`.

Hiding high-priority-number entries is a generation-time concern only. Pass `content_lines(glossary_priority_threshold=...)`, or the matching `render_prompt(glossary_priority_threshold=...)` keyword, since it flows through to every checkmarked node's `content_lines()`. `None` (the default) disables the filter.













### queried decode-only abbr

`(decode-only-abbr)` needs render-time input: a piece of text to scan for abbreviation occurrences. Pass it as `query=` to `render_prompt()` or `render.render_prompt_lines()`:

```python
prompt = render_prompt(
    blueprint,
    query="use an algo to calc the avg",
)
```

Given that query, `(decode-only-abbr)` finds `algo` and `calc` and renders them as a Markdown list:

```markdown
- algo:algorithm
- calc:calculate
```

Each raw match is verified before it is kept:

- an entry tagged `term_definition` never matches
- a lowercase abbreviation matches in any case; any other abbreviation must match its exact spelling
- the characters before and after the match must satisfy the entry's [`wrap`](#wrap) rule

If `query` is omitted or empty, `(decode-only-abbr)` falls back to every abbreviation tagged `always_understand`. `AbbrTagNode` and `GlossaryNode` ignore `query` entirely.


































## Exportable Groups

Loading `abbrs.json` also registers abbreviation groups into `exportable_registry`, so they export as Agent Skills, see [`exportable-registry-doc.md`](exportable-registry-doc.md). Each group is an `ExportableAbbr`, a list of entries sorted by abbreviation, rendered as a Markdown list. The groups are recomputed on every load, replacing any earlier group under the same key:

- by tag: `Abbr Single Character`, `Abbr Emoji`
- by glossary: one `Glossary NAME` group, named `glossary-NAME`, per glossary registered with `is_exportable=True`
- by wrap: `Abbr Prefixes`, `Abbr Suffixes`, `Abbr Symbols`
- by first character: `Abbr Starts with Digits 0~9`, one per letter `A` to `Z`, and `Abbr Starts with Non-Alphanumeric`

Only a glossary group can be user-invokable, following its `is_user_invokable` flag; every other group is llm-only.


































## entries `json` file schema

Top level structure:

```json
{
  "MEANING1": {
    "remark": "optional free-text note about this meaning",
    "abbrs": {
      "ABBR1": {
        "priority": 0,
        "tags": ["ascii_only", "common", "coding-terms"],
        "wrap": "word",
        "remark": "optional free-text note about this abbreviation"
      },
      "ABBR2": {}
    }
  },
  "MEANING2": {}
}
```

Each `MEANING` entry is an *object* with:

- `remark` *(optional)*: a *string* free-text note about this meaning; omitted when there is nothing to add
- `abbrs` *(required)*: an *object* mapping each spelling of this meaning to its own fields













### meaning-level fields





#### `remark`

An *optional string* free-text note about the meaning as a whole, not any single spelling. Omit this key entirely when there is no remark.





#### `abbrs`

A *required object* mapping each spelling (`ABBR1`, `ABBR2`, ...) of this meaning to its own fields, documented below.













### abbr-level fields

These fields live under each key of a meaning's `abbrs` object. `priority`, `tags` and `wrap` are all **required**; a missing one raises `ValueError`.





#### `priority`

An *integer* value, lower value means higher priority.





#### `tags`

A *required array* of *string*. Each item is resolved by trying it against the fixed, engine-defined `AbbrTags` enum first; anything that does not match a member is treated instead as a free-form, consumer-defined glossary name, which must already be registered via [`register_abbr_glossary`](#register_abbr_glossaryname-is_exportable-) before this entry is loaded, or loading raises `ValueError`. An entry exposes the two parts as `.tags` (an `AbbrTags` flag) and `.glossaries` (a tuple of names).

Fixed `AbbrTags` values:

- `"common"`: common abbreviations that any person might understand
- `"always_understand"`: abbreviations always provided so the LLM may understand them; the fallback list of `(decode-only-abbr)`
- `"term_definition"`: renders the entry as a term-definition list item (`mean` alone, or `mean (remark)`) instead of the default `abbr:mean` decode format
- character set:
  - `"single_character"`: single letter or character abbreviations
  - `"letters_only"`
  - `"word_character_only"`
  - `"ascii_only"`
  - `"emoji"`

`AbbrTags` also defines the composites `WORD_CHARACTER` (letters only or word characters only) and `ASCII` (`WORD_CHARACTER` or ASCII only), which are not valid `tags` values on their own.

Anything else is looked up as a glossary name, e.g.:

```json
"tags": ["ascii_only", "coding-terms", "programming-language-codes"]
```

Each glossary name also works as a [dynamic node](dynamic-content-doc.md) heading: `(glossary-name)` auto-populates with every matching entry, via `GlossaryNode`, see [Abbreviation Dynamic Nodes](#abbreviation-dynamic-nodes).





#### `wrap`

Defines how the abbreviation must be bounded by the characters before and after it, when found in a query. It must be one of these *string* values:

| Value | Characters before and after the match |
| --- | --- |
| `"word"` | a word boundary on both sides |
| `"prefix"` | a word boundary before, a word character after |
| `"suffix"` | a word character before, a word boundary after |
| `"symbol"` | a word boundary on both sides |
| `"unit"` | a unit-like abbreviation: a digit or boundary before, a word boundary after |
| `"currency"` | a currency-like abbreviation: a word boundary before, a digit or boundary after |

An unknown value raises `ValueError`.





#### `remark`

An *optional string* free-text note about this specific abbreviation, as opposed to the meaning's `remark`, which applies to every spelling. Omit this key entirely when there is no remark.

When rendered as a Markdown list entry, the meaning's `remark` and the abbreviation's `remark` are both included, in that order and separated by `; `, when present, e.g. `- abbr:meaning (meaning remark; abbr remark)`. Pass `is_remark_disabled=True` to `AbbrEntry.as_md_list_entry`, `GlossaryNode.content_lines`, or `register_abbr_glossary` to omit this suffix regardless of either `remark` being set.

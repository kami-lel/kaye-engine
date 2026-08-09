# `abbr_collection` Documentation

`abbr_collection` is the package that deals with **abbreviations**: the entry data structures, the store, and the loader that populates it from `abbrs.json`.

Every abbreviation-related *dynamic node* reads through this store rather than parsing the file or holding its own copy of the data.


































## `abbr_collection` module

### `get_abbr_data()`

Return the single, always-present `AbbrData` singleton.

```python
from kaye_engine.abbr_collection import get_abbr_data

data = get_abbr_data()
for entry in data.abbrs:
    print(entry.as_md_list_entry())
```





#### adding entries by hand

To add entries directly, open the singleton as a context manager and call `add_entry` for each one:

```python
from kaye_engine.abbr_collection import get_abbr_data, AbbrMeaning

data = get_abbr_data()
with data:
    mean = AbbrMeaning("for example", remark=None)
    data.add_entry(mean, "e.g.", {"priority": 5, "tags": [], "wrap": "word"})
```

> [!IMPORTANT]
> The `with` block matters: entries added inside it aren't searchable until the block exits, since that is when the lookup index is rebuilt.





#### `populate_abbr_data_with_json_file(file_path)`

Parse an `.json` file and add every entry it contains into `get_abbr_data()`.

```python
from kaye_engine.abbr_collection import populate_abbr_data_with_json_file

populate_abbr_data_with_json_file("abbrs.json")
```

Q.v. [abbreviation entries `json` file](#abbreviation-entries-json-file) below for the file's required schema.

> [!IMPORTANT]
> Every glossary name any entry's `tags` array uses (any item that isn't a fixed `AbbrTags` value) must already be registered via `register_abbr_glossary` (v.i.) before that entry is added — otherwise `add_entry`/`populate_abbr_data_with_json_file` raises `ValueError`.




#### `register_abbr_glossary(name, uses_numbered_list=False, is_sorted=False)`

Register a glossary name so entries may reference it via `tags` (v.i.), and set that glossary's default rendering behavior for its `GlossaryNode`:

- `uses_numbered_list`: render entries with numbered markers (`"1. ..."`) instead of bullets (`"- ..."`)
- `is_sorted`: render entries ordered by ascending `priority` instead of insertion order

```python
from kaye_engine.abbr_collection import register_abbr_glossary

register_abbr_glossary("coding-terms")
register_abbr_glossary("plan-step-by-step-abbr", uses_numbered_list=True, is_sorted=True)
```

Raises `ValueError` if `name` is already registered. Both flags are also render-time overrides — q.v. [`GlossaryNode`](#abbreviations-related-dynamic-nodes) below.

Priority-based filtering is not a registration concern — it is supplied by the caller at generation time via `glossary_priority_threshold`, q.v. below.

> [!NOTE]
> `glossary_priority_threshold` only filters rendering. An entry whose `priority` exceeds the threshold is still added to `AbbrData` — its `tags` glossary membership is still validated, and it is still findable through `get_abbr_data()` — it simply never appears in a rendered `GlossaryNode`.


































## abbreviations-related dynamic nodes

Every abbreviation-related [dynamic node](dynamic-node-doc.md) lives in `kaye_engine/prompt/dynamic_nodes/` and reads through `get_abbr_data()`.

| Node | Heading | Source | Behavior |
| --- | --- | --- | --- |
| `ShorthandNode` | `(Decode-Only Shorthand)` | `shorthand_node.py` | scans a `query=` string against `get_abbr_data().automaton`, verifying each raw match with `AbbrEntry.verify_found` before including it; falls back to every `always_understand`-tagged entry when `query` is omitted |
| `GlossaryNode` | `(glossary-name)` | `glossary_node.py` | every entry whose `glossaries` array contains `glossary-name` |

Unlike `ShorthandNode`, `GlossaryNode` is not a fixed engine type — one instance is created per glossary name a consumer registered via `register_abbr_glossary` (v.s.) and referenced on `AbbrEntry.glossaries` (q.v. [`tags`](#tags) below), never enumerated in `kaye-engine` code itself. Its rendering — bullets vs. numbered markers, and insertion order vs. sorted by `priority` — defaults to that glossary's registered flags, and both may be overridden per render via `content_lines(is_sorted=..., uses_numbered_list=...)`. Whether high-priority-number entries are hidden is a generation-time-only concern, not a registration default: pass `content_lines(glossary_priority_threshold=...)` (or the matching `generate_prompt(glossary_priority_threshold=...)` kwarg, since it flows through to every checkmarked node's `content_lines()`) — `None` (default) disables the filter. Q.v. [dynamic-node-doc.md](dynamic-node-doc.md) for the heading resolution order.













### queried shorthand

`(Decode-Only Shorthand)` needs render-time input — a piece of text to scan for abbreviation occurrences. Pass it as `query=` to `generate_prompt()` / `render.render_prompt_lines()`:

```python
prompt = blueprint.generate_prompt(
    query="use an algo to calc the avg",
)
```

Given that query, `(Decode-Only Shorthand)` finds `algo` and `calc` (verifying each match against its surrounding characters to avoid false positives) and renders them as a Markdown list:

```markdown
- algo:algorithm
- calc:calculate
```

If `query` is omitted or empty, `(Decode-Only Shorthand)` falls back to rendering every abbreviation tagged `always_understand`, the same way every `GlossaryNode` always does — those nodes ignore `query` entirely and simply render every entry carrying their glossary.

































## entries `json` file schema

Top level structure:

```json
{
  "MEANING1": {
    "remark": "optional free-text note about this meaning",
    "abbrs": {
      "ABBR1": {
        "priority": 0,
        "tags": [
          "ascii_only",
          "common",
          "coding-terms"
        ],
        "wrap": "word",
        "remark": "optional free-text note about this abbreviation",
       },
      "ABBR2": { ~ },
     }
  },

  "MEANING2": { ~ },
  "MEANING3": { ~ },
  ~
}
```

Each `MEANING` entry is an *object* with:

- `remark` *(optional)*: a *string* free-text note about this meaning; omitted when there is nothing to add
- `abbrs` *(required)*: an *object* mapping each spelling of this meaning to its own fields (v.i.)













### meaning-level fields

#### `remark`

An *optional string* free-text note about the meaning as a whole (not any single spelling). Omit this key entirely when there is no remark.





#### `abbrs`

A *required object* mapping each spelling/abbreviation (`ABBR1`, `ABBR2`, ...) of this meaning to its own fields, documented below.













### abbr-level fields

These fields live under each key of a meaning's `abbrs` object.





#### `priority`

An *integer* value, lower value means higher priority.





#### `tags`

A *required array* of *string*. Each item is resolved by trying it against
the fixed, engine-defined `AbbrTags` enum first; anything that doesn't
match a member is treated instead as a free-form, consumer-defined
glossary name, which must already be registered via
[`register_abbr_glossary`](#register_abbr_glossaryname-uses_numbered_listfalse-is_sortedfalse)
before this entry is loaded, or loading raises `ValueError`.

Fixed `AbbrTags` values:

- `"common"`: common abbreviations that any person might understand
- usage cases (these tags should be mutually exclusive):

  - `"always_understand"`: list of abbreviation always provided such LLM may understand

- character set:

  - `"single_character"`: single letter/character abbreviations
  - `"letters_only"`
  - `"word_character_only"`
  - `"ascii_only"`
  - `"emoji"`

Anything else is looked up as a glossary name, e.g.:

```json
"tags": ["ascii_only", "coding-terms", "programming-language-codes"]
```

Each glossary name also works as a [dynamic node](dynamic-node-doc.md)
heading: `(glossary-name)` auto-populates with every matching entry, via
`GlossaryNode` — q.v. [abbreviations-related dynamic nodes](#abbreviations-related-dynamic-nodes).





#### `"wrap"`

Define how the abbreviation will be understood with character before and after it.

Must be a *string* of these selected values:

- `"word"`
- `"prefix"`
- `"suffix"`
- `"symbol"`
- `"unit"`: unit-like abbreviation after a number
- `"currency"`: currency-like abbreviation before a number





#### `remark`

An *optional string* free-text note about this specific abbreviation (as opposed to the meaning's `remark`, which applies to every spelling). Omit this key entirely when there is no remark.

When rendered as a Markdown list entry, the meaning's `remark` and the abbr's `remark` are both included (in that order, separated by `; `) when present, e.g. `- abbr:meaning (meaning remark; abbr remark)`.


































## registered abbr groups


<!-- BUG export & register logic is wrong -->

kaye-engine itself registers none of these — every glossary below is registered by the current consumer (kaye-vault) via `register_abbr_glossary`, then exported under `abbr-glossary-<name>` by `register_exportable_abbrs` (q.v. [`exportable-registry-doc.md`](exportable-registry-doc.md)); every entry shares the same flags: `always_apply: no`, `user_invokable: no`, `llm_invokable: yes`.

| canonical name | display name | always_apply | user_invokable | llm_invokable |
| --- | --- | --- | --- | --- |
| `abbr-glossary-cardinal-directions` | Glossary cardinal-directions | ❌ | ❌ | ✔️ |
| `abbr-glossary-code-documentation-field-abbr` | Glossary code-documentation-field-abbr | ❌ | ❌ | ✔️ |
| `abbr-glossary-coding-terms` | Glossary coding-terms | ❌ | ❌ | ✔️ |
| `abbr-glossary-commit-sense-sigil` | Glossary commit-sense-sigil | ❌ | ❌ | ✔️ |
| `abbr-glossary-currency-symbols` | Glossary currency-symbols | ❌ | ❌ | ✔️ |
| `abbr-glossary-days-of-week` | Glossary days-of-week | ❌ | ❌ | ✔️ |
| `abbr-glossary-git-abbr` | Glossary git-abbr | ❌ | ❌ | ✔️ |
| `abbr-glossary-log-level` | Glossary log-level | ❌ | ❌ | ✔️ |
| `abbr-glossary-natural-language-codes` | Glossary natural-language-codes | ❌ | ❌ | ✔️ |
| `abbr-glossary-plan-step-by-step-abbr` | Glossary plan-step-by-step-abbr | ❌ | ❌ | ✔️ |
| `abbr-glossary-programming-language-codes` | Glossary programming-language-codes | ❌ | ❌ | ✔️ |
| `abbr-glossary-seasons` | Glossary seasons | ❌ | ❌ | ✔️ |
| `abbr-glossary-units-of-measure` | Glossary units-of-measure | ❌ | ❌ | ✔️ |
| `abbr-glossary-unity-engine-abbr` | Glossary unity-engine-abbr | ❌ | ❌ | ✔️ |
| `abbr-glossary-usable-agent-decoratives` | Glossary usable-agent-decoratives | ❌ | ❌ | ✔️ |
| `abbr-glossary-usable-agent-shorthands` | Glossary usable-agent-shorthands | ❌ | ❌ | ✔️ |
| `abbr-glossary-usable-briefness-abbr` | Glossary usable-briefness-abbr | ❌ | ❌ | ✔️ |
| `abbr-glossary-usable-commit-sense-shorthands` | Glossary usable-commit-sense-shorthands | ❌ | ❌ | ✔️ |
| `abbr-glossary-usable-identifier-abbr` | Glossary usable-identifier-abbr | ❌ | ❌ | ✔️ |


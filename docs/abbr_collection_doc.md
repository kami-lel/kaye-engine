# `abbr_collection` Documentation

**`abbr_collection`** holds the data structures and loader behind every
abbreviation-related dynamic node — `AbbrEntry`, `AbbrMeaning`,
`AbbrTags`, `AbbrWrap`, `AbbrData`, and the functions that populate and
expose a single, always-present `AbbrData` singleton. It owns the schema
and the lookup mechanism; the actual abbreviation entries live in a
separate `abbrs.json` file supplied by a host package, since kaye-engine
bundles no copy of its own.




## 1. Using `abbr_collection`

### `populate_abbr_data_with_json_file(file_path)`

Parse an `abbrs.json` file (v.i. for its schema) and add every entry it
contains into the single `get_abbr_data()` instance, via
`AbbrData.add_entry`. The lookup automaton is rebuilt once, after the
whole file has been applied.

```python
from kaye_engine.abbr_collection import populate_abbr_data_with_json_file

populate_abbr_data_with_json_file("abbrs.json")
```

- **raises** `json.JSONDecodeError`: malformed JSON
- **raises** `ValueError`: malformed content, or an entry duplicating one
  already added

### `get_abbr_data()`

Return the single, always-present `AbbrData` singleton — empty if nothing
has been added yet. Every abbreviation-related dynamic node reads through
this function rather than holding its own reference.

```python
from kaye_engine.abbr_collection import get_abbr_data

data = get_abbr_data()
for entry in data.abbrs:
    print(entry.as_md_list_entry())
```

### `AbbrData`

Holds the parsed collection — `.meanings` (list of `AbbrMeaning`),
`.abbrs` (list of `AbbrEntry`), and `.automaton` (an `ahocorasick`
automaton used for fast substring matching against arbitrary query text).
Starts empty and grows additively, one `AbbrEntry` at a time, via
`add_entry`, called within a `with` block so the automaton is rebuilt once
per batch rather than per entry:

```python
from kaye_engine.abbr_collection import AbbrData, AbbrMeaning

data = AbbrData()
with data:
    mean = AbbrMeaning("for example", remark=None)
    data.add_entry(mean, "e.g.", {"priority": 5, "tags": [], "wrap": "word"})
```

### `AbbrEntry`

A single `abbr => meaning` record — `.abbr`, `.mean`, `.priority`,
`.tags` (`AbbrTags`), `.wrap` (`AbbrWrap`), `.remark`. Provides
`as_md_list_entry()` to render itself as a Markdown list item
(`- abbr:meaning`, or `- abbr:meaning (remark; remark)` when either the
meaning or the abbr carries a remark), and `verify_found(found,
char_before, char_after)` to confirm a raw automaton match satisfies case
sensitivity and wrap-boundary rules before it is accepted.

### `AbbrMeaning`

Represents a single meaning shared by one or more spellings — `.mean`,
`.remark`.

### `AbbrTags`

A bit-flag `Enum` of every tag an abbreviation entry may carry (v.i. for
the full list). `AbbrTags.parse(tags_list)` converts the raw `list[str]`
from `abbrs.json` into a combined flag value, raising `ValueError` on any
unrecognized tag.

### `AbbrWrap`

An `Enum` of boundary rules (`WORD`, `PREFIX`, `SUFFIX`, `SYMBOL`, `UNIT`,
`CURRENCY`) governing what characters may surround a match for it to
count as a real occurrence — q.v. `AbbrEntry.verify_found` above, and the
`wrap` field description in the schema section below.




## 2. Where Abbreviations Are Used

Every abbreviation-related [dynamic node](dynamic_node_doc.md) lives in
`kaye_engine/prompt/dynamic_nodes/` and reads through `get_abbr_data()` —
none of them hold their own copy of the data.

| Node | Heading | Source | Behavior |
| --- | --- | --- | --- |
| `AbbrNode` | `(Abbreviations)` | `abbr_nodes.py` | scans a `query=` string against `get_abbr_data().automaton`, verifying each raw match with `AbbrEntry.verify_found` before including it; falls back to every `always_understand`-tagged entry when `query` is omitted |
| `UsableAbbrNode` | `(Usable Abbreviations)` | `abbr_tag_nodes.py` | every entry tagged `usable_in_brief` |
| `CodingTermsNode` | `(Coding Terms)` | `abbr_tag_nodes.py` | every entry tagged `coding` |
| `LanguageCodeNode` | `(Languages Code)` | `abbr_tag_nodes.py` | every entry tagged `language_code` |
| `PLCNode` | `(Programming Languages Code)` | `abbr_tag_nodes.py` | every entry tagged `programming_language_code` |
| `UnityEngineAbbrNode` | `(Unity Engine Abbreviations)` | `abbr_tag_nodes.py` | every entry tagged `unity_engine_abbr` |

`AbbrNode` is the only one that does substring scanning against render-time
input; the rest are thin wrappers around `gen_abbrs_content_lines(tag)`,
which filters `get_abbr_data().abbrs` by a single `AbbrTags` member and
renders each match via `AbbrEntry.as_md_list_entry()`.




## 3. `abbrs.json` Schema

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
          "common"
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

- `remark` *(optional)*: a *string* free-text note about this meaning;
  omitted when there is nothing to add
- `abbrs` *(required)*: an *object* mapping each spelling of this meaning
  to its own fields (v.i.)

### meaning-level fields

#### `remark`

An *optional string* free-text note about the meaning as a whole (not
any single spelling). Omit this key entirely when there is no remark.

#### `abbrs`

A *required object* mapping each spelling/abbreviation (`ABBR1`, `ABBR2`,
...) of this meaning to its own fields, documented below.

### abbr-level fields

These fields live under each key of a meaning's `abbrs` object.

#### `priority`

An *integer* value, lower value means higher priority.

#### `tags`

Additional information regards this entry,
must be an *array* of *string* of these selected values:

- `"common"`: common abbreviations that any person might understand
- usage cases (these tags should be mutually exclusive):

  - `"always_understand"`: list of abbreviation always provided such LLM may understand
  - `"usable_in_brief"`: abbreviations those can be used during for briefness styles
  - `"coding"`: abbreviation/terms used in software development / coding context

- specialized groups:
  - `"programming_language_code"`: it is an abbreviation of a programming language
    e.g. `cpp` for C++ programming language
  - `"language_code"`: abbreviation for natural languages;
    partial of and based on ISO 639-1 (2 letter)
  - `"unity_engine_abbr"`: abbreviations specific to Unity Engine
  - `"log_level"`
  - `"unit_of_measure"`: scientific units for measurement
  - `"currency_symbol"`: monetary currency symbol

- character set:

  - `"single_character"`: single letter/character abbreviations
  - `"letters_only"`
  - `"word_character_only"`
  - `"ascii_only"`
  - `"emoji"`

#### `"wrap"`

Define how the abbreviation will be understood
with character before and after it.

Must be a *string* of these selected values:

- `"word"`
- `"prefix"`
- `"suffix"`
- `"symbol"`
- `"unit"`: unit-like abbreviation after a number
- `"currency"`: currency-like abbreviation before a number

#### `remark`

An *optional string* free-text note about this specific abbreviation (as
opposed to the meaning's `remark`, which applies to every spelling). Omit
this key entirely when there is no remark.

When rendered as a Markdown list entry, the meaning's `remark` and the
abbr's `remark` are both included (in that order, separated by `; `) when
present, e.g. `- abbr:meaning (meaning remark; abbr remark)`.

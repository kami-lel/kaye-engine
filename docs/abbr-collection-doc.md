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


































## abbreviations-related dynamic nodes

Every abbreviation-related [dynamic node](dynamic-node-doc.md) lives in `kaye_engine/prompt/dynamic_nodes/` and reads through `get_abbr_data()`.

| Node | Heading | Source | Behavior |
| --- | --- | --- | --- |
| `AbbrNode` | `(Abbreviations)` | `abbr_nodes.py` | scans a `query=` string against `get_abbr_data().automaton`, verifying each raw match with `AbbrEntry.verify_found` before including it; falls back to every `always_understand`-tagged entry when `query` is omitted |
| `UsableAbbrNode` | `(Usable Abbreviations)` | `abbr_tag_nodes.py` | every entry tagged `usable_in_brief` |
| `CodingTermsNode` | `(Coding Terms)` | `abbr_tag_nodes.py` | every entry tagged `coding` |
| `LanguageCodeNode` | `(Languages Code)` | `abbr_tag_nodes.py` | every entry tagged `language_code` |
| `PLCNode` | `(Programming Languages Code)` | `abbr_tag_nodes.py` | every entry tagged `programming_language_code` |
| `UnityEngineAbbrNode` | `(Unity Engine Abbreviations)` | `abbr_tag_nodes.py` | every entry tagged `unity_engine_abbr` |
| `PlanStepByStepAbbrNode` | `(Plan Step By Step Abbreviations)` | `abbr_tag_nodes.py` | every entry tagged `plan_step_by_step_abbr` |
| `CodeDocumentationFieldAbbrNode` | `(Code Documentation Field Abbreviations)` | `abbr_tag_nodes.py` | every entry tagged `code_documentation_field_abbr` |













### queried abbreviations

`(Abbreviations)` needs render-time input — a piece of text to scan for abbreviation occurrences. Pass it as `query=` to `generate_prompt()` / `render.render_prompt_lines()`:

```python
prompt = blueprint.generate_prompt(
    query="use an algo to calc the avg",
)
```

Given that query, `(Abbreviations)` finds `algo` and `calc` (verifying each match against its surrounding characters to avoid false positives) and renders them as a Markdown list:

```markdown
- algo:algorithm
- calc:calculate
```

If `query` is omitted or empty, `(Abbreviations)` falls back to rendering every abbreviation tagged `always_understand`, the same way the tag-filtered nodes (`(Usable Abbreviations)`, `(Coding Terms)`, etc.) always do — those nodes ignore `query` entirely and simply render every entry carrying their tag.

































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

Additional information regards this entry, must be an *array* of *string* of these selected values:

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
  - `"plan_step_by_step_abbr"`: abbreviations used within step-by-step planning
  - `"code_documentation_field_abbr"`: abbreviations for code documentation
    fields, e.g. docstring/comment field keywords

- character set:

  - `"single_character"`: single letter/character abbreviations
  - `"letters_only"`
  - `"word_character_only"`
  - `"ascii_only"`
  - `"emoji"`





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

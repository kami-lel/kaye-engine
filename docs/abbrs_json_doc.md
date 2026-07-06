# `abbrs.json` documentation

Explain format of `kaye/abbrs.json`

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













## meaning-level fields

#### `remark`

An *optional string* free-text note about the meaning as a whole (not any single spelling). Omit this key entirely when there is no remark.

#### `abbrs`

A *required object* mapping each spelling/abbreviation (`ABBR1`, `ABBR2`, ...) of this meaning to its own fields, documented below.




## abbr-level fields

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






#### ``"wrap"``

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

An *optional string* free-text note about this specific abbreviation (as opposed to the meaning's `remark`, which applies to every spelling). Omit this key entirely when there is no remark.

When rendered as a Markdown list entry, the meaning's `remark` and the abbr's `remark` are both included (in that order, separated by `; `) when present, e.g. `- abbr:meaning (meaning remark; abbr remark)`.
# `abbrs.json` documentation

Explain format of `kaye/gen_prompt/abbrs.json`

Top level structure:

```json
{
  "MEANING1": {
    "ABBR1": {
      "priority": 0,
      "tags": [
        "ascii_only",
        "common"
      ],
      "wrap": "word",
     },
    "ABBR2": { ~ },
   },

  "MEANING2": { ~ },
  "MEANING3": { ~ },
  ~
}
```













## fields

#### `priority`

An *integer* value, lower value means higher priority.





#### `tags`

Additional information regards this entry,
must be an *array* of *string* of these selected values:

- `"common"`: common abbreviations that any person might understand,
  thus LLM may utilize this abbreviation in conversation

- `"programming_language"`: it is an abbreviation of a programming language
  e.g. `cpp` for C++ programming language

Character set:

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
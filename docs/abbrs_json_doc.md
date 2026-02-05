# `abbrs.json` documentation

Explain format of `kaye/gen_prompt/abbrs.json`


Top level structure:

```json
{
  "abbrs": {
    ...
  },
  "alts": {
    ...
  }
}
```





#### entries in `"abbrs"`

Key must be a *string* of the **abbreviation** itself.

Value must be an object contains:

- ``"mean"``: meaning of the abbreviation, *string*
- ``"wrap"``: v.i.
- ``"tags"``: v.i.

E.g.

```json
{
  "abbrs": {
    "e.g.": {
      "mean": "for example,for instance",
      "tags": [
        "ascii"
      ],
      "wrap": "word"
    },
    "avg": {
      "mean": "average",
      "tags": [
        "ascii"
      ],
      "wrap": "word"
    },
    ...
  },
  ...
}
```



#### entries in `"alts"`

Key must be a *string* of the **alternative spelling** of an abbreviation.

Value must be an object contains:

- ``"abbr"``: name reference of an abbreviation entry existed in ``"abbrs"``
- ``"wrap"``: v.i.
- ``"tags"``: v.i.


E.g.

```json
{
  ...
  "alts": {
    "eg": {
      "abbr": "e.g.",
      "tags": [
        "ascii"
      ],
      "wrap": "word"
    },
    ...
  }
}
```





#### ``"tags"``

Additional information regards this entry,
must be an *array* of *string* of these selected values:

- `"ascii"`: this abbreviation contains strictly ASCII characters
- `"usable"`: LLM may utilize this abbreviation in conversation
  and it will generally be considered understandable
- `"emoji"`
- `"programming_language"`: it is an abbreviation of a programming language,
  e.g. `cpp` for C++ programming language





#### ``"wrap"``

Define how the abbreviation will be understood
with character before and after it.

Must be a *string* of these selected values:

- `"word"`
- `"prefix"`
- `"suffix"`
- `"symbol"`
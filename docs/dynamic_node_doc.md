# Dynamic Node Documentation

**Dynamic nodes** are prompt corpus nodes whose content is generated at render time instead of being written by hand — today's date, abbreviation lookups against a query, and similar. Unlike [sidecar nodes](sidecar_node_doc.md), dynamic nodes **are** included in the rendered prompt output by default, exactly like a regular corpus section.

Every dynamic node's name is its heading wrapped in parentheses, e.g. `(Today)`, `(Abbreviations)` — that syntax marks a node as dynamic wherever it appears, whether in a tree preview, a blueprint, or an error message.




## Available Dynamic Nodes

| Node | Heading | Renders |
| --- | --- | --- |
| Today | `(Today)` | current date and time |
| Abbreviations | `(Abbreviations)` | meanings of abbreviations found in a `query=` string, or every `always_understand`-tagged entry when no query is given |
| Usable Abbreviations | `(Usable Abbreviations)` | abbreviations tagged `usable_in_brief` |
| Coding Terms | `(Coding Terms)` | abbreviations tagged `coding` |
| Languages Code | `(Languages Code)` | abbreviations tagged `language_code` |
| Programming Languages Code | `(Programming Languages Code)` | abbreviations tagged `programming_language_code` |
| Unity Engine Abbreviations | `(Unity Engine Abbreviations)` | abbreviations tagged `unity_engine_abbr` |

Q.v. [`abbrs_json_doc.md`](abbrs_json_doc.md) for how the `tags` field on an abbreviation entry drives the tag-filtered nodes above.

Every dynamic node is a **leaf** — it never has children, so it cannot itself contain sub-sections.




## Using a Dynamic Node

Every dynamic node type is attached once to the prompt corpus tree automatically, as a direct child of the root — you do not add them to `prompt_corpus.md` yourself, and in fact `prompt_corpus.md` **rejects** any heading in the `(...)` form, since that syntax is reserved for dynamic nodes.

Once attached, a dynamic node behaves like any other corpus node in a blueprint: checkmark it to include it, uncheckmark it to leave it out.

```python
from kaye.prompt import PromptBlueprint

blueprint_text = """ ○
[x] └── (Abbreviations)"""

blueprint = PromptBlueprint.parse(blueprint_text)
prompt = blueprint.generate_prompt()
```

There is no special opt-in required — unlike conditional sidecar nodes, which are excluded unless explicitly requested via `contains_sidecar_nodes=`, q.v. [`sidecar_node_doc.md`](sidecar_node_doc.md#conditional-sidecar-nodes).




## Feeding Render-Time Input

Some dynamic nodes need input that only exists at render time — `(Abbreviations)` scans a piece of text for abbreviation occurrences, for example. Pass that input as an extra keyword argument to `generate_prompt()` / `render.render_prompt_lines()`; it is forwarded to every node's content generation, and each dynamic node picks out the keyword(s) it understands.

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

`(Today)` needs no input at all; it always renders the current date and time.




## Adding Introductory Text

A dynamic node's content is generated at render time, so you cannot normally write your own text into it. If you want introductory text to appear above a dynamic node's generated content, write a regular section in `prompt_corpus.md` with that dynamic node's exact heading:

```markdown
# (Usable Abbreviations)

Use the following abbreviations only when brevity is required.
```

When the corpus loads, that section is detected, removed from the static tree, and its content is carried over as a **preface** — prepended to the dynamic node's generated lines every time it renders. The result is a single `(Usable Abbreviations)` node whose output is:

```markdown
Use the following abbreviations only when brevity is required.
- ...
- ...
```

Without this, any section written under a dynamic node's heading is silently dropped in favor of the generated content.




## Cross-References

- [`corpus_doc.md`](corpus_doc.md) — `prompt_corpus.md` format and heading-to-tree-depth rules
- [`sidecar_node_doc.md`](sidecar_node_doc.md) — sidecar nodes, the other special node category, and how they differ from dynamic nodes
- [`programmatic_api_doc.md`](programmatic_api_doc.md) — `PromptBlueprint`, checkmarking, and `generate_prompt()` / `render.render_prompt_lines()` in full
- [`abbrs_json_doc.md`](abbrs_json_doc.md) — abbreviation entries and the tags the tag-filtered dynamic nodes key off of

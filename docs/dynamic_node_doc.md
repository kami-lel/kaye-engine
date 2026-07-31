# Dynamic Node Documentation

**Dynamic nodes** are prompt corpus nodes whose content is generated at render time instead of being written by hand — today's date, and similar. Unlike [sidecar nodes](sidecar_node_doc.md), dynamic nodes **are** included in the rendered prompt output by default, exactly like a regular corpus section.

Every dynamic node's name is its heading wrapped in parentheses, e.g. `(Today)` — that syntax marks a node as dynamic wherever it appears, whether in a tree preview, a blueprint, or an error message.




## Available Dynamic Nodes

| Node | Heading | Renders |
| --- | --- | --- |
| Today | `(Today)` | current date and time |

Every abbreviation-related dynamic node (`(Abbreviations)`, `(Usable Abbreviations)`, `(Coding Terms)`, and the rest) is documented separately in [`abbr_collection_doc.md`](abbr_collection_doc.md).

Every dynamic node is a **leaf** — it never has children, so it cannot itself contain sub-sections.




## Using a Dynamic Node

Every dynamic node type is attached once to the prompt corpus tree automatically, as a direct child of the root — you do not add them to `prompt_corpus.md` yourself, and in fact `prompt_corpus.md` **rejects** any heading in the `(...)` form, since that syntax is reserved for dynamic nodes.

Once attached, a dynamic node behaves like any other corpus node in a blueprint: checkmark it to include it, uncheckmark it to leave it out.

```python
from kaye_engine.prompt import PromptBlueprint

blueprint_text = """ ○
[x] └── (Today)"""

blueprint = PromptBlueprint.parse(blueprint_text)
prompt = blueprint.generate_prompt()
```

There is no special opt-in required — unlike conditional sidecar nodes, which are excluded unless explicitly requested via `contains_sidecars=`, q.v. [`sidecar_node_doc.md`](sidecar_node_doc.md#conditional-sidecar-nodes).




## Feeding Render-Time Input

Some dynamic nodes need input that only exists at render time — a search query, for example. Pass that input as an extra keyword argument to `generate_prompt()` / `render.render_prompt_lines()`; it is forwarded to every node's content generation, and each dynamic node picks out the keyword(s) it understands.

```python
prompt = blueprint.generate_prompt(
    query="...",
)
```

A dynamic node that has nothing to key off of ignores keywords it doesn't recognize. `(Today)` needs no input at all; it always renders the current date and time.




## Adding Introductory Text

A dynamic node's content is generated at render time, so you cannot normally write your own text into it. If you want introductory text to appear above a dynamic node's generated content, write a regular section in `prompt_corpus.md` with that dynamic node's exact heading:

```markdown
# (Today)

The current date and time, for reference.
```

When the corpus loads, that section is detected, removed from the static tree, and its content is carried over as a **preface** — prepended to the dynamic node's generated lines every time it renders. The result is a single `(Today)` node whose output is:

```markdown
The current date and time, for reference.
...
```

Without this, any section written under a dynamic node's heading is silently dropped in favor of the generated content.




## Cross-References

- [`corpus_doc.md`](corpus_doc.md) — `prompt_corpus.md` format and heading-to-tree-depth rules
- [`sidecar_node_doc.md`](sidecar_node_doc.md) — sidecar nodes, the other special node category, and how they differ from dynamic nodes
- [`programmatic_api_doc.md`](programmatic_api_doc.md) — `PromptBlueprint`, checkmarking, and `generate_prompt()` / `render.render_prompt_lines()` in full
- [`abbr_collection_doc.md`](abbr_collection_doc.md) — abbreviation-related dynamic nodes, their tags, and render-time query input

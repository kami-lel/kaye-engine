# Kaye Engine: Dynamic Node Documentation

**Dynamic nodes** are prompt corpus nodes whose content is generated at render time instead of being written by hand — today's date, and similar. Unlike [sidecar nodes](sidecar-node-doc.md), dynamic nodes **are** included in the rendered prompt output by default, exactly like a regular corpus section.

Every dynamic node's name is its heading wrapped in parentheses, e.g. `(Today)` — that syntax marks a node as dynamic wherever it appears, whether in a tree preview, a blueprint, or an error message.













## Available Dynamic Nodes

| Node | Heading | Renders |
| --- | --- | --- |
| Today | `(Today)` | current date and time |
| AbbrTagNode | `(Title Case Of Tag Name)` | every abbr entry tagged with that `AbbrTags` member |

`AbbrTagNode` is parametrized by an `AbbrTags` member instead of being subclassed per tag — one instance is attached per member of `ABBR_TAG_NODE_MEMBERS` (every simple, single-bit `AbbrTags` member except `always_understand`, which `(Decode-Only Shorthand)` already covers as its no-query fallback; composite members like `WORD_CHARACTER`/`ASCII` are excluded). Its heading is the tag's name in Title Case, e.g. `emoji` → `(Emoji)`, `single_character` → `(Single Character)`. On the CLI, the `NODE` argument for one of these is the raw tag name, e.g. `kaye-engine dn emoji`, `kaye-engine dn single_character`.

Every other abbreviation-related dynamic node (`(Decode-Only Shorthand)`, plus one `(glossary-name)` per abbr glossary, e.g. `(coding-terms)`) is documented in [`abbrs-doc.md`](abbrs-doc.md).

Every dynamic node is a **leaf** — it never has children, so it cannot itself contain sub-sections.













## Using a Dynamic Node

Engine-defined types (`Today`, `Decode-Only Shorthand`) attach automatically as direct children of the root — you do not add them to `prompt_corpus.md` yourself. `AbbrTagNode` also attaches automatically, one instance per `ABBR_TAG_NODE_MEMBERS` entry — no registration required, since every `AbbrTags` member is known statically. `GlossaryNode` (q.v. [`abbrs-doc.md`](abbrs-doc.md#tags)) is different: it attaches only when a top-level `(glossary-name)` heading is present **and** `glossary-name` is registered via `register_abbr_glossary`. No heading, no node; a registered glossary with no loaded entries yet still attaches and simply renders empty.

A top-level `(...)` heading resolves against engine-defined types first, then against `AbbrTagNode` headings, then against known glossary names. Loading a corpus **rejects** a parenthesized heading matching none of the three, or one below the root. A resolving heading supplies introductory text rather than creating a second node — v.i.

Once attached, a dynamic node behaves like any other corpus node in a blueprint: checkmark it to include it, uncheckmark it to leave it out.

```python
from kaye_engine.prompt import PromptBlueprint

blueprint_text = """ ○
[x] └── (Today)"""

blueprint = PromptBlueprint.parse(blueprint_text)
prompt = blueprint.generate_prompt()
```

There is no special opt-in required — unlike conditional sidecar nodes, which are excluded unless explicitly requested via `contains_sidecars=`, q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md#conditional-sidecar-nodes).













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

When the corpus loads, that section is detected, removed from the static tree, and its content lines are carried over as the dynamic node's `preface=` constructor argument — prepended to the dynamic node's generated lines every time it renders. This applies uniformly to every dynamic node type, since it is implemented once, generically, where each node type is attached to the tree — not something each dynamic node opts into individually. The result is a single `(Today)` node whose output is:

```markdown
The current date and time, for reference.
...
```

Without this, any section written under a dynamic node's heading is silently dropped in favor of the generated content.

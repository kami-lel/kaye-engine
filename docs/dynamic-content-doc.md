# Kaye Engine: Dynamic Content Documentation

**Dynamic nodes** are prompt corpus nodes whose content is generated at render time instead of being written by hand — today's date, and similar. Unlike [sidecar nodes](sidecar-node-doc.md), dynamic nodes **are** included in the rendered prompt output by default, exactly like a regular corpus section.

Every dynamic node's identity is a canonical **kebab-case** `NAME` slug; its heading is that slug wrapped in parentheses, e.g. `(today)` — that syntax marks a node as dynamic wherever it appears, whether in a tree preview, a blueprint, or an error message. This same `NAME` is also the CLI's `NODE` argument and the placeholder name inside a `(((name)))` inline substitution (q.v. [Dynamic Substitution](#dynamic-substitution) below) — one canonical name, three surfaces, resolved by a single shared function, `resolve_dynamic_node_factory`. Both structures below also accept the same extra render-time keyword arguments (q.v. [Feeding Render-Time Input](#feeding-render-time-input)).











## Dynamic Nodes

#### Identity & Naming

`AbbrTagNode` is parametrized by an `AbbrTags` member instead of being subclassed per tag — one instance is attached per member of `ABBR_TAG_NODE_MEMBERS` (every simple, single-bit `AbbrTags` member except `always_understand`, which `(decode-only-abbr)` already covers as its no-query fallback; composite members like `WORD_CHARACTER`/`ASCII` are excluded). Its `NAME` is `slug_for_abbr_tag(abbr_tag)` — the tag's name in kebab-case, e.g. `emoji` → `(emoji)`, `single_character` → `(single-character)`. On the CLI, the `NODE` argument for one of these is that same kebab slug, e.g. `kaye-engine dn emoji`, `kaye-engine dn single-character`.

Every other abbreviation-related dynamic node (`(decode-only-abbr)`, plus one `(glossary-name)` per abbr glossary, e.g. `(coding-terms)`) is documented in [`abbrs-doc.md`](abbrs-doc.md).



#### Leaf Constraint

Every dynamic node is a **leaf** — it never has children, so it cannot itself contain sub-sections.



#### Auto-Attachment

Every dynamic node auto-attaches when a corpus tree is created via `load_corpus_tree` — every engine-defined type (`today`, `decode-only-abbr`), every `ABBR_TAG_NODE_MEMBERS` entry, and every `GlossaryNode` for a glossary registered via `register_abbr_glossary`. You never need to author a `(name)` heading in `prompt_corpus.md` just for a dynamic node to exist and be checkmarkable — a registered glossary with no loaded entries yet still attaches and simply renders empty.

Where it attaches depends on whether `prompt_corpus.md` authors that node's `(name)` heading. Authored, at any nesting depth: the dynamic node takes that heading's exact spot in the tree, in place of it, keeping its position among siblings. Not authored: the node falls back to a direct child of root.

There is no special opt-in required — unlike conditional sidecar nodes, which are excluded unless explicitly requested via `conditional_sidecars=`, q.v. [`sidecar-node-doc.md`](sidecar-node-doc.md#conditional-sidecar-nodes).



#### Adding Introductory Text (Preface)

A dynamic node's content is generated at render time, so you cannot normally write your own text into it. If you want introductory text to appear above a dynamic node's generated content — and, per [Auto-Attachment](#auto-attachment) above, to place that node at a specific tree location — write a regular section in `prompt_corpus.md` with that dynamic node's exact heading:

```markdown
# (today)

The current date and time, for reference.
```

When the corpus loads, that section is detected, swapped for the dynamic node it names, and its content lines are carried over as the dynamic node's `preface=` constructor argument — prepended to the dynamic node's generated lines every time it renders. This applies uniformly to every dynamic node type, since it is implemented once, generically, where each node type is attached to the tree — not something each dynamic node opts into individually. The result is a single `(today)` node, in place of the authored heading, whose output is:

```markdown
The current date and time, for reference.
...
```

A `(name)` heading resolves against `resolve_dynamic_node_factory`: engine-defined types first, then `AbbrTagNode` slugs, then known glossary names. Loading a corpus **rejects** a parenthesized heading matching none of the three, and a `(name)` heading authored more than once for the same dynamic node.

Without an authored heading, a dynamic node still attaches — at root, with an empty preface — and renders only its generated content.



#### Checkmark Control

Once attached, a dynamic node behaves like any other corpus node in a blueprint: checkmark it to include it, uncheckmark it to leave it out.

```python
from kaye_engine.prompt import PromptBlueprint

blueprint_text = """ ○
[x] └── (today)"""

blueprint = PromptBlueprint.parse(blueprint_text)
prompt = blueprint.generate_prompt()
```

Because every dynamic node now auto-attaches, `PromptBlueprint.create_full_blueprint()` checkmarks them too, like any other node — its output now includes today's date/time, the shorthand fallback list, and the full content of every abbr-tag and every registered glossary, where previously it was effectively empty of dynamic content unless explicitly authored.













## Dynamic Substitution

#### Resolution & Headless Rendering

Alongside the tree-child mechanism above, `PromptBlueprint.generate_prompt()` runs a second, independent pass: any `(((name)))` placeholder appearing anywhere in the fully-assembled prompt text is replaced with that dynamic node's generated content — unconditionally, regardless of whether a same-named tree child exists or is checkmarked. This lets you drop a dynamic node's content in the middle of ordinary prose, not just as a whole checkmark-controlled section.

`name` resolves against the same `resolve_dynamic_node_factory` used by the tree mechanism, via a **headless** instance of the matched `DynamicNode` subclass (`parent=None`, empty preface) — content generation is identical, just without ever attaching to the tree.



#### Unconditional, Anywhere-in-Prose

```markdown
Today's date is (((today))), for reference.
```

renders as:

```markdown
Today's date is Date: 2026-08-13
Time: 16:35:45, for reference.
```

An unresolved `name` logs a warning and leaves the literal `(((name)))` text in place — it never raises.

The two mechanisms are independent and both fully functional: `DynamicNode` tree children give you whole-section, checkmark-controlled, preface-capable content; `(((name)))` substitution gives you the same generated content dropped anywhere inside ordinary prose, unconditionally.













## Available Dynamic Node/Substitution

`Today`, with `NAME`/heading `(today)`, renders the current date and time.

`AbbrTagNode`, with `NAME`/heading `(kebab-case-of-tag-name)`, renders every abbr entry tagged with that `AbbrTags` member.













## Feeding Render-Time Input

Some dynamic nodes need input that only exists at render time — a search query, for example. Pass that input as an extra keyword argument to `generate_prompt()` / `render.render_prompt_lines()`; it is forwarded to every node's content generation, and each dynamic node picks out the keyword(s) it understands.

```python
prompt = blueprint.generate_prompt(
    query="...",
)
```

A dynamic node that has nothing to key off of ignores keywords it doesn't recognize. `(today)` needs no input at all; it always renders the current date and time.


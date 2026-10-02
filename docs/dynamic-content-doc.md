# Kaye Engine: Dynamic Content Documentation

**Dynamic nodes** are prompt corpus nodes whose content is generated at render time instead of being written by hand, such as today's date. Unlike [sidecar nodes](sidecar-doc.md), dynamic nodes **are** included in the rendered prompt output by default, exactly like a regular corpus section.

Every dynamic node's identity is a canonical **kebab-case** `NAME` slug; its heading is that slug wrapped in parentheses, e.g. `(today)`. That syntax marks a node as dynamic wherever it appears, whether in a tree preview, a blueprint, or an error message. The same `NAME` is also the CLI's `NODE` argument and the placeholder name inside a `(((name)))` inline substitution, see [Dynamic Substitution](#dynamic-substitution). One canonical name, three surfaces, resolved by a single shared function, `resolve_dynamic_node_factory`. Both mechanisms also accept the same extra render-time keyword arguments, see [Feeding Render-Time Input](#feeding-render-time-input).


































## Dynamic Nodes

`DynamicNode` is the abstract class of every dynamic node, a subclass of `BasePromptNode`. Its `NAME` attribute is the canonical slug, and its heading is built from it.













### Identity & Naming

Three kinds of dynamic node exist:

- engine-defined types: one subclass per fixed `NAME`, listed in `DYNAMIC_NODE_TYPES`: `TodayNode` (`today`) and `DecodeOnlyAbbrNode` (`decode-only-abbr`)
- `AbbrTagNode`: parametrized by an `AbbrTags` member instead of being subclassed per tag, one instance per member of `ABBR_TAG_NODE_MEMBERS`; its `NAME` is `slug_for_abbr_tag(abbr_tag)`, the tag's name in kebab case, e.g. `emoji` becomes `(emoji)` and `single_character` becomes `(single-character)`
- `GlossaryNode`: parametrized by a glossary name, one instance per glossary registered via `register_abbr_glossary`, e.g. `(coding-terms)`

`ABBR_TAG_NODE_MEMBERS` holds every simple, single-bit `AbbrTags` member except `always_understand`, which `(decode-only-abbr)` already covers as its no-query fallback. Composite members such as `WORD_CHARACTER` and `ASCII` are excluded.

The abbreviation-related nodes are documented in [`abbrs-doc.md`](abbrs-doc.md#abbreviation-dynamic-nodes). On the CLI, the `NODE` argument is the same slug, e.g. `kaye-engine dn emoji`.













### Leaf Constraint

Every dynamic node is a **leaf**: it never has children, so it cannot contain sub-sections. Attaching a child raises `TypeError`.













### Auto-Attachment

Every dynamic node auto-attaches when a corpus tree is created via `load_corpus_tree`: every engine-defined type, every `ABBR_TAG_NODE_MEMBERS` entry, and every `GlossaryNode` for a glossary registered via `register_abbr_glossary`. You never need to author a `(name)` heading in the corpus just for a dynamic node to exist and be checkmarkable. A registered glossary with no loaded entries still attaches and simply renders empty.

Where it attaches depends on whether the corpus authors that node's `(name)` heading:

- authored, at any nesting depth: the dynamic node takes that heading's exact spot in the tree, in place of it, keeping its position among siblings
- not authored: the node falls back to a direct child of root

There is no special opt-in required. Conditional sidecar nodes, by contrast, are excluded unless explicitly requested via `profile=RenderProfile(conditional_sidecars=...)`, see [`sidecar-doc.md`](sidecar-doc.md#conditional-sidecars).













### Adding Introductory Text (Preface)

A dynamic node's content is generated at render time, so you cannot normally write your own text into it. To put introductory text above a dynamic node's generated content, and to place that node at a specific tree location, write a regular section in the corpus with that dynamic node's exact heading:

```markdown
# (today)

The current date and time, for reference.
```

When the corpus loads, that section is detected and swapped for the dynamic node it names. Its content lines are carried over as the node's `preface=` constructor argument, prepended to the generated lines every time it renders. This applies uniformly to every dynamic node type, since it is implemented once, in the loader. The result is a single `(today)` node, in place of the authored heading, whose output is:

```markdown
The current date and time, for reference.
Date: 2026-08-13
Time: 16:35:45
```

A `(name)` heading resolves against `resolve_dynamic_node_factory`: engine-defined types first, then `AbbrTagNode` slugs, then known glossary names. Loading a corpus **rejects** with `ValueError` a parenthesized heading matching none of the three, and a `(name)` heading authored more than once for the same dynamic node.

Without an authored heading, a dynamic node still attaches, at root with an empty preface, and renders only its generated content.













### Checkmark Control

Once attached, a dynamic node behaves like any other corpus node in a blueprint: checkmark it to include it, uncheckmark it to leave it out.

```python
from kaye_engine.prompt import parse_blueprint_tree, render_prompt

blueprint_text = """ ○
[x] └── (today)"""

blueprint = parse_blueprint_tree(blueprint_text)
prompt = render_prompt(blueprint)
```

Because every dynamic node auto-attaches, `create_blueprint(is_full=True)` checkmarks them too, like any other non-sidecar node. Its output includes today's date and time, the shorthand fallback list, and the full content of every abbreviation tag and every registered glossary.

Unlike a static section, a dynamic node's content is never cached in the corpus index. It is generated live on each render, so it sees the render's keyword arguments, and the tree preview shows its current content.


































## Dynamic Substitution













### Resolution & Headless Rendering

Alongside the tree-child mechanism, `render_prompt()` runs a second, independent pass: any `(((name)))` placeholder appearing anywhere in the fully assembled prompt text is replaced with generated content, unconditionally, whether or not a same-named tree child exists or is checkmarked. This lets you drop generated content into the middle of ordinary prose, not just as a whole checkmark-controlled section. The pass runs in every render mode, the negative prompt included, and before the profile's `sparseness` is applied.

A `name` is looked up in this order:

1. `dynamic_substitution_registry`: a source a consumer registered directly via `register_dynamic_substitution(name, substitution)`; `substitution` must be a `DynamicSubstitution`, otherwise `TypeError`
2. `resolve_dynamic_node_factory`, the resolver the tree mechanism uses, run on a **headless** instance of the matched node (`parent=None`, empty preface), so content generation is identical without ever attaching to the tree

In the second step, an engine-defined type or an `AbbrTagNode` slug always resolves, but a glossary name resolves only when it was registered with `is_dyn_substitution=True`, see [`abbrs-doc.md`](abbrs-doc.md#register_abbr_glossaryname-is_exportable-).

A `DynamicSubstitution` is an abstract class with one method, `generate(**kwargs)`, returning the replacement text. `StringDynamicSubstitution(content)` is the ready-made variant returning a fixed string.

```python
from kaye_engine import (
    StringDynamicSubstitution,
    register_dynamic_substitution,
)

register_dynamic_substitution("project-name", StringDynamicSubstitution("Kaye"))
```

The placeholder name is trimmed of surrounding whitespace, and each distinct name is generated once per render.













### Unconditional, Anywhere-in-Prose

```markdown
Today's date is (((today))), for reference.
```

renders as:

```markdown
Today's date is Date: 2026-08-13
Time: 16:35:45, for reference.
```

An unresolved `name` logs a warning and leaves the literal `(((name)))` text in place. It never raises.

The two mechanisms are independent and both fully functional: `DynamicNode` tree children give you whole-section, checkmark-controlled, preface-capable content; `(((name)))` substitution gives you the same generated content dropped anywhere inside ordinary prose, unconditionally.













### CLI

Two commands print dynamic content without a corpus export:

- `kaye-engine dynamic-node NODE...` (alias `dn`): render one or more dynamic nodes merged into one output; `NODE=ls` lists every available value, and `-t THRESHOLD` hides glossary entries whose priority exceeds it
- `kaye-engine dynamic-substitution NAME` (alias `ds`): print a directly registered substitution's content; `NAME=ls` lists every registered name


































## Available Dynamic Node/Substitution

| `NAME` / heading | Node | Renders |
| --- | --- | --- |
| `today`, `(today)` | `TodayNode` | the current date and time, as a `Date: YYYY-MM-DD` line and a `Time: HH:MM:SS` line |
| `decode-only-abbr`, `(decode-only-abbr)` | `DecodeOnlyAbbrNode` | the abbreviations found in `query=`, else every `always_understand` entry |
| kebab-case of a tag name, such as `(emoji)` | `AbbrTagNode` | every abbreviation entry tagged with that `AbbrTags` member |
| a registered glossary name, such as `(coding-terms)` | `GlossaryNode` | every abbreviation entry of that glossary |

The three abbreviation rows are detailed in [`abbrs-doc.md`](abbrs-doc.md#abbreviation-dynamic-nodes).


































## Feeding Render-Time Input

Some dynamic nodes need input that only exists at render time, a search query for example. Pass that input as an extra keyword argument to `render_prompt()` or `render.render_prompt_lines()`. It is forwarded to every dynamic node's `content_lines()`, and each node picks out the keywords it understands.

```python
prompt = render_prompt(
    blueprint,
    query="...",
)
```

A dynamic node that has nothing to key off of ignores keywords it does not recognize. `(today)` needs no input at all.

The recognized keywords are:

- `query`: the text `(decode-only-abbr)` scans
- `is_sorted`, `is_numbered_list`, `is_remark_disabled`, `is_term_definition_forced`, `glossary_priority_threshold`: the per-render overrides of a `GlossaryNode`, see [`abbrs-doc.md`](abbrs-doc.md#abbreviation-dynamic-nodes)

> [!NOTE]
> The keyword arguments passed to `render_prompt()` reach tree nodes as given. The render profile's own fields (`glossary_priority_threshold`, `is_sorted`, `is_numbered_list`) are merged in for `(((name)))` substitutions only, with an explicit keyword argument winning. To filter or sort a glossary that is a tree node, pass the keyword to `render_prompt()` itself.

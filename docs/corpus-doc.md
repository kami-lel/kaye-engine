# Kaye Engine: `prompt_corpus.md` Format Documentation

<!-- FIXME mpv doc corpus -->

`prompt_corpus.md` is the authoritative Source of Truth for an agent's identity, roles, rules, styles, and references. It describes the logical document format parsed at runtime into a **prompt tree** — `load_corpus_tree` may assemble that logical document from a single file or from an ordered list of sources; either way the parsed result reads as one continuous Markdown document.

`kaye-engine` bundles no corpus of its own — a consumer package supplies and loads the real content.


































## Format

The file is plain Markdown. Each section heading becomes a node in the prompt
tree; the text between headings is that node's content.

A heading-shaped line inside a fenced code block (` ``` `/`~~~`, with or
without a language tag such as ` ```cpp `) is not treated as a real
heading — it stays part of the surrounding node's content, so a code
sample can safely contain lines that start with `#`.

Heading depth maps directly to tree depth:

```md
# Introduction
content of Introduction

## Basic
content of Basic

## Advanced
content of Advanced

# Usage
content of Usage
```

is equivalent to the tree:

```
○
├── Introduction
│   ├── Basic
│   └── Advanced
└── Usage
```

The root node `○` is synthetic — it is never written in the file.

Consecutive empty lines are collapsed to a single empty line during parsing.
Leading and trailing empty lines within a node's content are trimmed.


































## Sidecar Nodes

A **sidecar node** is a section whose heading is wrapped in curly braces. Its roles, descriptors, and rendering are documented in [`sidecar-doc.md`](sidecar-doc.md); this section covers how to write one in the corpus.

A sidecar follows the standard Markdown heading format of the corpus, as set out in [Format](#format):

````markdown
# Parent Node

Content of parent node.

## {description}

This node describes the parent.

## {when_to_use}

This node indicates when to use the parent.

## {globs}

```glob
**/*.py
```

## {avoid}

What the parent's content should not produce.

## {[ClaudeCode:TodoWrite] Usage}

This node contains TodoWrite-specific instructions.
````

Heading conventions:

- depth: a sidecar sits **one level deeper than its parent**
- identification: any heading matching `^\{.+\}$` is a sidecar; there is no fixed vocabulary
- reserved names: `description`, `when_to_use` and `globs` are read through `BlueprintMeta`, and `avoid` is read by the negative render; every other name is free for conditional content
- nesting: a conditional sidecar may carry sidecar children of its own, such as its own `{description}`, since detection applies per node

`get_sidecar_name(node)` from `kaye_engine.prompt.sidecar_node` returns the name inside the braces, or `None` for a node that is not a sidecar:

```python
from kaye_engine.prompt.sidecar_node import get_sidecar_name

name = get_sidecar_name(node)  # "description", "avoid", ..., or None
```

The reserved names are also exported as constants of that module: `AVOID_NAME` publicly, and `DESCRIPTION_NAME`, `WHEN_TO_USE_NAME` and `GLOBS_NAME` for documentation only.













### Checkmarking Behavior

- A sidecar is **never** auto-checkmarked by `create_blueprint(is_full=True)` or by `checkmark_nodes(..., is_recursive=True)`
- A descriptor sidecar is generally not checkmarked at all, since its content is read through the blueprint's `.meta`
- A conditional sidecar is spliced in at render time, and only when its **parent is checkmarked**
- To checkmark a sidecar yourself, name it: `bp = checkmark_nodes(bp, sidecar_node)`













### Affordance and Variant Sidecars

A registered affordance or variant derives its own sidecar names, see [Affordances and Variants](sidecar-doc.md#affordance) for the registry.

Each level derives a `Usage` sidecar and one mirror-opposite sidecar:

| Level | Sidecar | Checkmarked when |
| --- | --- | --- |
| variant | `{[variant canonical_name] Usage}` | that variant is present |
| variant | `{[variant canonical_name] Lack}` | that variant is absent |
| affordance | `{[affordance canonical_name] Usage}` | at least one of its variants is present |
| affordance | `{[affordance canonical_name] Fallback}` | every one of its variants is absent |

Author each affordance and variant sidecar under a checkmarked node, one level deeper than its parent, describing what to do in that case, per [Sidecar Nodes](#sidecar-nodes). An affordance with no registered variant never fires either of its sidecars.

> [!WARNING]
> Both levels use the literal suffix `Usage`. An affordance and a variant sharing one `canonical_name` collide on a single sidecar key, so keep the names unique across both registries.

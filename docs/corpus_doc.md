# `prompt_corpus.md` Format Documentation

`prompt_corpus.md` is the authoritative Source of Truth for the Kaye persona,
roles, rules, styles, and references. It is a single continuous Markdown file
parsed at runtime into a **prompt tree**.













## Format

The file is plain Markdown. Each section heading becomes a node in the prompt
tree; the text between headings is that node's content.

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













## Meta Nodes

**Meta nodes** are corpus nodes whose names are enclosed in curly braces, e.g. `{description}`. They can be attached to any node in the prompt tree and hold structured metadata about their parent. Meta nodes appear in the blueprint preview tree but are **not** included in the rendered prompt output.

Four meta node types are defined:





### `{description}`

Describes the parent node's functionality — what the node represents or what it instructs.






### `{when_to_use}`

Indicates when the parent node should be enabled — the conditions or contexts that make the node relevant.





### `{globs}`

Lists file glob patterns that indicate which file types or paths make the parent node relevant. Each line is treated as a separate pattern — multiple patterns are supported.

E.g.:

    ### Python Files

    #### {globs}

    ```glob
    **/*.py
    **/*.pyi
    ```





### `{prerequisite}`

Lists prerequisite instructions that apply whenever the parent node is enabled.
Pass `contains_prerequisite_nodes=True` to `generate_prompt()` or
`generate_prompt_lines()` to auto-checkmark every `{prerequisite}` node whose
parent is already checkmarked before rendering. A node is recognized via
`BasePromptNode.is_prerequisite_node` (it checks `self.name == "{prerequisite}"`).

# Kaye Engine: `prompt_corpus.md` Format Documentation

`prompt_corpus.md` is the authoritative Source of Truth for an agent's identity, roles, rules, styles, and references. It is a single continuous Markdown file parsed at runtime into a **prompt tree**.

`kaye-engine` bundles no corpus of its own — a consumer package supplies and loads the real file.


































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

Q.v. [`Sidecar Node Documentation`](sidecar-node-doc.md) for comprehensive documentation on sidecar nodes.

# Kaye Engine: `prompt_corpus.md` Format Documentation

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

Q.v. [`Sidecar Node Documentation`](sidecar-node-doc.md) for comprehensive documentation on sidecar nodes.

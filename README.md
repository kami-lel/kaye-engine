# Kaye README

> Consistent AI Agent Persona **Kaye**, powered by rigorous prompt engineering

Kaye is a toolkit for maintaining a consistent AI agent persona from a single, structured source of truth. The project focuses on producing scenario-ready prompts from a central Markdown corpus using blueprints with APIs and CLI.

### ✨ Features

- 📌 single Source Of Truth for persona, roles, and rules
- ⚙️ generate scenario-ready prompts from blueprints and templates
- 🐍 programmatic Python API for listing, previewing, and generating prompts
- 🌐 HTTP endpoints for dynamic prompt generation via a lightweight Flask service
- 💻 CLI for quick local generation and inspection












## 🧩 Core Concepts

### 📄 Prompt Corpus

The [Prompt Corpus](kaye/prompt_corpus.md) is the single, structured Markdown file that defines persona, roles, rules, styles, and references. It is the authoritative Source Of Truth used to generate prompts for different scenarios.

Q.v. [Prompt Corpus Format documentation](docs/corpus_doc.md) for the heading-to-tree mapping and full Markdown syntax.

----

Other core concepts:

- 🎭 role: task-specific **Behavior Profile** inside the corpus shaping response style and scope
- 📝 prompt: final **Rendered Text** tailored to a context and ready for direct use
- 🌲 blueprint: tree **Selection Spec** that controls which corpus parts are rendered
- 🔀 dynamic node: corpus node whose content is **Generated** at render time — Q.v. [Dynamic Node documentation](docs/dynamic_node_doc.md)
- 🗂️ sidecar node: corpus node holding structured **Metadata** about its parent — Q.v. [Sidecar Node documentation](docs/sidecar_node_doc.md)

The `(Abbreviations)` dynamic node reads its meanings from [`kaye/abbrs.json`](kaye/abbrs.json) — Q.v. [`abbrs.json` documentation](docs/abbrs_json_doc.md) for its format.

### 🎭 Personas

Beyond Kaye, the corpus defines sibling personas **Ria** and **Zin** for comparison and reuse.

Q.v. [Personalities documentation](docs/personalities_doc.md) for an axis-by-axis comparison.


































## Usage

### Programmatic API

The **Kaye Programmatic API** provides *Python programmatic access* to list corpus entries, preview sections, and generate concrete prompts.

Q.v. [Kaye Programmatic API documentation](docs/programmatic_api_doc.md)













### HTTP API

The **Kaye HTTP API** uses *Flask* to provide endpoints for requesting rendered prompts and previews dynamically.

Q.v. [Kaye HTTP API documentation](docs/http_api_doc.md)













### Python CLI

A simple **Kaye Python CLI** is provided, exposed as the `kaye` command once
installed (or run as `python -m kaye`):

```bash
kaye --help
```













### Using Kaye with Claude

Package Kaye as a Claude Desktop plugin or wire it into the Claude Code
VS Code Extension.

Q.v. [Using Kaye with Claude documentation](docs/claude_doc.md)













### Using Kaye with Dify

A Dify App wires Kaye into a chat workflow, round by round.

Q.v. [Dify App Kaye Chat documentation](docs/ky_doc.md)













### Kaye Commit Sense

Commit messages carry a leading **Sigil** summarizing the nature of the
change (added, deleted, moved, refactored, ~~).

Q.v. [Kaye Commit Sense documentation](docs/kaye_commit_sense_doc.md)

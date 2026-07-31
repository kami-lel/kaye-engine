# Kaye Engine README

> Consistent AI Agent Identity, powered by rigorous prompt engineering

Kaye Engine is a toolkit for maintaining a consistent AI agent identity from a single, structured source of truth. The project focuses on producing scenario-ready prompts from a central Markdown corpus using blueprints with APIs and CLI.

### ✨ Features

- 📌 single Source Of Truth for identity, roles, and rules
- ⚙️ generate scenario-ready prompts from blueprints and templates
- 🐍 programmatic Python API for listing, previewing, and generating prompts
- 🌐 HTTP endpoints for dynamic prompt generation via a lightweight Flask service
- 💻 CLI for quick local generation and inspection












## 🧩 Core Concepts

### 📄 Prompt Corpus

The **Prompt Corpus** is a single, structured Markdown file that defines identity, roles, rules, styles, and references — the authoritative Source Of Truth used to generate prompts for different scenarios. `kaye-engine` does not bundle one itself; it only provides the parsing mechanism (`load_corpus_tree()` / `get_corpus_tree()`) that any caller uses to load and cache one by name.

Q.v. [Prompt Corpus Format documentation](docs/corpus_doc.md) for the heading-to-tree mapping and full Markdown syntax.

----

Other core concepts:

- 🎭 role: task-specific **Behavior Profile** inside the corpus shaping response style and scope
- 📝 prompt: final **Rendered Text** tailored to a context and ready for direct use
- 🌲 blueprint: tree **Selection Spec** that controls which corpus parts are rendered
- 🔀 dynamic node: corpus node whose content is **Generated** at render time — Q.v. [Dynamic Node documentation](docs/dynamic_node_doc.md)
- 🗂️ sidecar node: corpus node holding structured **Metadata** about its parent — Q.v. [Sidecar Node documentation](docs/sidecar_node_doc.md)

The `(Abbreviations)` dynamic node reads its meanings from an `abbrs.json` file loaded via `populate_abbr_data_with_json_file`/`get_abbr_data` — kaye-engine bundles no copy of its own; a separate host package supplies and loads the real file. Q.v. [`abbr_collection` documentation](docs/abbr_collection_doc.md) for its schema, top-level functions, and where abbreviations are used.


































## Usage

### Programmatic API

The **Kaye Engine Programmatic API** provides *Python programmatic access* to list corpus entries, preview sections, and generate concrete prompts.

Q.v. [Kaye Engine Programmatic API documentation](docs/programmatic_api_doc.md)













### Python CLI

A simple **Kaye Engine Python CLI** is provided, exposed as the `kaye-engine` command
once installed (or run as `python -m kaye_engine`):

```bash
kaye-engine --help
```













### Using Kaye Engine with Claude

Package Kaye Engine as a Claude Desktop plugin or wire it into the Claude Code
VS Code Extension.

Q.v. [Using Kaye Engine with Claude documentation](docs/claude_doc.md)













### Using Kaye Engine with Dify

A Dify App wires Kaye Engine into a chat workflow, round by round.

Q.v. [Dify App Kaye Chat documentation](docs/ky_doc.md)

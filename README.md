# Kaye Engine README

> Consistent AI Agent Identity, powered by rigorous prompt engineering

Kaye Engine parses a plain Markdown file, as the structured single source of truth for LLM instructions, then renders scenario-ready prompt assets through blueprints, a programmatic API, and a CLI.

### ✨ Features

- 📌 single Source Of Truth for an LLM's prompt assets
- ⚙️ generate scenario-ready prompts from blueprints and templates
- 🐍 programmatic Python API for listing, previewing, and generating prompts
- 💻 CLI for quick local generation and inspection
- 🔌 pluggable mechanism, ready for a consumer package to plug in its own corpus, abbreviations, and blueprints — including a Flask/HTTP surface, if the consumer chooses to build one












## 🧩 Core Concepts

### 📄 Prompt Corpus

The **Prompt Corpus** is a single, structured Markdown file that defines identity, roles, rules, styles, and references — the authoritative Source Of Truth used to generate prompts for different scenarios. `kaye-engine` does not bundle one itself; it only provides the parsing mechanism (`load_corpus_tree()` / `get_corpus_tree()`) that any caller uses to load and cache one by name.

Q.v. [Prompt Corpus Format documentation](docs/corpus-doc.md) for the heading-to-tree mapping and full Markdown syntax.

----

Other core concepts:

- 🎭 role: task-specific **Behavior Profile** inside the corpus shaping response style and scope
- 📝 prompt: final **Rendered Text** tailored to a context and ready for direct use
- 🌲 blueprint: tree **Selection Spec** that controls which corpus parts are rendered
- 🔀 dynamic node: corpus node whose content is **Generated** at render time — Q.v. [Dynamic Node documentation](docs/dynamic-node-doc.md)
- 🗂️ sidecar node: corpus node holding structured **Metadata** about its parent — Q.v. [Sidecar Node documentation](docs/sidecar-node-doc.md)

The `(Decode-Only Shorthand)` dynamic node reads its meanings from an `abbrs.json` file loaded via `populate_abbr_data_with_json_file`/`get_abbr_data` — kaye-engine bundles no copy of its own; a separate consumer package supplies and loads the real file. Q.v. [`abbr_collection` documentation](docs/abbr-collection-doc.md) for its schema, top-level functions, and where abbreviations are used.


































## Usage

### Programmatic API

The **Kaye Engine Programmatic API** provides *Python programmatic access* to list corpus entries, preview sections, and generate concrete prompts.

Q.v. [Kaye Engine Programmatic API documentation](docs/programmatic-api-doc.md)













### Python CLI

A simple **Kaye Engine Python CLI** is provided, exposed as the `kaye-engine` command
once installed (or run as `python -m kaye_engine`):

```bash
kaye-engine --help
```













### Using Kaye Engine with Claude

Package Kaye Engine as a Claude Desktop plugin or wire it into the Claude Code
VS Code Extension.

Q.v. [Using Kaye Engine with Claude documentation](docs/claude-doc.md)














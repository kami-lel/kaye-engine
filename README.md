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

----

Other core concepts:

- 🎭 role: task-specific **Behavior Profile** inside the corpus shaping response style and scope
- 📝 prompt: final **Rendered Text** tailored to a context and ready for direct use
- 🌲 blueprint: tree **Selection Spec** that controls which corpus parts are rendered











## Usage

### Programmatic API

The **Kaye Programmatic API** provides *Python programmatic access* to list corpus entries, preview sections, and generate concrete prompts.

Q.v. [Kaye Programmatic API documentation](docs/programmatic_api_doc.md)





### HTTP API

The **Kaye HTTP API** uses *Flask* to provide endpoints for requesting rendered prompts and previews dynamically.

Q.v. [Kaye HTTP API documentation](docs/http_api_doc.md)





### Python CLI

A simple **Kaye Python CLI** is provided:

```bash
python -m kaye --help
```



### Using Kaye with Claude

#### Claude Desktop

Generate a plugin package using the Kaye CLI:

```bash
python -m kaye claude plugin --zip  # or
python -m kaye a p -z
```

Upload the generated `.zip` file to [Claude Desktop](https://claude.ai) settings under *Plugins* to enable Kaye integration.

#### Claude Code VS Code Extension

Set up Kaye for the Claude Code VS Code Extension with one command:

```bash
python -m kaye claude vs-code-extension  # or
python -m kaye a v
```

This writes the User System Prompt to `~/.claude/CLAUDE.md`, creates a
`~/.claude/kaye_marketplace/` folder containing the kaye plugin, and
configures a `PreCompact` hook in `~/.claude/settings.json` so session
changes are logged before context is compacted.

To load the marketplace in VS Code:

1. Open the *Claude* sidebar in VS Code.
2. Go to *Settings* → *Marketplaces*.
3. Add the path to `~/.claude/kaye_marketplace/` and click *Install*.

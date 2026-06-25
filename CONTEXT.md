# kaye CONTEXT

System knowledge for the **Kaye** repository — architecture, entities, and
boundaries. Read this alongside `AGENTS.md` before making changes.

## Project Overview

**Kaye** is a prompt-engineering toolkit that maintains a consistent AI agent
persona from a single, structured Source Of Truth. It renders scenario-ready
prompts from a central Markdown corpus using tree-based blueprints, exposed
through a Python API, an HTTP API, and a CLI.

- language: Python (`>=3.11`)
- package name: `kaye` (distribution and import name; `PROGRAM_NAME` in
  `kaye/__init__.py`, paired with `DISPLAY_NAME` = `"Prompt Engineering Project
  Kaye"` used as the Claude plugin `displayName`)
- core dependencies: `anytree`, `flask`, `pyahocorasick`, `pyyaml`
- entry point: `python -m kaye` (CLI; `http` subcommand starts the Flask app)

### Key Concepts

- **Prompt Corpus** — `kaye/prompt_corpus.md`, the authoritative Source Of
  Truth defining persona, roles, rules, styles, and references
- **Prompt Tree** — parsed corpus; each section heading is a `BasePromptNode`
- **Blueprint** — a `PromptBlueprint` tree selection spec controlling which
  corpus parts render into a concrete prompt
- **Role** — task-specific behavior profile inside the corpus
- **Meta Node** — `{name}`-bracketed subnode holding structured metadata for
  its parent (members of `kaye/prompt/meta_node_type.py::MetaNodeType`:
  `DESCRIPTION`, `WHEN_TO_USE`, `GLOBS`, `PREREQUISITE`; `.as_node_heading`
  renders e.g. `{description}`); detected via `BasePromptNode.is_meta_node`
  (regex `^\{.+\}$`); looked up and rendered by
  `kaye/prompt/blueprint_meta_nodes.py::BlueprintMetaNodes`. To add a new meta
  node type: add a member to `MetaNodeType`, add a property + `_node` lookup
  (via `MetaNodeType.<NAME>.as_node_heading`) in `BlueprintMetaNodes`, add
  `### {name}` examples to `kaye/prompt_corpus.md`,
  document it in `docs/corpus_doc.md` and `docs/programmatic_api_doc.md`, wire
  CLI export consumers (`kaye/cli/frontmatter_md_file.py`,
  `kaye/cli/cli_continue/rule_file.py`) if the type should surface in exports,
  and mirror tests under `tests/prompt/bp/` and `tests/prompt/node/`.
- **Prerequisite Node** — `{prerequisite}` meta node; `MetaNodeType
  .is_prerequisite(node)` checks `node.name == "{prerequisite}"`;
  pass `contains_prerequisite_nodes=True` to `generate_prompt()` /
  `generate_prompt_lines()` to auto-checkmark every `{prerequisite}` node
  whose parent is already checkmarked before rendering.

### Prompt Corpus Structure

`kaye/prompt_corpus.md` is one large Markdown document parsed into the prompt
tree. Each `#`/`##`/`###` heading becomes a node; `{name}` headings are meta
nodes (see above). Blank "spacer" lines between sections are intentional —
preserve them. The top-level (`#`) sections, in order:

- **Introduction** — defines Kaye as an AI agent serving the user
- **Personality** — the Kaye persona: submissive/deferential voice, emotion
  expression rules (blockquote `>` for emotions, `----` separators between
  explanation and emotion)
- **Language** — respond in the user's language; never mix languages in one
  reply
- **Style Guide** — `Markdown Format`, `Capitalization` (Title Case /
  Commentary Case), `Briefness Style`, `Good Writing` — the *style* blueprints
- **Elements** — reusable formatting fragments: `Date and Time Format`,
  `Numerical Values with Units`, `Annotation Markers`, `International Phonetic
  Alphabet`
- **Kaye Chat** — `sense`/`merge` selection logic driving role, difficulty,
  and `programming_languages` resolution for the `Chat` blueprint
- **Role** — task personas: `Art Tutor`, `Assistant Barista`, `Deutschlehrer`,
  `Editor`, `Librarian`, `Secretary`, `Tarot Reader`
- **Projects** — `Project Structure`, `Project Semantic Versioning`, the
  `README`/`CHANGELOG`/`AGENTS` writers, and project workflow prompts: `Create
  README`, `Maintain README`, `Create CHANGELOG`, `Maintain CHANGELOG`,
  `Create AGENTS and CONTEXT`, `Maintain AGENTS and CONTEXT`, `Create Docs`,
  `Maintain Docs`, `Initialize Project`, `Compact with Maintenance`, `Prepare
  for Feature Finish`, `Prepare for Version Release`
- **Prompt Engineering** — `Prompt Writer`, `Skill Description Writer`
- **Kaye Cash Tracker** / **Kaye Commit Sense** / **Kaye Event Radar** —
  standalone task prompts (expense extraction, commit-message generation,
  event parsing/filtering)
- **Kaye Peer Coder** — shared coder rules (`code format`, `variable naming`,
  `code comment`, `Brace Style`) plus per-language coder profiles: `Bash`,
  `C`, `CPP`, `Unreal Engine`, `C Sharp`, `Unity Engine`, `GDScript`, `HTML`,
  `JavaScript and TypeScript`, `Python` (with `Docstring Style` and `Testing
  Guidelines` sub-profiles)
- **Opus Tag Smith** — media tagging (title/subtitle, release year, tags)
- **Agent Behavior** — baseline agent conduct; `Continue Behavior` is a
  subsection (e.g. `run_terminal_command`)
- **Utility Prompts** — Conversation Follow Up / Tag / Title generation

Most leaf sections that back an exportable blueprint carry `{description}` and
`{when_to_use}` meta nodes; coder and writer sections add `{globs}` and
`{prerequisite}`.

## Repository Layout

- `kaye/` — main package (API, CLI, prompt engine, abbreviation collection)
  - `kaye/prompt/` — prompt tree, nodes, blueprints, loaders
  - `kaye/api/` — Flask HTTP API and Dify app endpoints
  - `kaye/cli/` — argparse-based CLI subcommands
    - `kaye/cli/cli_continue/` — exports blueprint/abbreviation rules to
      `~/.continue`
    - `kaye/cli/claude/` — exports blueprints as Claude plugins, marketplaces,
      agentskills.io Skills, VS Code Extension setup, and the user system
      prompt `CLAUDE.md`
    - `kaye/cli/cli_prompt/` — prompt generation CLI subcommands
  - `kaye/prompt_corpus.md`, `kaye/abbrs.json` — packaged data
- `dify_studio/` — Dify workflow node sources (not part of the package)
- `docs/` — in-depth documentation (API, HTTP, CLI, abbreviations)
- `tests/` — `pytest` suite, mirrors the package structure
  - `tests/prompt/` — unit tests for the prompt engine (nodes, blueprints)
    - `tests/prompt/bp/` — `PromptBlueprint` tests
    - `tests/prompt/node/` — `PromptCorpusNode` / `BasePromptNode` tests
  - `tests/api/` — HTTP API and Dify app endpoint tests
  - `tests/cli/` — CLI integration tests; `tests/cli/__init__.py` holds
    `MD_FILENAME2SKILL_NAME` (skill slug → display name) and
    `TESTEE_FILE_CONTENT_ALL` (skill slug → expected content strings)
    - `tests/cli/a/` — `claude` subcommand tests
      - `tests/cli/a/c/` — `claude code` export tests (CLAUDE.md, plugin.json,
        skill files, command aliases)
      - `tests/cli/a/m/` — `claude marketplace` export tests (file structure,
        marketplace.json content, command aliases)
      - `tests/cli/a/p/` — `claude plugin` export tests (skill files,
        plugin.json content, command aliases)
      - `tests/cli/a/cz/` — `claude plugin -z` (zipped package) tests
      - `tests/cli/a/s/` — `claude skill` export tests
        - `tests/cli/a/s/structure/` — structure/exportability tests for every
          blueprint in `__all__`
          (`cli-a-s-structure-exportable_blueprints_test.py`) and prompt
          blueprints
        - `tests/cli/a/s/coder/` — per-skill content tests for coder blueprints
        - `tests/cli/a/s/others/` — per-skill content tests for miscellaneous
          blueprints (chat, triage-tags, date-time, IPA, etc.)
        - `tests/cli/a/s/proj/` — per-skill content tests for project blueprints
        - `tests/cli/a/s/role/` — per-skill content tests for role blueprints
        - `tests/cli/a/s/style/` — per-skill content tests for style blueprints
        - `tests/cli/a/s/pe/` — per-skill content tests for prompt-engineering
          blueprints
      - `tests/cli/a/sz/` — `claude skill -z` (zipped packages) tests
      - `tests/cli/a/u/` — `claude user-system-prompt` export tests (content,
        flags, aliases)
      - `tests/cli/a/v/` — `claude vs-code-extension` export tests (CLAUDE.md,
        marketplace, command aliases)
    - `tests/cli/c/` — `continue` subcommand tests
  - `tests/abbr/` — abbreviation collection tests
- `scripts/` — Git hooks and the `systemd` service file


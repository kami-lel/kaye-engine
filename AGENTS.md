----
name: kaye AGENTS.md
alwaysApply: true
----

# kaye AGENTS.md

Guidance for AI coding agents working in the **Kaye** repository. This file is
agent-readable context: read it before making changes, and follow the exact
commands and conventions below.

## Project Overview

**Kaye** is a prompt-engineering toolkit that maintains a consistent AI agent
persona from a single, structured Source Of Truth. It renders scenario-ready
prompts from a central Markdown corpus using tree-based blueprints, exposed
through a Python API, an HTTP API, and a CLI.

- language: Python (`>=3.11`)
- package name: `Kaye` (import as `kaye`)
- core dependencies: `anytree`, `flask`, `pyahocorasick`
- entry point: `python -m kaye` (CLI; `http` subcommand starts the Flask app)

### Key Concepts

- **Prompt Corpus** — `kaye/prompt_corpus.md`, the authoritative Source Of
  Truth defining persona, roles, rules, styles, and references
- **Prompt Tree** — parsed corpus; each section heading is a `BasePromptNode`
- **Blueprint** — a `PromptBlueprint` tree selection spec controlling which
  corpus parts render into a concrete prompt
- **Role** — task-specific behavior profile inside the corpus
- **Meta Node** — `{name}`-bracketed subnode holding structured metadata for
  its parent (e.g. `{description}`, `{when_to_use}`, `{globs}`, `{prerequisite}`);
  detected via `BasePromptNode.is_meta_node` (regex `^\{.+\}$`); looked up and
  rendered by `kaye/prompt/blueprint_meta_nodes.py::BlueprintMetaNodes`. To add
  a new meta node type: add a property + `_node` lookup in
  `BlueprintMetaNodes`, add `### {name}` examples to `kaye/prompt_corpus.md`,
  document it in `docs/corpus_doc.md` and `docs/programmatic_api_doc.md`, wire
  CLI export consumers (`kaye/cli/frontmatter_md_file.py`,
  `kaye/cli/cli_continue/rule_file.py`) if the type should surface in exports,
  and mirror tests under `tests/prompt/bp/` and `tests/prompt/node/`.
- **Prerequisite Node** — `{prerequisite}` meta node; `BasePromptNode
  .is_prerequisite_node` checks `self.name == "{prerequisite}"`;
  `PromptBlueprint.checkmark_prerequisite_nodes()` recursively checkmarks
  every `{prerequisite}` node whose parent is already checkmarked.

### Repository Layout

- `kaye/` — main package (API, CLI, prompt engine, abbreviation collection)
  - `kaye/prompt/` — prompt tree, nodes, blueprints, loaders
  - `kaye/api/` — Flask HTTP API and Dify app endpoints
  - `kaye/cli/` — argparse-based CLI subcommands
    - `kaye/cli/cli_continue/` — exports blueprint/abbreviation rules to `~/.continue`
    - `kaye/cli/cli_claude/` — exports blueprints as Claude plugins and agentskills.io Skills
    - `kaye/cli/cli_prompt/` — prompt generation CLI subcommands
  - `kaye/prompt_corpus.md`, `kaye/abbrs.json` — packaged data
- `dify_studio/` — Dify workflow node sources (not part of the package)
- `docs/` — in-depth documentation (API, HTTP, CLI, abbreviations)
- `tests/` — `pytest` suite, mirrors the package structure
- `scripts/` — Git hooks and the `systemd` service file

## Build and Test

Set up a virtual environment and install in editable mode:

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

Run the full test suite:

```bash
pytest
```

Run a single test file or test:

```bash
pytest tests/cli/c/p/cli-c-p-maintain_changelog_test.py
pytest tests/cli/c/p/cli-c-p-maintain_changelog_test.py::TestHeader::test_name
```

Run the CLI and HTTP API locally:

```bash
python -m kaye --help          # show CLI usage
python -m kaye http            # start Flask HTTP API (port 11255)
python -m kaye continue config                  # export rules to ~/.continue
python -m kaye continue config LOCAL_CONFIG_FOLDER  # export to custom path
python -m kaye continue prompt PROMPTS_FOLDER        # export Continue prompts
python -m kaye claude skill SKILLS_FOLDER            # export blueprints as Skill folders
python -m kaye claude skill -z ZIPS_FOLDER           # create .zip Skill packages
python -m kaye claude plugin PLUGINS_FOLDER          # export blueprints as plugin folder
python -m kaye claude plugin -z PLUGINS_FOLDER       # create .plugin file
```

CLI subcommand aliases: `http` → `h`; `continue` → `c`;
`continue config` → `c c`; `continue prompt` → `c p`;
`claude` → `anthropic`, `a`; `claude plugin` → `claude p`;
`claude skill` → `claude s`.

## Code Conventions

- follow **PEP 8**; keep lines within **80 characters**
- use **Sphinx**-style docstrings written in **reStructuredText**
- public methods must have docstrings; private methods (`_` prefix) only when
  the name is not self-explanatory
- test files end with `_test.py` and mirror the source tree under `tests/`
- test classes are grouped as `TestStructure`, `TestHeader`, `TestContent`
- use comment section headings (`#`, `=`, `*`, `+`, `-`) only for long files

## Annotation Markers

The codebase uses `TODO`, `FIXME`, `BUG`, and `HACK` markers. When resolving a
primary marker, implement the task and remove the marker. Do not touch markers
unrelated to your current change.

## Security

- do not commit secrets, credentials, or tokens
- `.git`, `venv/`, build artifacts, and generated prompts are git-ignored;
  keep them out of commits
- the Git submodule `scripts/hooks_utility` is fetched via SSH; do not embed
  credentials in `.gitmodules`
- the HTTP API is intended for trusted local or internal deployment; do not
  expose it publicly without review

## Documentation Maintenance

After meaningful changes, keep these in sync:

- `README.md` — human-facing overview and quick start
- `docs/` — programmatic API, HTTP API, CLI, abbreviations
- `CHANGELOG.md` — record notable changes per release
- this `AGENTS.md` — update agent-specific context as structure evolves

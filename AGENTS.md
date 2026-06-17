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
- **Prerequisite Node** — `{prerequisite}` meta node; `BasePromptNode
  .is_prerequisite_node` checks `self.name == "{prerequisite}"`;
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
- **Projects** — `Project Structure`, `Project Semantic Versioning`, and the
  `README`/`CHANGELOG`/`AGENTS` writers, plus `project prompts` (Maintain Docs,
  Maintain CHANGELOG, Create README, Create AGENTS, Prepare for Feature Finish,
  Prepare for Release)
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
- **Agent Behavior** / **Continue Behavior** — baseline agent conduct and
  Continue-specific behavior (e.g. `run_terminal_command`)
- **Utility Prompts** — Conversation Follow Up / Tag / Title generation

Most leaf sections that back an exportable blueprint carry `{description}` and
`{when_to_use}` meta nodes; coder and writer sections add `{globs}` and
`{prerequisite}`.

### Repository Layout

- `kaye/` — main package (API, CLI, prompt engine, abbreviation collection)
  - `kaye/prompt/` — prompt tree, nodes, blueprints, loaders
  - `kaye/api/` — Flask HTTP API and Dify app endpoints
  - `kaye/cli/` — argparse-based CLI subcommands
    - `kaye/cli/cli_continue/` — exports blueprint/abbreviation rules to `~/.continue`
    - `kaye/cli/cli_claude/` — exports blueprints as Claude plugins,
      marketplaces, agentskills.io Skills, a Claude Code `.claude/` folder, and
      the user system prompt `CLAUDE.md`
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
      - `tests/cli/a/s/` — `claude skill` export tests
        - `tests/cli/a/s/structure/` — structure/exportability tests for every
          blueprint in `__all__` (`cli-a-s-structure-exportable_blueprints_test.py`)
          and prompt blueprints
        - `tests/cli/a/s/coder/` — per-skill content tests for coder blueprints
        - `tests/cli/a/s/others/` — per-skill content tests for miscellaneous
          blueprints (chat, annotation-markers, date-time, IPA, etc.)
        - `tests/cli/a/s/proj/` — per-skill content tests for project blueprints
        - `tests/cli/a/s/role/` — per-skill content tests for role blueprints
        - `tests/cli/a/s/style/` — per-skill content tests for style blueprints
        - `tests/cli/a/s/pe/` — per-skill content tests for prompt-engineering
          blueprints
    - `tests/cli/c/` — `continue` subcommand tests
  - `tests/abbr/` — abbreviation collection tests
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
python -m kaye claude plugin -z PLUGINS_FOLDER       # create .plugin file (-n omits version)
python -m kaye claude marketplace MARKETPLACE        # export a marketplace folder (plugin under plugins/)
python -m kaye claude code                           # export plugin + CLAUDE.md into ~/.claude
python -m kaye claude user-system-prompt             # export Chat blueprint to ~/.claude/CLAUDE.md
```

CLI subcommand aliases: `http` → `h`; `continue` → `c`;
`continue config` → `c c`; `continue prompt` → `c p`;
`claude` → `anthropic`, `a`; `claude plugin` → `claude p`;
`claude skill` → `claude s`; `claude marketplace` → `claude m`;
`claude code` → `claude c`; `claude user-system-prompt` → `claude u`.

## Code Conventions

- follow **PEP 8**; keep lines within **80 characters**
- use **Sphinx**-style docstrings written in **reStructuredText**
- public methods must have docstrings; private methods (`_` prefix) only when
  the name is not self-explanatory
- test files end with `_test.py` and mirror the source tree under `tests/`
- test classes are grouped as `TestStructure`, `TestHeader`, `TestContent`
- use comment section headings (`#`, `=`, `*`, `+`, `-`) only for long files

## Adding an Exportable Blueprint

To add a blueprint that appears in both `claude skill` and `continue config`
exports, touch these locations in order:

1. **`kaye/prompt/embedded_blueprints.py`** — define the variable and add its
   name to `__all__` (controls the `*` import into `kaye/cli/__init__.py`)
2. **`kaye/cli/__init__.py` → `EXPORTABLE_BLUEPRINTS`** — append the blueprint
   object; this is the actual gate for CLI export; omitting it causes "file not
   found" in tests even though import works
3. **`tests/cli/__init__.py`** — add entries to both:
   - `MD_FILENAME2SKILL_NAME`: `"kebab-slug": "Display Name"`
   - `TESTEE_FILE_CONTENT_ALL`: `"kebab-slug": ["string1", "string2", ...]`
4. **`tests/cli/a/s/structure/cli-a-s-structure-exportable_blueprints_test.py`**
   — add a `test_<name>()` calling `validate_blueprint(bp)`
5. **`tests/cli/a/s/<group>/cli-a-s-<group>-<slug>_test.py`** — per-skill
   content test (classes `TestBasic`, `TestHeader`, `TestStructure`,
   `TestContent`); group folders: `coder/`, `proj/`, `style/`, `pe/`,
   `others/` (catch-all incl. Elements nodes), `role/` (Role section)
6. **`tests/cli/c/c/<group>/cli-c-c-bp-<slug>_test.py`** — continue config
   content test; fixture is `testee_rules_folder / (display_name + ".md")`
   (file named by display name, not kebab slug)

### YAML-quoting gotcha in `c/c` `test_description`

Descriptions that contain `/`, `—`, or `↵` (U+21B5, the separator between
`{description}` and `{when_to_use}`) are double-quoted by PyYAML with unicode
escapes. The resulting header line is too long to match exactly. Use:

```python
def test_description(_, testee_header):
    assert any("distinctive keyword" in line for line in testee_header)
```

instead of `"description: X" in testee_header` (exact list-membership check).

### `always_apply` for new blueprints

Defaults to `False`. Only `"Chat"`, `"Coder"`, `"Agent Behavior"`,
`"Continue Behavior"` are in `_ALWAYS_APPLY_BLUEPRINT`
(`kaye/cli/cli_continue/export_blueprint_rules.py`).

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

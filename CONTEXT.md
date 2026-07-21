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
- core dependencies: `anytree`, `flask`, `json5`, `pyahocorasick`, `pyyaml`
- entry point: `kaye` console script (`[project.scripts]` in
  `pyproject.toml`, mapped to `kaye.__main__:main`); `python -m kaye` still
  works identically. `http` subcommand starts the Flask app

### Key Concepts

- **Prompt Corpus** — `kaye/prompt_corpus.md`, the authoritative Source Of
  Truth defining persona, roles, rules, styles, and references
- **Prompt Tree** — parsed corpus; each section heading is a `BasePromptNode`
- **Blueprint** — a `PromptBlueprint` tree selection spec controlling which
  corpus parts render into a concrete prompt
- **Role** — task-specific behavior profile inside the corpus
- **Sidecar Node** — `{name}`-bracketed subnode attached to a blueprint's
  parent but stored as corpus content; excluded by default and conditionally
  spliced in via `contains_sidecars` (`kaye/prompt/sidecar_nodes/`). There is
  no fixed enum of sidecar names — `get_sidecar_name(node)` (regex
  `^\{.+\}$`, returns `None` if not a sidecar node) extracts the name inside
  the braces as a plain string. Two usage-role labels under the same
  mechanism, not separate classes: *descriptor sidecar* for `{description}`,
  `{when_to_use}`, `{globs}` (reserved names, consumed as blueprint metadata
  by `BlueprintDescriptorSidecars` via plain string-key lookup, exposed as
  `blueprint.sidecars`) and *conditional sidecar* for any other name, e.g.
  `{prerequisite}`, `{for-claude-code}` (real prompt content spliced in
  conditionally when its name is passed in `contains_sidecars`). Because
  detection is name-based rather than type-based, a reserved descriptor name
  can also be requested via `contains_sidecars` for conditional content
  inclusion — nothing structurally prevents it. To add a new conditional
  sidecar name: add `### {name}` examples to `kaye/prompt_corpus.md`,
  document it in `docs/corpus_doc.md`, `docs/sidecar_node_doc.md`, and
  `docs/programmatic_api_doc.md`, wire CLI export consumers
  (`kaye/cli/claude/skill/skill_md.py`, `kaye/cli/cli_continue/rule_file.py`,
  both built on the shared `kaye/cli/frontmatter_doc.py`) if the name should
  surface in exports, and mirror tests under `tests/prompt/bp/` and
  `tests/prompt/node/`.
- **Prerequisite Node** — `{prerequisite}` conditional sidecar node; pass
  `contains_sidecars=("prerequisite",)` (or a larger collection) to
  `generate_prompt()` / `render.render_prompt_lines()` to auto-checkmark
  every matching sidecar node whose parent is already checkmarked before
  rendering; `"for-claude-code"` and `"prerequisite"` are combined in
  `kaye.cli.claude.CONTAINING_SIDECARS` for all Claude exports
- **Blueprint Sidecar Merging** — `BlueprintDescriptorSidecars.__or__` merges
  two instances via `left | right`; left operand takes priority for each
  field (description, when_to_use, globs, prerequisite); `PromptBlueprint.__or__`
  now includes sidecar merging so merged blueprints preserve sidecar
  information
- **Dynamic Node** — `kaye/prompt/dynamic_nodes/`, a node type whose content
  has no fixed value and is generated during `.generate_prompt()`; abstract
  base `DynamicNode` (`dynamic_node.py`), heading syntax `(Name)`;
  `DYNAMIC_NODE_TYPES` registers every concrete type: `TodayNode` (today's
  date/time), `AbbrNode` (renders `always_understand`-tagged abbreviations by
  default, or abbreviations found in a `query=` string when one is passed),
  and the tag-filtered `_AbbrTagNodeBase` subclasses — `UsableAbbrNode`
  (`usable_in_brief`), `CodingTermsNode` (`coding`), `PLCNode`
  (`programming_language_code`), `LanguageCodeNode` (`language_code`),
  `UnityEngineAbbrNode` (`unity_engine_abbr`) — each rendering every
  `AbbrData().abbrs` entry matching its `AbbrTags` member via
  `gen_abbrs_content_lines()`. `chat` checkmarks `(Abbreviations)`; `coder`
  checkmarks `(Coding Terms)` via a small `coding_terms_blueprint`
  (`kaye/prompt/blueprint/registrations.py`).
  - **Preface** — every `DynamicNode` accepts a `preface=()` sequence, stored
    as `self._preface` and prepended to `content_lines()`'s generated output.
    `load_prompt_corpus_tree()` populates this automatically: `prompt_corpus.md`
    may contain a literal `# (Today)`-style section (same heading as a dynamic
    node); `_attach_dynamic_node()` (`prompt_corpus_loader.py`) detaches that
    static `PromptCorpusNode` and passes its `content_lines()` as the dynamic
    node's `preface`, so hand-written intro text renders before the generated
    entries instead of being silently dropped.
- **Comment Banner (CB)** — visual separators written inside code comments to
  show structure in long code; part of `Kaye Peer Coder` guidance under `code
  comment` section; defines 6 hierarchy levels (`CB0`–`CB5`): `CB0` (boxed,
  file-level), `CB1` (`#` ruler), `CB2` (`=` ruler), `CB3` (`*` ruler),
  `CB4` (`+` ruler), `CB5` (`-` ruler); must live inside code comments only,
  sparingly used for logical boundaries; headings use Title Case for
  public/exported items, lowercase for internal/private implementation details

### Prompt Corpus Structure

`kaye/prompt_corpus.md` is one large Markdown document parsed into the prompt
tree. Each `#`/`##`/`###` heading becomes a node; `{name}` headings are
sidecar nodes (see above). Blank "spacer" lines between sections are
intentional — preserve them. The top-level (`#`) sections, in order:

- **Introduction** — defines Kaye as an AI agent serving the user
- **Personality** — the Kaye persona: polite, cautious, deferential voice;
  emotion-formatting rules (blockquote `>` reserved for emotional/personality
  asides during task/factual responses, no `----` separators). Followed by an
  unused `{explicit}` sidecar node carrying an intense submissive/master-servant
  variant of the persona — defined for a possible future conditional splice,
  not currently referenced in any `contains_sidecars` call site
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
  `Maintain Docs`, `Initialize Project`, `Maintenance Before Compact`, `Plan
  for Step By Step`, `Resolve Merge Conflict`, `Prepare for Feature Landing`,
  `Prepare for Version Release`, `Gap Review`
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
- **`(Today)` / `(Abbreviations)` / `(Usable Abbreviations)` / `(Coding
  Terms)` / `(Programming Languages Code)` / `(Languages Code)` / `(Unity
  Engine Abbreviations)`** — parenthesized sections whose content is not
  rendered directly; each is carried over as the matching Dynamic Node's
  `preface` (see above) instead

Most leaf sections that back an exportable blueprint carry `{description}` and
`{when_to_use}` sidecar nodes; coder and writer sections add `{globs}` and
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
    - `kaye/cli/prompt/` — `kaye prompt` (alias `p`) subcommand: `ls`
      (list registered blueprint names), `show` (preview a blueprint's
      structure), `generate` (alias `g`, render a concrete prompt);
      `show`/`generate` share a `blueprint_io_parser` base plus
      `load_blueprint_from_args()`/`write_blueprint_result()` helpers
      (`blueprint_io_parser.py`); supersedes the dead, never-wired
      `kaye/cli/cli_prompt/`
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
      - `tests/cli/a/s/` — `claude skill` export tests; no dedicated
        structural-exportability folder — `tests/cli/a/__init__.py`'s
        `ALL_CLAUDE_SKILL_NAMES` derives the full skill list straight from
        `BLUEPRINT_REGISTRIES`, and parametrized suites like
        `tests/corpus/corpus-skill_frontmatter_test.py` cover every
        registration automatically
        - `tests/cli/a/s/coder/` — per-skill content tests for coder blueprints
        - `tests/cli/a/s/others/` — per-skill content tests for miscellaneous
          blueprints (chat, triage-tags, date-time, IPA, etc.)
        - `tests/cli/a/s/proj/` — per-skill content tests for project blueprints
        - `tests/cli/a/s/prompts/` — per-skill content tests for `Projects`
          workflow prompts registered via `_register_prompt`
          (`kaye/prompt/blueprint/registrations.py`, e.g. Create README, Gap
          Review, Plan for Step By Step)
        - `tests/cli/a/s/role/` — per-skill content tests for role blueprints
        - `tests/cli/a/s/style/` — per-skill content tests for style blueprints
        - `tests/cli/a/s/pe/` — per-skill content tests for prompt-engineering
          blueprints
      - `tests/cli/a/sz/` — `claude skill -z` (zipped packages) tests
      - `tests/cli/a/usp/` — `claude user-system-prompt` export tests
        (content, flags, aliases)
      - `tests/cli/a/v/` — `claude vs-code-extension` export tests (CLAUDE.md,
        marketplace, command aliases)
    - `tests/cli/c/` — `continue` subcommand tests
  - `tests/abbr/` — abbreviation collection tests
- `scripts/` — Git hooks and the `systemd` service file


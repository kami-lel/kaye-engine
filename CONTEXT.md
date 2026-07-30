# kaye-engine CONTEXT

System knowledge for the **Kaye** repository — architecture, entities, and
boundaries. Read this alongside `AGENTS.md` before making changes.

## Project Overview

**Kaye** is a prompt-engineering toolkit that maintains a consistent AI agent
identity from a single, structured Source Of Truth. It renders scenario-ready
prompts from a central Markdown corpus using tree-based blueprints, exposed
through a Python API and a CLI.

- language: Python (`>=3.11`)
- package name: `kaye-engine` (distribution name); import name `kaye_engine`
  (`PROGRAM_NAME` in `kaye_engine/__init__.py`, paired with `DISPLAY_NAME` =
  `"Prompt Engineering Project Kaye Engine"` used as the Claude plugin
  `displayName`)
- core dependencies: `anytree`, `json5`, `pyahocorasick`, `pyyaml`
- entry point: `kaye-engine` console script (`[project.scripts]` in
  `pyproject.toml`, mapped to `kaye_engine.__main__:main`); `python -m
  kaye_engine` still works identically. No `http` subcommand — the Flask HTTP
  API moved wholesale to a separate host package

### Key Concepts

- **Prompt Corpus** — a markdown file defining identity, roles, rules,
  styles, and references; the authoritative Source Of Truth for whatever
  content it holds. `kaye_engine` bundles none itself — a caller loads
  and caches one by name via `load_corpus_tree(tree_name, file_path)` /
  `get_corpus_tree(tree_name)` (`kaye_engine/prompt/prompt_corpus_loader.py`)
- **Prompt Tree** — parsed corpus; each section heading is a `BasePromptNode`
- **Blueprint** — a `PromptBlueprint` tree selection spec controlling which
  corpus parts render into a concrete prompt
- **Role** — task-specific behavior profile inside the corpus
- **Sidecar Node** — `{name}`-bracketed subnode attached to a blueprint's
  parent but stored as corpus content; excluded by default and conditionally
  spliced in via `contains_sidecars` (`kaye_engine/prompt/sidecar_nodes/`). There is
  no fixed enum of sidecar names — `get_sidecar_name(node)` (regex
  `^\{.+\}$`, returns `None` if not a sidecar node) extracts the name inside
  the braces as a plain string. Two usage-role labels under the same
  mechanism, not separate classes: *descriptor sidecar* for `{description}`,
  `{when_to_use}`, `{globs}` (reserved names, consumed as blueprint metadata
  by `BlueprintDescriptorSidecars` via plain string-key lookup, exposed as
  `blueprint.sidecars`) and *conditional sidecar* for any other name, e.g.
  `{prerequisite}`, `{for claude code}` (real prompt content spliced in
  conditionally when its name is passed in `contains_sidecars`). Because
  detection is name-based rather than type-based, a reserved descriptor name
  can also be requested via `contains_sidecars` for conditional content
  inclusion — nothing structurally prevents it. To add a new conditional
  sidecar name: add `### {name}` examples to the corpus markdown file
  supplied to `load_corpus_tree()`, document it in `docs/corpus_doc.md`,
  `docs/sidecar_node_doc.md`, and
  `docs/programmatic_api_doc.md`, wire CLI export consumers
  (`kaye_engine/cli/claude/skill/skill_md.py`, `kaye_engine/cli/cli_continue/rule_file.py`,
  both built on the shared `kaye_engine/cli/frontmatter_doc.py`) if the name should
  surface in exports, and mirror tests under `tests/prompt/bp/` and
  `tests/prompt/node/`.
- **Prerequisite Node** — `{prerequisite}` conditional sidecar node; pass
  `contains_sidecars=("prerequisite",)` (or a larger collection) to
  `generate_prompt()` / `render.render_prompt_lines()` to auto-checkmark
  every matching sidecar node whose parent is already checkmarked before
  rendering; `"for claude code"` and `"prerequisite"` are combined in
  `kaye_engine.cli.claude.CONTAINING_SIDECARS` for all Claude exports
- **Blueprint Sidecar Merging** — `BlueprintDescriptorSidecars.__or__` merges
  two instances via `left | right`; left operand takes priority for each
  field (description, when_to_use, globs, prerequisite); `PromptBlueprint.__or__`
  now includes sidecar merging so merged blueprints preserve sidecar
  information
- **Dynamic Node** — `kaye_engine/prompt/dynamic_nodes/`, a node type whose content
  has no fixed value and is generated during `.generate_prompt()`; abstract
  base `DynamicNode` (`dynamic_node.py`), heading syntax `(Name)`;
  `DYNAMIC_NODE_TYPES` registers every concrete type: `TodayNode` (today's
  date/time), `AbbrNode` (renders `always_understand`-tagged abbreviations by
  default, or abbreviations found in a `query=` string when one is passed),
  and the tag-filtered `_AbbrTagNodeBase` subclasses — `UsableAbbrNode`
  (`usable_in_brief`), `CodingTermsNode` (`coding`), `PLCNode`
  (`programming_language_code`), `LanguageCodeNode` (`language_code`),
  `UnityEngineAbbrNode` (`unity_engine_abbr`) — each rendering every
  `get_abbr_data().abbrs` entry matching its `AbbrTags` member via
  `gen_abbrs_content_lines()`. `chat` checkmarks `(Abbreviations)`; `coder`
  checkmarks `(Coding Terms)` via a small `coding_terms_blueprint`
  (`kaye_engine/prompt/blueprint/registrations.py`).
  - **Preface** — every `DynamicNode` accepts a `preface=()` sequence, stored
    as `self._preface` and prepended to `content_lines()`'s generated output.
    `load_corpus_tree()` populates this automatically: the corpus file
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

A prompt corpus file is one large Markdown document parsed into the prompt
tree by `load_corpus_tree()`. Each `#`/`##`/`###` heading becomes a node;
`{name}` headings are sidecar nodes (see above). Blank "spacer" lines between
sections are intentional — preserve them. `kaye-engine` bundles no corpus of
its own and has no knowledge of what top-level sections a real one contains;
that structure is documented by whichever host package supplies the real
file.

## Repository Layout

- `kaye_engine/` — main package (CLI, prompt engine, abbreviation collection)
  - `kaye_engine/prompt/` — prompt tree, nodes, blueprints, loaders
  - `kaye_engine/cli/` — argparse-based CLI subcommands
    - `kaye_engine/cli/cli_continue/` — exports blueprint/abbreviation rules to
      `~/.continue`
    - `kaye_engine/cli/claude/` — exports blueprints as Claude plugins, marketplaces,
      agentskills.io Skills, VS Code Extension setup, and the user system
      prompt `CLAUDE.md`
    - `kaye_engine/cli/prompt/` — `kaye-engine prompt` (alias `p`) subcommand: `ls`
      (list registered blueprint names), `show` (preview a blueprint's
      structure), `generate` (alias `g`, render a concrete prompt);
      `show`/`generate` share a `blueprint_io_parser` base plus
      `load_blueprint_from_args()`/`write_blueprint_result()` helpers
      (`blueprint_io_parser.py`)
- `dify_studio/` — Dify workflow node sources (not part of the package)
- `docs/` — in-depth documentation (programmatic API, corpus format, sidecar
  and dynamic nodes, abbreviations, Claude and Dify integration)
- `tests/` — `pytest` suite, mirrors the package structure. It runs
  **serially by design**: most cases are cheap in-process assertions against
  an already-parsed corpus, so worker startup costs more than the split saves
  — a measured `-n auto` run finished no faster than the serial one — and the
  session-scoped export fixtures (`tests/conftest.py`,
  `tests/cli/conftest.py`, which shell out to `kaye-engine claude skill` and friends)
  are rebuilt per worker and carry run-order assumptions that a split breaks.
  `pytest-xdist` is deliberately absent from the `dev` extra
  - `tests/prompt/` — unit tests for the prompt engine (nodes, blueprints)
    - `tests/prompt/bp/` — `PromptBlueprint` tests
    - `tests/prompt/node/` — `PromptCorpusNode` / `BasePromptNode` tests
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
        - `tests/cli/a/s/prompts/` — per-skill content tests for workflow
          prompts registered via `_register_prompt`
          (`kaye_engine/prompt/blueprint/registrations.py`, e.g. Create README, Gap
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
  - `tests/api/`, `tests/dify/` — **stale.** Tested the Flask HTTP API and
    Dify app endpoints that lived at `kaye_engine/api/` before that package
    moved wholesale to a separate host package; left in place unmoved and
    now fail to collect (`kaye_engine.api` no longer exists). Not part of
    the `pytest` scope for any current source path — do not re-add an
    `api` package here to satisfy them, move or retire them instead

## Personalization Boundary

`kaye-engine` is a public mechanism package, meant to be extended by a
separate, private repository holding the user's personalized project —
one that supplies the actual identity content, abbreviations, and
blueprint registrations `kaye-engine`'s mechanism operates on. The
dependency runs one direction only: a personalized project depends on
`kaye-engine`; `kaye-engine` must build, test, and export with no
knowledge of what specific identity content, abbreviations, or
blueprints such a project supplies.


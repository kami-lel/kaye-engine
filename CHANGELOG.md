# Kaye CHANGELOG

[^format]

<!-- todo improve AM usage: abbreviations, vocab for up/down, vocab for different levels, and usage in Kaye Peer Coder -->













## [Unreleased]

### Added

- **`kaye/cli/claude/vs_code/`** — new VS Code Extension export subcommand
  (`claude vs-code-extension`, alias `a v`): writes User System Prompt to
  `~/.claude/CLAUDE.md` and exports marketplace to
  `~/.claude/kaye_marketplace/`; combines user-prompt and marketplace exports
  for streamlined Claude Code setup
- **`tests/cli/a/v/`** — new test suite for `kaye claude vs-code-extension`:
  `cli-a-v-alts_test.py` covers command aliases (`v`, `vs-code-extension`);
  `cli-a-v-claude_md_test.py` verifies CLAUDE.md creation and content
  equivalence to `kaye claude u -c`; `cli-a-v-command_test.py` tests command
  success path; `cli-a-v-marketplace_test.py` tests marketplace export; shared
  fixtures in `conftest.py`
- **`tests/__init__.py`** — new centralized test constants module: 
  `TESTEE_INTRODUCTION_CONTENT`, `TESTEE_MARKDOWN_FORMAT_CONTENT`, 
  `TESTEE_CHAT_ADDITIONAL_CONTENT`, `TESTEE_CHAT_COMMENTARY_CASE_CONTENT`, 
  `TESTEE_CODER_CONTENT`, `TESTEE_TITLE_CASE_CONTENT`, `TESTEE_BRIEFNESS_CONTENT`; 
  eliminates duplicate string lists across test files; semantic, reusable content 
  markers organized by feature area
- **`tests/cli/a/c/cli-a-c-claude_md_test.py`** — extended with parametrized 
  content tests: `TestIntroductionContent`, `TestMarkdownFormatContent`, 
  `TestChatAdditionalContent`, `TestChatCommentaryCaseContent`, `TestCoderContent`; 
  verifies `kaye claude code` CLAUDE.md has content equivalent to 
  `kaye claude u -c` (chat blueprint + coder mode)
- **`tests/api/ky/task/` content constants** — re-exported from `tests/__init__.py` 
  for use in API task tests
- **Project CONTEXT Writer** — new corpus section for creating and maintaining
  `CONTEXT.md` and `CONTEXT.local.md` files; covers document title, suggested
  sections, living document maintenance, and quality expectations
- **`tests/cli/a/p/`** — new test suite for `kaye claude plugin`: skill file
  existence across all 78 exported skills, `plugin.json` content validation
  (`name`, `displayName`, `version`, `description`, `author`), and mock-based
  command and alias tests (`claude plugin`, `claude p`, `a plugin`, `a p`)
- **`tests/cli/a/cz/`** — new test suite for `kaye claude plugin -z`: mirrors
  `tests/cli/a/p/` with zip extraction via `zipfile.ZipFile.extractall()`
  before path assertions; extended with `cli-a-cz-claude_md_test.py` to verify
  CLAUDE.md presence in the extracted output
- **`tests/cli/a/m/`** — new test suite for `kaye claude marketplace`: file
  existence for all skill files, `plugin.json`, and `marketplace.json`;
  `marketplace.json` content validation (`$schema`, `name`, `version`,
  `description`, `owner.name`, `plugins` list, `plugins[0].source`);
  mock-based command and alias tests (`claude marketplace`, `claude m`, `a m`,
  `a marketplace`)
- **`tests/cli/a/sz/alts/`** — new mock-based alias tests for
  `kaye claude skill -z` (`claude s -z`, `a skill -z`, `a s -z`)
- **New project prompt corpus sections** — 7 new `## ` prompt sections added
  under `# Projects`: `Create README`, `Maintain README`, `Create CHANGELOG`,
  `Maintain AGENTS and CONTEXT`, `Create Docs`, `Initialize Project`,
  `Compact with Maintenance`; all follow the shared `#### Instructions` /
  `#### Output` / `{prerequisite}` structure
- **`kaye/cli/prompts_blueprints.py`** — expanded from 2 to 12 blueprints:
  `create_readme`, `maintain_readme`, `create_changelog`, `maintain_changelog`,
  `create_agents_and_context`, `maintain_agents_and_context`, `create_docs`,
  `maintain_docs`, `initialize_project`, `compact_with_maintenance`,
  `prepare_for_feature_finish`, `prepare_for_version_release`; `PROMPTS_BLUEPRINTS`
  list updated accordingly; uses `recursively=True` only for nodes with
  non-meta child sections
- **`tests/corpus/corpus-skill_frontmatter_test.py`** — refactored to a single
  `@pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)` test in
  `TestSkillFrontmatter.test_frontmatter_conforms_to_spec`; covers every
  exported blueprint, prompt, and abbreviation skill automatically — no
  per-skill hand-written function needed for new additions
- **`tests/cli/a/c/`** — new test suite for `kaye claude code` (`a code`,
  `a c`, `claude c`): CLAUDE.md existence at `~/.claude/CLAUDE.md`,
  `plugin.json` content validation, skill files existence across all exported
  skills, and mock-based command/alias tests
- **`tests/cli/a/u/`** — new package replacing `cli-a-u-chat_test.py`:
  `cli-a-u-alts_test.py` covers all command aliases and flags,
  `cli-a-u-content_test.py` covers output content per flag combination
  (`--rapid`, `--coder`), and `conftest.py` provides shared fixtures

### Changed

- **README** — restructured Claude integration section: added dedicated `####
  Claude Code VS Code Extension` subsection with step-by-step marketplace setup
  instructions; clarified install targets (`Claude Desktop` vs `Claude Code VS
  Code Extension`) and command output paths
- **API task content tests** — refactored `tests/api/ky/task/api-ky-task-chat1_test.py` 
  and `api-ky-task-rapid1_test.py` from 51 and 14 individual `test_*` methods 
  respectively to parametrized test classes using `@pytest.mark.parametrize` over 
  shared content constants; reduced duplication and improved maintainability
- **Continue blueprint coder test** — `tests/cli/c/c/coder/cli-c-c-bp-coder_test.py` 
  refactored to use `TESTEE_CODER_CONTENT` from `tests/__init__.py` instead of 
  `TESTEE_FILE_CONTENT_ALL`; content tests converted from 10 individual 
  `test0`...`test9` methods to a single parametrized `test_content` method
- **`kaye claude user-system-prompt`** (`claude u`, `a u`) — new `-r`/`--rapid`
  flag uses the Rapid blueprint instead of Chat; new `-c`/`--coder` flag appends
  Kaye Peer Coder content after the main blueprint
- **`chat_blueprint` and `rapid_blueprint`** in `embedded_blueprints.py` —
  `Role` and `(Abbreviations)` removed from their embedded definitions; the
  Dify chat task now merges them in via a local `_user_scope_blueprint`
  (`Role` + `(Abbreviations)`), keeping the base blueprints leaner and the
  user-scope composition explicit
- **Prompt corpus — skill metadata** — added `{description}` and `{when_to_use}`
  meta nodes to `Create Docs`, `Prompt Writer`, and `Skill Description Writer`
  sections; all three now export accurate skill metadata
- **Continue Behavior** — rehomed from a standalone top-level `# Continue
  Behavior` section to a `## ` subsection under `# Agent Behavior`; corpus
  path updated in `export_blueprint_rules.py`; `run_terminal_command`
  subsection normalized from `### ` to `#### `; Continue config test
  expectations updated to reflect new heading levels
- **Prompt corpus — project prompts** — removed the `## project prompts`
  container; `Maintain Docs`, `Maintain CHANGELOG`, `Create README`, `Create
  AGENTS`, `Prepare for Feature Finish`, and `Prepare for Release` promoted
  from `### ` to `## ` level as direct children of `# Projects`; internal
  subsections normalized from `#####`/`######` to `#### `; `{description}`
  and `{prerequisite}` meta nodes normalized from `#### ` to `### `;
  `prompts_blueprints.py` path updated to remove `["project prompts"]` lookup,
  orphaned `checkmark()` calls on the removed `edit CHANGELOG` node removed;
  Continue prompt tests updated for new heading levels
- `kaye claude` subcommands (`code`, `marketplace`, `plugin`, `skill`,
  `user-system-prompt`) — `--help` now prints a detailed description with an
  output-folder tree diagram, rendered verbatim via
  `RawDescriptionHelpFormatter`
- **Project AGENTS Writer** — expanded and clarified guidance: new sections
  covering Continue Rule compatibility, frontmatter format, suggested sections,
  what to include/exclude, testing instructions, and quality expectations;
  updated glob pattern to include `.local` and `.override` file variants;
  unit tests enhanced with comprehensive content assertions for description
  and when_to_use metadata; Continue config tests updated to match reformatted
  export output
- **Project Structure** — unit tests updated to reflect new file and folder
  entries: `CREDITS.md`, `DEVLOG.md`, `AGENTS.local.md`, `CONTEXT.md`,
  `CONTEXT.local.md`, `bin/`, `examples/`, and `tools/`
- **Agent Behavior** — content expanded with new Git Command Safety Policy
  guidance; unit tests added for all 5 content entries across Claude skill
  and Continue config exports
- **`tests/cli/a/s/` and `tests/cli/a/sz/`** — all `TestContent` and
  `TestPrerequisite` classes refactored: manually-numbered `test0`, `test1`,
  ... methods replaced with a single `@pytest.mark.parametrize` method;
  `tests/cli/a/s/alts/` and `tests/cli/a/sz/alts/` refactored to mock-based
  tests (no file I/O) using shared fixtures from `tests/cli/a/conftest.py`
  (`mock_run`, `mock_tmp_path`, `mock_tmp_path_factory`)
- **`blueprint_meta_nodes.py`** — removed `collapse_lines_into_single_line()`
  helper function; replaced with module-level `REPLACEMENT_NEWLINE_SYMBOL`
  constant (`"↵"`) used inline with `.join()`
- **Renamed prompt sections** — `Create AGENTS` → `Create AGENTS and CONTEXT`;
  `Prepare for Release` → `Prepare for Version Release`; slug keys updated in
  `prompts_blueprints.py`, `tests/cli/__init__.py` (`PROMPT_FILENAME2NAME`,
  `TESTEE_FILE_CONTENT_ALL`, `TESTEE_DESCRIPTION_CONTENT_ALL`,
  `TESTEE_PREREQUISITE_CONTENT_ALL`), and all affected test files
- **Project README Writer** — rewritten from persona style to guideline style:
  intro changed from "You are an expert..." to "These guidelines define what a
  good `README.md` is"; removed `#### Purpose` and `#### Document Title`
  subsections; renamed `#### Quality Expectations` → `#### Quality`; backtick-
  wrapped filenames simplified to plain references in `description` and
  `when_to_use` metadata
- **Project CHANGELOG Writer** — `**Types of Changes:**` inline bold changed
  to `#### Types of Changes` subheading; corrected `Github` → `GitHub`;
  removed the `"- title must be \`Project Name CHANGELOG\`"` rule;
  backtick-wrapped `CHANGELOG.md` simplified to `CHANGELOG` in metadata
- **Project AGENTS Writer** — intro updated from "`AGENTS.md` files" to
  "`AGENTS.md` (or AGENTS-style file) files" to clarify applicable file types
- **`tests/cli/c/p/`** — all 6 Continue prompt test files refactored:
  `TestContent` now uses `TESTEE_FILE_CONTENT_ALL[PROMPT_FILENAME]` with a
  single `@pytest.mark.parametrize` method; `TESTEE_FILE_CONTENT` module
  constant added to each file; stale `assert_edit_changelog*`,
  `assert_edit_readme*`, `assert_edit_agents*` helpers removed from
  `tests/cli/c/p/__init__.py`; `PROMPT_FILENAME2NAME["prepare-for-feature"]`
  renamed to `"prepare-for-feature-finish"`
- **`tests/cli/__init__.py`** — `TESTEE_FILE_CONTENT_ALL` entries for 6 prompt
  blueprints expanded with full section content strings (headings, instructions,
  output); description and when_to_use metadata strings updated to use plain
  file references instead of backtick-wrapped filenames
- **Style Guide capitalization split** — `Style Guide Capitalization` section
  split into two standalone sections: `Style Guide Title Case` (headlines and
  document titles) and `Style Guide Commentary Case` (list items and table
  cells); each has independent `{description}` and `{when_to_use}` meta nodes;
  `style_capitalization_blueprint` replaced with `style_title_case_blueprint`
  and `style_commentary_case_blueprint` in `embedded_blueprints.py` and
  `EXPORTABLE_BLUEPRINTS`; `chat_blueprint` updated to include Commentary Case
  (added to Style Guide traversal); skill and continue rule exports split:
  new `style-guide-title-case` and `style-guide-commentary-case` skills replace
  single `style-guide-capitalization` skill; test files reorganized in
  `tests/cli/a/s/`, `tests/cli/a/sz/`, and `tests/cli/c/c/style/`;
  `tests/cli/a/u/__init__.py` updated with `COMMENTARY_CASE` marker
  (`## Style Guide Commentary Case`)
- **pytest-xdist reverted to manual opt-in** — removed `addopts = -n auto`
  from `setup.cfg`; pytest now runs serially by default; `-n auto` available
  manually; documented in AGENTS.md; session-scoped fixture re-execution across
  xdist workers made parallel runs 2× slower (212s vs 109s) due to expensive
  CLI exports; root cause fixed by `generate_lineage()` memoization (see Fixed)
- **CLI prompt export tests aligned** — `tests/cli/a/u/` tests now expect
  `Role` and `(Abbreviations)` nodes absent from CLI user-system-prompt output
  (only injected by Dify API); `USER_SCOPE` constant added to `__init__.py`

### Deprecated

### Removed

- **`collapse_lines_into_single_line()`** in `blueprint_meta_nodes.py` —
  removed in favor of `REPLACEMENT_NEWLINE_SYMBOL.join(...)` at call sites

### Fixed

- **`BasePromptNode` lineage/hash memoization** — `generate_lineage()` now
  caches its result as a tuple in `_lineage_cache` on first call and returns
  a copy on subsequent calls; `__hash__` caches its result in `_hash_cache`;
  both caches are stored via `self.__dict__` to avoid `__slots__` conflicts;
  reduced 33M redundant `generate_lineage()` calls per full skill export to
  O(1) per node after warm-up; single export: ~10s → ~4.3s; full test suite:
  ~109s → ~49s (2.2× faster); output byte-identical (verified via `diff -r`)

### Security

[unreleased]: https://github.com/kami-lel/kaye/compare/v6.6.0...dev












## [6.6.0] - 2026-06-18

### Added

- `kaye claude` command suite (aliases `anthropic`, `a`) — exports blueprints
  for Anthropic Claude:

  - `plugin` (`p`) — plugin folder; `-z` builds compressed `.plugin`, `-n`
    drops version from filename
  - `skill` (`s`) — agentskills.io Skill folders; `-z` builds `.zip` packages
  - `marketplace` (`m`) — marketplace folder; `marketplace.json` at root,
    plugin under `plugins/`

- `kamilog` logging module re-introduced (`v1.4.1`); adds `SUCC` and `DONE`
  levels
- `MetaNodeType` checkers — `is_meta_node`, `is_description`, `is_when_to_use`,
  `is_globs`, `is_prerequisite`
- `ManifestPluginJson` and `MarketplaceJson` helpers — build plugin and
  marketplace JSON manifests
- `DISPLAY_NAME` constant `"Prompt Engineering Project Kaye"` — plugin
  `displayName`, separate from `PROGRAM_NAME`

### Changed

- Claude CLI split into `claude_plugin/` and `claude_skill/` subpackages
- `AGENTS.md` expanded — meta nodes, corpus structure, layout, build/test,
  conventions

Package metadata:

- `PROGRAM_NAME` lowercased to `kaye`; `DIST_NAME` removed — single
  distribution name for all `importlib.metadata` lookups
- `setup.cfg` gains author email, homepage, repository; plugin and skill
  version derive from this source

Logging:

- Claude CLI export routes through `kamilog`, not `print()`; `-v`/`-q` set
  verbosity
- output drops timestamps and bracket framing (e.g. `DONE`, not `[DONE ]`)
- `PASS` renumbered `25` → `21`; default level now `DONE`; `-q`/`-qq`/`-qqq`
  map to `WARNING`/`ERROR`/`CRITICAL`

Exports:

- skill `SKILL.md` glob patterns moved to native `paths` frontmatter for
  path-scoped activation
- corpus blueprints carry `{prerequisite}` meta nodes, auto-checkmarked with
  their parent
- marketplace plugin placed under `plugins/<name>/`

### Removed

- `BasePromptNode.is_prerequisite_node` — use `MetaNodeType.is_prerequisite()`
- `kaye skill` top-level subcommand — superseded by `kaye claude skill`
- `kaye claude update` and `kaye claude create` stubs — superseded by
  `kaye claude plugin -z`
- `kaye/cli/cli_skill/` package — relocated to `kaye/cli/cli_claude/`

### Fixed

- `plugin.json` fields (`displayName`, `author.email`, `homepage`,
  `repository`) now populated; were blank from stale dist-info and wrong
  metadata key casing
- corpus Coder Python — prohibit type hints, require `str.format()` over
  f-strings
- corpus Coder Python Docstring — module docstring first line is filename plus
  description
- corpus Prepare for Release — drop empty subsections when promoting
  *Unreleased*
- `continue` CLI — corrected verbosity init order

[6.6.0]: https://github.com/kami-lel/kaye/compare/v6.5.1...v6.6.0












## [6.5.1] - 2026-06-14

### Changed

**Prompt Corpus**:

- coder blueprint metadata expanded:

  - All coder blueprints (Bash, C, C++, C#, Unity Engine, GDScript, HTML,
    JavaScript/TypeScript, Python, Python Docstring Style, Python Testing
    Guidelines) now carry richer `{description}` text and a dedicated
    `{when_to_use}` sub-node with trigger examples

  - Unreal Engine description unchanged; no `{when_to_use}` node added

- style and project blueprint metadata refined:

  - Good Writing, Briefness Style, Capitalization: descriptions tightened and
  `{when_to_use}` guidance added with trigger phrases

  - Skill Metadata: enforce non-repeating, concise fields; usage guidance added

  - Project blueprints (Agents, Changelog, Project, Readme, Semantic Versioning):
standardized description headers and expanded usage triggers

- **Skill version metadata**: version field now always included in exported
  `SKILL.md` files; `includes_version` parameter removed from export functions
  (version stamping is no longer optional)

- **Unit tests**:

  - `s/u` and `c/c` header tests updated across all coder, proj, style, and
    others test files to assert corpus-derived `description` and `when_to_use`
    YAML values
  - `test_version()` added to all 27 skill header tests in `s/u` directory
  - VERSION_LINE_PATTERN now matches any version string (lowercase letters,
    digits, `.`, `-`) instead of hardcoded version

### Fixed

- **`skill print`**: version is now printed correctly for skills that have no
  version field across all print modes

### Security

[6.5.1]: https://github.com/kami-lel/kaye/compare/v6.5.0...v6.5.1












## [6.5.0] - 2026-06-14

### Added

- `MetadataMDFile` (`metadata_md_file.py`): a more generic version of `RuleFile`

- **`skill` CLI subcommand** with two subcommands (aliases: `s`):

  - `skill update FOLDER` (aliases: `skill u`, `s update`, `s u`) — exports all
    blueprints, prompts, and abbreviation groups as skill folders containing
    `SKILL.md` files into FOLDER
  - `skill create FOLDER` (aliases: `skill c`, `skill z`, `s c`, `s z`) —
    creates `.zip` archives of all skill folders and places them in FOLDER

- `SKILL.md` frontmatter: `user-invocable` field — abbreviation skills are
  exported with `user-invocable: false` to suppress them from slash-command
  listings

- `export_skills_as_folders`: optional `includes_version` parameter to embed
  the package version in abbreviation skill frontmatter metadata

### Changed

- split Style Guide blueprints

- **Prompt Corpus**: refactored "Coder Python Docstring Style" meta nodes
  (`{description}`, `{when_to_use}`, `{globs}`) to proper heading level 4
  nesting so they are correctly parsed as child nodes of the section

- CLI test helpers renamed for generality:

  - `split_rule_file_basic_format` → `split_frontmatter_md_file`
  - `assert_rule_file_basic_format` → `assert_frontmatter_md_file_basic_structure`
  - backward-compatibility aliases retained in `tests.cli.c.c`

- CLI test constants: removed redundant `MD_FILENAMES` and `PROMPT_FILENAMES`
  lists; callers now use `MD_FILENAME2SKILL_NAME.keys()` and
  `PROMPT_FILENAME2NAME.keys()` directly


### Fixed

- **RuleFile**: fixed blueprint rule export to use `blueprint.meta.description`
  instead of `blueprint.meta.description_and_when_to_use` — ensures only the
  description is written to the frontmatter, not both description and when_to_use

### Security

[6.5.0]: https://github.com/kami-lel/kaye/compare/v6.4.0...v6.5.0













## [6.4.0] - 2026-06-10

### Added

- `abbrs.json`: add `"single_character"` tag to all single-character abbreviations

### Changed

- `prompt_corpus.md`

  - rename Coder docs roles to Project docs for clarity
  - Continue Behavior: avoid unnecessary closing statement

- **Dify App**: update blueprint imports in `kaye_chat_task.py` for `project_changelog_blueprint`
- **Annotation Markers**: refactor comment section heading examples for improved clarity

Programmatic API:

- rewrite `abbr_rule.py` logic to allow duplicate abbreviations occurring in different files
- refactor `abbr_rule.py` with data-driven naming dictionaries (`_TAG_NAMES`, `_WRAP_NAMES`) for
- add `AbbrTags.single_character` and `AbbrTags.emoji` to tag-based rule file exports

embedded blueprints

- rename blueprint variables for better semantic alignment with corpus node structure
- add `project_semantic_versioning_blueprint` to `embedded_blueprints.py` for Semantic Versioning documentation

Continue Export: 

- update blueprint rule exports to reflect renamed project documentation blueprints
  standardized file naming following `{rule_name}.md` pattern
- optimize `_export_by_first_char()` for single-pass bucket grouping with frozensets for O(1) lookups
  instead of 28 separate list iterations
- standardize abbreviation rule file naming convention: `abbr-*.md` → `Abbr *.md` (filename matches rule name)

[6.4.0]: https://github.com/kami-lel/kaye/compare/v6.3.0...v6.4.0














## [6.3.0] - 2026-06-09

### Added

- `BasePromptNode`: new properties

  - `.is_technical_node` — check if node name matches pattern `{name}`, identifying
    technical and special nodes (e.g., dynamic nodes)
  - `.description_subnode` — retrieve child node with heading `{description}` if
    present, supporting nodes that contain description subnodes in `prompt_corpus.md`
  - `.is_description_node` — check if node name is exactly `{description}`,
    identifying whether the node itself is a description node

- `PromptBlueprint`: new classmethod and parameter

  - `.create_from_node()` — create a blueprint from a specific node, automatically
    extracting description subnode content as blueprint description for LLM task
    relevance assessment
  - `.generate_prompt()` — new `disable_first_heading` parameter to suppress
    rendering the top-level heading when embedding prompts in larger contexts

- **Continue Export**: documentation workflow blueprints and Continue export refactor

  - `prepare_for_feature_finish` — prepare feature branch for final submission;
    generates prompts to update `CHANGELOG.md` and documentation files
  - `prepare_for_release` — prepare release branch with comprehensive documentation
    updates
  - `create_readme` — create a new `README.md` tailored to the repository
  - `create_agents` — create a new `AGENTS.md` tailored to the repository
  - `maintain_docs` — maintain and update existing `README.md` and `AGENTS.md` files
  - `maintain_changelog` — update `CHANGELOG.md` with structured entries
  - move Continue export under the CLI package and keep it out of the programmatic API

- `abbrs.json`: add two abbrs of `~` and `~~`
- embedded blueprints for documentation writing:

  - `coder_readme_blueprint` (`Coder README Writer`) — format and style guidance for
    `README.md`
  - `coder_agents_blueprint` (`Coder AGENTS Writer`) — format and style guidance for
    `AGENTS.md`

- prompt_corpus.md: **README/AGENTS Writer** role with comprehensive guidance:

  - **create README/AGENTS** — structured instructions for authoring new
    documentation files
  - **maintain README/AGENTS** — guidelines for updating existing documentation
  - **Changelog Writer** — format, versioning, and entry style standards

- prompt_corpus.md: **Maintain Changelog** — explicit guidance for CHANGELOG
  updates including:

  - feature branch change identification
  - existing entry preservation and deduplication
  - recursive blueprint handling
  - changelog structure standards

- unit tests for `continue prompt` subcommand with documentation maintenance
  scenarios

### Changed

- **Continue Export module**: refactor Continue export for CLI-only use with
  relative imports

  - moved `continue_export` package under `kaye.cli` as internal CLI subcommand
    support
  - export logic now lives behind CLI commands instead of the Python API
  - relative imports adopted for improved modularity and clearer package
    boundaries
  - standardize blueprint exported rule file names

- prompt_corpus.md: better organization of prompts related to documentation
  workflows, clearly split into:

  - **README/AGENTS Writer** (style & format guidelines)
  - **Create README/AGENTS** (create new files)
  - **Maintain README/AGENTS** (update existing files)
  - **Maintain Changelog** (CHANGELOG.md updates)

- prompt_corpus.md: **Maintain Docs** prompt expanded with:

  - recursive blueprint handling for comprehensive documentation updates
  - explicit README/AGENTS edit guidance
  - content assertion rules

- Continue Export: blueprints refactored for clarity:

  - renamed `prepare_feature` to `prepare_for_release`
  - refactored rule text for consistency
  - improved changelog export with feature-specific guidance

- prompt_corpus.md: code block formatting standardized with proper indentation

### Fixed

- `PromptBlueprint.generate_prompt()`: trim leading and trailing empty lines
  before joining rendered lines
- prompt_corpus.md: **Kaye Peer Coder**: comment section headings — corrected
  wrong example of top-level heading

[6.3.0]: https://github.com/kami-lel/kaye/compare/v6.2.1...v6.3.0











## [6.2.1] - 2026-06-06

### Fixed

- `prompt_corpus.md`: Continue Prompts: Maintain Docs: fix rule name

[6.2.1]: https://github.com/kami-lel/kaye/compare/v6.2.0...v6.2.1











## [6.2.0] - 2026-06-06

### Added

- Python CLI: subcommand `continue prompt` to support exporting **Continue Prompts**

  - comprehensive unit tests for this

`prompt_corpus.md`: 

- **Continue Prompts**:

  - Maintain Changelog
  - Maintain Docs
  - Resolve Annotation Markers
  - Prepare for Release

- Coder: AGENTS.md Writer: instruction for **writing proper** `AGENTS.md`
- `AGENTS.md` for this project

### Changed

- Python CLI: subcommand `continue` moved to `continue config`

`prompt_corpus.md`

- Coder: Python: *TestingGuidelines*: more comprehensive instruction 
- Coder: Project Structure: include `AGENTS.md`
- rename section **Style Guide** (from Style)

[6.2.0]: https://github.com/kami-lel/kaye/compare/v6.1.0...v6.2.0













## [6.1.0] - 2026-06-18

### Added

`abbrs.json`:

- add `HK$`, `JP¥`, `JP`

Programmatic API: 

- `continue_export`: 

  - split into `continue_export` package from `continue_support.py`
  - `abbr_rule.py`: export rule files split by tag, wrap type (symbol, suffix, prefix), digits, letters, and other

- `abbr_collection`: 

  - split from `abbr_collection.py`
  - `AbbrEntry`: add `as_md_list_entry()`, abbreviation list item format normalized

    - update usages & unit tests to utilize this

### Changed

- `kaye continue` CLI now delegates entirely to `continue_export`

`prompt_corpus.md`:

- update instruction on *Continue Behavior*
- more comprehensive instruction on Python *Docstring Style*

[6.1.0]: https://github.com/kami-lel/kaye/compare/v6.0.0...v6.1.0













## [6.0.0] - 2026-06-05

### Added

- **Continue support**: generate **Continue** rule files for `~/.continue` via the `continue_support` package and the `kaye continue` CLI command
- **Changelog Writer** role
- new `Continue Behavior` section in `prompt_corpus.md`

Dify App *Opus Tag Smith*:

- **`Shelver` mode** for books, replacing Kaye Chat's *shelver* role
- subtitle extraction, and Flask HTTP API documentation

### Changed

- **embedded blueprints are now Python modules** (in `embedded_blueprints.py`), with shared `rapid`/`chat`/coder factories and per-blueprint `display_name`/`description`
- **CLI restructured around subcommands**: the HTTP API moved to `python -m kaye http` (alias `h`)
- in `prompt_corpus.md`, lift *Kaye Peer Coder* up one level

Dify App *Opus Tag Smith*:

- split title, subtitle, and translated-title extraction

Dify App *Kaye Chat*:

- tune difficulty-to-model thresholds

### Deprecated

- `kaye.gen_prompt` blueprint loading: replaced by direct imports from `kaye.prompt.embedded_blueprints`

### Removed

- **old embedded blueprint files** (`./kaye/gen_prompt/embedded_blueprints/` and its `.kaye_blueprint` files) and `create_blueprint` wrappers
- the `prompt` CLI subcommand (disabled, pending rework)
- Kaye Chat's *shelver* role

[6.0.0]: https://github.com/kami-lel/kaye/compare/v5.5.0...v6.0.0













## [5.5.0] - 2026-05-04

### Added

- *Opus Tag Smith* Dify App

[5.5.0]: https://github.com/kami-lel/kaye/compare/v5.4.1...v5.5.50















## [5.4.1] - 2026-04-14

### Changed

Kaye Chat *Dify App*:

- always use the higher value of `current_difficulty` and `decayed_difficulty`
  to ensure prefer more intelligent LLM(s) for each round

- update *meta content* format

[5.4.1]: https://github.com/kami-lel/kaye/compare/v5.4.0...v5.4.1















## [5.4.0] - 2026-04-10

### Added

Kaye Chat *Dify App*:

- **decaying difficulty**: a sequence of difficulty is saved to create a *Exponential Moving Average* `decayed_difficulty`

- *Kaye Peer Coder* role: MonoBehaviour:
  prompt for Inspector Field Null Guard

- *Shelver* role

### Changed

- refactorize unit tests, defining and using helper functions

Kaye Chat *Dify App*:

- connect *Fail Branch* of LLMs for **fail gracefully** design
- pre-process user query for sense node (and sense node only) by truncating and keep constant amount of lines

[5.4.0]: https://github.com/kami-lel/kaye/compare/v5.3.0...v5.4.0













## [5.3.0] - 2026-04-08

### Added

`abbrs.json` & related:

- new wrap: `currency` and `unit`
- new tags: `unit_of_measure` and `currency_symbol`
- new abbrs: *b* (bit,) *B* (byte,) *d* (dimension,) & *phy* (physics)

Kaye Chat *Dify App* roles:

- Changelog Writer
- Prompt Writer
- Librarian

### Changed

`abbrs.json` & related:

- `mpl` (implement, from `mpmt`)
- update abbrs entries with new wraps & tags
- unit tests for aforementioned above
- documentation for aforementioned above

Kaye Chat *Dify App*:

- update difficulty and LLMs conversion with one more case

  - related unit test

- for *coder* role, improve sensing PLs' prompt
- turn `show_meta_content` to off by default
- refactoring `kaye_chat.py` (Flask API)
- refactoring unit tests

### Removed

Kaye Chat *Dify App* **Kaye Peer Coder**:

- support for QML and Qt

### Fixed

Kaye Chat *Dify App*:

- *coder* role should never skip sense

[5.3.0]: https://github.com/kami-lel/kaye/compare/v5.2.2...v5.3.0














## [5.2.2] - 2026-04-06

### Added

- instruction on formatting **LaTeX**
- instruction on formatting **mermaid** graph

Kaye Chat *Dify App*, Kaye Peer Coder:

- code format instruction, especially on file name
- instruction on brace style

### Changed

Kaye Chat *Dify App*:

- enable **vision** for all LLMs
- use more readable role tags with Emoji in *meta content*

Kaye Commit Sense *Dify App*:

- re-implement as a **Chatflow** such that it can utilize:
  *OpenAI Compatible Dify App* Plugin

[5.2.2]: https://github.com/kami-lel/kaye/compare/v5.2.1...v5.2.2













## [5.2.1] - 2026-04-06

### Fixed

- handle case where unknown PLC is given

[5.2.1]: https://github.com/kami-lel/kaye/compare/v5.2.0...v5.2.2















## [5.2.0] - 2026-04-06

### Added

Kaye Chat *Dify App* Roles:

- Art Tutor
- Deutschlehrer
- Tarot Reader

### Changed

- make *Prompt Writer* part of the utility prompts
- move `abbrs.json` level up, to be in the same folder as `prompt_corpus.md`

Kaye Chat *Dify App*:

- re-implement in Dify to support **merged response**
- Kaye Peer Coder Role:

  - Unity Engine:

    - instead of specific version, simplify ask Kaye to use Unity 6
    - give specific structure for writing MonoBehaviour script

  - Comment Section Heading:

    - rewrite CSH prompt to tighten usage
    - require filename as Level 0 CSH

[5.2.0]: https://github.com/kami-lel/kaye/compare/v5.1.0...v5.2.0

















## [5.1.0] - 2026-03-25

### Added

Kaye Chat *Dify App*:

- *Assistant Barista* role: assisting user managing *Coffee Note*
- *Editor* & *Secretary* roles, as merging & combination of various roles
- function docstring for Dify App nodes
- utilize `AbbrNode` for creating abbreviations node  from **query**

### Changed

Kaye *Python* Package:

- prompt corpus tree singleton (from `load_prompt_corpus_tree()`) always contains all dynamic nodes under root
- remove `.identifier` property from `BasePromptNode`

  - rename function `.generate_lineage()` (from `.generate_identifier_lineage()`)

- unit tests related to above changes
- update *Kaye Python Package API documentation*

Kaye Chat *Dify App*:

- update prompt related to difficulty, using another set of *anchor points* examples that will normally yield a higher value of difficult
- update used OpenAI LLM models

Kaye Commit Sense *Dify App*:

- update used OpenAI LLM models

### Removed

Kaye Chat *Dify App*:

- remaining prompt of *Translator* role
- remaining prompt of *Enclyelopic* role
- *Message Level* section of coder role

### Fixed

Kaye Chat *Dify App*:

- for coder role, no longer skip sense node
  when only provided `difficulty_override`,
  (sense node is still required for sensing PLs)

- include Annotation Markers for coder
- Input Field `difficulty_override` defaults to `-1`

[5.1.0]: https://github.com/kami-lel/kaye/compare/v5.0.1...v5.1.0














## [5.0.1] - 2026-03-06

### Changed

*Kaye Cash Tracker* Dify App:

- add environment variable `KAYE_API_PORT` to allow using debug port during development

### Fixed

Kaye HTTP API: Kaye Cash Tracker:

- fix bug in `fill_extract_prompt.py`

[5.0.1]: https://github.com/kami-lel/kaye/compare/v5.0.0...v5.0.1













## [5.0.0] - 2026-03-01

### Added

Dynamic Nodes:

- `TodayNode`
- `AbbrNode`
- `PLCNode`

Kaye Chat: Kaye Peer Coder role:

- input field `difficulty_override`
- anchor point tasks for sense prompt
- additional information for *meta content*: times for pre-sense & task

### Changed

Kaye Commit Sense:

- minor adjustment on change commit message format to utilize *Markdown*

Kaye Chat:

- merged functions of Kaye Peer Coder

### Removed

- Kaye Peer Coder
- use of `kamilog`

### Fixed

Kaye Cash Tracker:

- re-implement app using new HTTP API

[5.0.0]: https://github.com/kami-lel/kaye/compare/v4.12.1...v5.0.0













## [4.12.1] - 2026-01-18

### Changed

- unify docstring of all `.py` files of Dify App nodes

Kaye Chat:

- utilize dify LLM node's *memory* build-in function to prevent lack of context when switching LLM

Kaye Commit Sense:

- improve prompts to summarize better
- functions for disable/enable usage of markdown syntax in result

Kaye Peer Coder:

- improve prompt
- allows *prefix meta content*
- utilize *memory* build-in, v.s.

[4.12.1]: https://github.com/kami-lel/kaye/compare/v4.12.0...v4.12.1














## [4.12.0] - 2026-01-16

### Added

- Dify App **Kaye Chat**: conversation focused agent,
  dynamically change LLM based on type of conversation

- Python HTTP API:

  - unit tests for endpoints
  - `kaye_http_api.service` to enable Kaye HTTP API to be ran
  as *systemd* on Linux; & related documentations

- `PromptCorpusNode`: implement `__getitem__()` for subscriptable

### Changed

- re-implementation of `PromptBlueprint` to improve efficiency and clarity
- update Dify App *Kaye Peer Coder* structure such that it support text streaming
- complete HTTP API support for Dify App *Kaye Peer Coder*
- complete `python_api_doc.md`

[4.12.0]: https://github.com/kami-lel/kaye/compare/v4.11.0...v4.12.0













## [4.11.0] - 2026-01-09

### Added

- dify app `kaye_peer_coder`
- Kaye HTTP API to create prompts dynamically,
  and update Dify Apps to utilize the new API:

  - Kaye Cash Tracker
  - Kaye Commit Sense
  - Kaye Event Radar: non-functional in current version
  - Kaye Peer Coder: partially functional with basic static prompt

- conversation opener for Dify App Kaye Event Radar

### Changed

- use hooks-utility as Git Submodule
- add abbreviations to `prompt_corpus.md`
- start writing *Kaye Python API documentation*

### Removed

re `prompt_corpus.md`:

- rm 2D data declaration for role *Kaye Peer Coder*
- *Peer Coder* role (adapted into a dify App)

[4.11.0]: https://github.com/kami-lel/kaye/compare/v4.10.2...v4.11.0













## [4.10.2] - 2025-12-08

### Changed

- restore basic function of role: Peer Coder

dify app `kaye_cash_tracker`:

- improve push branching logic, add a fail answer node
- improve party_from and party_to extraction in prompt to prefer using given entries

[4.10.2]: https://github.com/kami-lel/kaye/compare/v4.10.1...v4.10.2














## [4.10.1] - 2025-11-24

### Changed

- role *Prompt Writer*: improvement
- dify app `kaye_cash_tracker`: use `|` for push trigger
- dify app `kaye_event_radar`: generate URLs of various websites for better interactions

[4.10.1]: https://github.com/kami-lel/kaye/compare/v4.10.0...v4.10.1














## [4.10.0] - 2025-11-20

### Added

- dify app `kaye_event_radar`, based on previous prompt-based role *Event Search*

[4.10.0]: https://github.com/kami-lel/kaye/compare/v4.9.1...v4.10.0
















## [4.9.1] - 2025-11-19

### Changed

- clean up blueprints for embedded prompts

`kaye_cash_tracker` dify app:

- clarify date extraction logic
- improve remarks creation instruction
- improve party extraction, make general

`kaye_commit_sense` dify app:

- use *promote/demote* regarding AMs
- attempt to fix wordiness

Python CLI, change args:

- change to `-f` (from `-s`)
- change to `-F` (from `-f`)
- change to `--target-file` (from `--destination-file`)

[4.9.1]: https://github.com/kami-lel/kaye/compare/v4.9.0...v4.9.1


















## [4.9.0] - 2025-10-04

### Added

- utility module `kamilog` version `v1.2.0`

### Changed

CLI:

- split parsing logic into multiple files under `./kaye/cli/`
- adjustments on option argument of `kaye prompt show/gen`

`gen_prompt` module:

- add functions `load_empty_prompt_blueprint`, `load_full_prompt_blueprint`
  and adjust related code
- use `.kaye_blueprint` to store all blueprint files

`kaye_cash_tracker` dify app:

- use secret environment variable to hide user accounts details
- provide common transaction parties for better info extraction

`kaye_commit_sense` dify app:

- different behavior dealing with single/multiple files commits
- dynamically generate prompts by `gen_prompt` module using script
- utilize `long_short_threshold` to decide if a file's change is large/small
- extract filename by code node, instead of LLM (unstable result)

### Removed

- functions of cli `kaye generate_vsc_continue_prompts`

[4.9.0]: https://github.com/kami-lel/kaye/compare/v4.8.1...v4.9.0
















## [4.8.1] - 2025-09-25

### Added

re `prompt_corpus.md`:

- add abbr

### Changed

re `dify_studio/`:

- rename `.yml` files to not use spaces
  improve execution time
- select emojis for each app
- use only Python code node instead of Jinja2 template node

[4.8.1]: https://github.com/kami-lel/kaye/compare/v4.8.0...v4.8.1





















## [4.8.0] - 2025-09-17

### Added

- new abbreviations in `prompt_corpus.md`
- Dify App: Kaye Cash Tracker
- Dify App: Kaye Commit Sense

### Changed

- abbreviations in `prompt_corpus.md`

[4.8.0]: https://github.com/kami-lel/kaye/compare/v4.7.6...v4.8.0
















## [4.7.6] - 2025-09-09

### Added

`prompt_corpus.md`:

- section `Emoji`
- role `Cash Tracker` and related blueprint
- new abbreviations

----

- script `update_prompt_blueprints_structure.py`

### Changed

- update abbreviations in `prompt_corpus.md`

[4.7.6]: https://github.com/kami-lel/kaye/compare/v4.7.5...v4.7.6













## [4.7.5] - 2025-08-14

### Changed

- improve role `git commit message`

[4.7.5]: https://github.com/kami-lel/kaye/compare/v4.7.4...v4.7.5













## [4.7.4] - 2025-08-14

### Removed

- blueprint `bibliographer`
- blueprint `book_body`

### Fixed

- update blueprints `librarian` & `librarian_bibliographer` to be used as prompt during chat
- blueprint `kyc` for missing sections

[4.7.4]: https://github.com/kami-lel/kaye/compare/v4.7.3...v4.7.4













## [4.7.3] - 2025-08-14

### Added

- abbreviations related:

  - new blueprint `all_abbreviations`
  - new blueprint `understandable_abbreviations`
  - more abbrs

### Changed

- re `prompt_corpus.md`:

  - rewrite old *book buddy* and *bibliographer* into the new **Librarian** role
  - rename previously role known as *Librarian* (and zh Librarian) to **Shelver** (and Chinese Shelver)
  - improve section `Annotation Markers` to enforce the usage of the term
  - minor update of the `Introduction` section

- improve `README.md`, especially contains a link to `prompt_corpus.md`

### Fixed

- restore section `Introduction` which was accidentally deleted
- stronger tone in paragraph preceding Understandable Abbreviations, forbid agent use these abbrs

[4.7.3]: https://github.com/kami-lel/kaye/compare/v4.7.2...v4.7.3













## [4.7.2] - 2025-08-12

### Added

- section `Elements` and `Styles` for customized language styles
- section `Briefness Style`
- section `Annotation Markers` & update related blueprints

### Changed

- split the single abbreviation table into 3 sub-lists. Utilize these abbrs in various prompts
- improve role `git_commit_message` to avoid generated output being wordy

[4.7.2]: https://github.com/kami-lel/kaye/compare/v4.7.1...v4.7.2













## [4.7.1] - 2025-08-11

### Changed

- improve `Conversation Follow Up Generation`, prefix with emoji

### Fixed

- more clearly define `Title Case`
- blueprint settings of `conversation_title_generation` and `conversation_follow_up_generation`

[4.7.1]: https://github.com/kami-lel/kaye/compare/v4.7.0...v4.7.1













## [4.7.0] - 2025-08-11

### Added

- CLI command `kaye generate_vsc_continue_prompts`: generate `.yaml` prompts that could be utilized by VS Code extension *Continue*
- blueprint `abbreviation`

### Changed

- shuffle content of `Language`, `Formats`, `Standards`
- consolidate content related to *capitalization* under section `Capitalization Style`
- content of `Comment Section Headings` to be 3-level systems

[4.7.0]: https://github.com/kami-lel/kaye/compare/v4.6.2...v4.7.0











## [4.6.2] - 2025-08-10

### Added

- blueprint `rapid`

[4.6.2]: https://github.com/kami-lel/kaye/compare/v4.6.1...v4.6.2











## [4.6.1] - 2025-08-08

### Added

- test to check runtime-generated prompt against static prompts

  - & its supporting script

### Changed

- create public function `generate_preview_tree()` of `class PromptCorpusNode` to replace direct call to `__repr__()`
- re `class PromptBlueprint`:

  - create public function `generate_preview_tree()` & `generate_prompt()` to replace direct call to `__repr__()` & `__str__()`
  - improve handling of empty lines

- re-organize & simplify all tests
- add section divider in `__main__.py` for better visual clarity

[4.6.1]: https://github.com/kami-lel/kaye/compare/v4.6.0...v4.6.1













## [4.6.0] - 2025-08-07

### Added

- section `Header Separation` and related blueprint
- section `Message Level`
- section `Commentary Capitalization` (partially from content of `Commentary Language`)

### Changed

- improve and simplify role text of `Peer Coder`
- improve section `Conversation` to prevent use of `_` for bold and italics
- some example code blocks' format, for better preview rendering

### Removed

- section `Commentary Language`

### Fixed

- corpus parsing will now keep empty lines
- ensure consistent empty lines before section header

[4.6.0]: https://github.com/kami-lel/kaye/compare/v4.5.2...v4.6.0













## [4.5.2] - 2025-07-30

### Added

- `__str__()` of `class PromptBlueprint` may include comment line
- parser flag `--no-comment` for module `kaye prompt gen`

### Changed

- improve *Conversation Follow Up Generation* role in `prompt_corpus.md`, attempt to emphasize to create short-phrase and use title case

### Fixed

- update tests criteria to accommodate new features

[4.5.2]: https://github.com/kami-lel/kaye/compare/v4.5.1...v4.5.2












## [4.5.1] - 2025-07-27

### Changed

- improve *Conversation Follow Up Generation* role (in `prompt_corpus.md`) to generate answers as follow-ups

[4.5.1]: https://github.com/kami-lel/kaye/compare/v4.5.0...v4.5.1














## [4.5.0] - 2025-07-27

### Added

- **Changelog Writer** role and blueprint
- **Conversation Follow Up Generation** role and blueprint
- *Commentary Language* blueprint

### Changed

- include more sections & improve in `prompt_writer` blueprint
- minor language fix in `prompt_corpus.md`

[4.5.0]: https://github.com/kami-lel/kaye/compare/v4.4.1...v4.5.0













## [4.4.1] - 2025-07-09
### Changed
- rename prompt blueprint `kyc` (abbr Kaye Code) from `code`
- create Commentary Language section in `prompt_corpus.md` for comment writing style
- update various tests

[4.4.1]: https://github.com/kami-lel/kaye/compare/v4.4...v4.4.1













## [4.4] - 2025-06-05
### Changed
- prompt_blueprint.py: add render datetime in version
- prompt_corpus.md:
  - improve 2d data declarations section
  - reorder Peer Coder role alphabetically
  - improve Art Tutor role with image orientation, paragraph prompts

[4.4]: https://github.com/kami-lel/kaye/compare/v4.3.1...v4.4













## [4.3.1] - 2025-06-03
### Fixed
- fix bug in `tarot_reader.txt`, prompt generation issue
### Changed
- prompt_corpus.md:
  - improve Conversation section for language consistency
  - improve Art Tutor role for better interaction

[4.3.1]: https://github.com/kami-lel/kaye/compare/v4.3...v4.3.1













## [4.3] - 2025-06-03
### Changed
- prompt_corpus.md:
  - reorganize introduction, personality, emotion response format
  - Peer Coder role updates:
    - add QML coding conventions
    - refactor code comment guidelines, add HACK instruction
    - add 2d data declarations section
  - add new Art Tutor role

[4.3]: https://github.com/kami-lel/kaye/compare/v4.2.2...v4.3













## [4.2.2] - 2025-06-02
### Changed
- rename prompt role Peer Coder (from Code Assistant)
- add Qt framework support in Peer Coder role
- improve git commit message role for shorter results
- fix bibliographer typo across project

[4.2.2]: https://github.com/kami-lel/kaye/compare/v4.2.1...v4.2.2













## [4.2.1] - 2025-05-31
### Changed
- add language switch in title generation role

[4.2.1]: https://github.com/kami-lel/kaye/compare/v4.2...v4.2.1













## [4.2] - 2025-05-31
### Added
- new prompt role Tarot Reader
### Changed
- reorganize Kaye personality prompts; move "Sir" mentions to Character section

[4.2]: https://github.com/kami-lel/kaye/compare/v4.1...v4.2













## [4.1] - 2025-05-24
### Changed
- prompt comments include blueprint name info
- improve CLI `kaye prompt ls` printout layout

[4.1]: https://github.com/kami-lel/kaye/compare/v4.0.2...v4.1













## [4.0.2] - 2025-05-24
### Fixed
- include non-Python files (.md) in Python package

[4.0.2]: https://github.com/kami-lel/kaye/compare/v4.0.1...v4.0.2













## [4.0.1] - 2025-05
### Changed
- improve conversation language consistency in prompt corpus
### Fixed
- fix CLI `kaye prompt show` blueprint retrieval bug
- fix conflicting `-f` CLI flag issue

[4.0.1]: https://github.com/kami-lel/kaye/compare/v4.0...v4.0.1













## [4.0] - 2025-05-13
### Added
- implement CLI for module
- add parsers for:
  - `python -m kaye`
  - `python -m kaye prompt`
  - `python -m kaye prompt ls`
  - `python -m kaye prompt show`
- implement technical blueprints in `prompt_blueprint_loader.py`

[4.0]: https://github.com/kami-lel/kaye/compare/v3.3...v4.0













## [3.3] - 2025-05-09
### Changed
- refactor prompt corpus from full prompt tree in `gen_prompt`
- refactor prompt blueprint from prompt template
- rewrite docstrings for clarity
- reorganize tests
- append kaye version at end of rendered prompt

[3.3]: https://github.com/kami-lel/kaye/compare/v3.2...v3.3













## [3.2] - 2025-04-18
### Changed
- merge dev branch

[3.2]: https://github.com/kami-lel/kaye/compare/v3.1...v3.2













## [3.1] - 2025-03-19
### Added
- implement `PromptTemplate` and tests

[3.1]: https://github.com/kami-lel/kaye/compare/v3.0...v3.1













## [3.0] - 2025-03-16
### Changed
- rewrite `gen_prompt` module using `anytree`
- remove vscode plugin-related module
- update full prompt

[3.0]: https://github.com/kami-lel/kaye/compare/v2.2.1...v3.0













## [2.2.1] - 2025-01-22
### Added
- add prompt for C#
### Changed
- apply minor adjustments

[2.2.1]: https://github.com/kami-lel/kaye/compare/v2.2...v2.2.1













## [2.2] - 2025-03-16
### Added
- add general role
### Changed
- translate CHANGELOG from rst to md format
- update `./kaye/prompt_full.md` for general role
- update DDC tag format in librarian role
- apply minor format adjustments

[2.2]: https://github.com/kami-lel/kaye/compare/v2.1...v2.2













## [2.1] - 2025-03-16
### Added
- add git diff summary role
### Changed
- split git-related prompts in `prompt_full.md`
- rename commit message writer role to git commit message writer
- update other files to accommodate renaming

[2.1]: https://github.com/kami-lel/kaye/compare/v2.0...v2.1













## [2.0] - 2025-03-16
### Added
- create `.gitignore` file
- add `requirement.txt`
- distribute kaye as python package with `kaye.get_prompt`, `kaye.update_vsc` submodules
- create `static_prompts` directory with `generate_static_prompts.py` script
- add initial tests

[2.0]: https://github.com/kami-lel/kaye/compare/v1.4...v2.0













## [1.4] - 2025-03-16
### Added
- add secretary role
- add librarian role
### Changed
- use ISO 639-1 language codes in prompts
- apply other prompt adjustments

[1.4]: https://github.com/kami-lel/kaye/compare/v1.3...v1.4













## [1.3] - 2025-03-16
### Added
- add editor role
- add encyclopedia role source citation
- add python docstring example for boolean-returning functions

[1.3]: https://github.com/kami-lel/kaye/compare/v1.2...v1.3













## [1.2] - 2025-03-16
### Added
- add abbreviation list for roles
### Changed
- reorganize prompt around role concept

[1.2]: https://github.com/kami-lel/kaye/compare/v1.1...v1.2













## [1.1] - 2025-03-16
### Added
- create `prompt/` directory
- add `commit_message.md` file
### Changed
- capitalize Sir reference in `system_message.md`
- rename section mission to task in `system_message.md`

[1.1]: https://github.com/kami-lel/kaye/compare/v1.0...v1.1













## [1.0] - 2025-03-16
### Added
- initial prompt for Kaye with mission adapted from ChatGPT - Genie AI extension

[1.0]: https://github.com/kami-lel/kaye/releases/tag/v1.0


























[^format]: CHANGELOG format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); Version scheme adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

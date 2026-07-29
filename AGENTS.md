----
name: kaye-engine AGENTS.md
alwaysApply: true
----

# kaye-engine AGENTS

Guidance for AI coding agents working in the **Kaye** repository. Read this
file alongside `CONTEXT.md` before making changes, and follow the exact
commands and conventions below.

## Build and Test

Set up a virtual environment and install in editable mode:

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

**Always run tests selectively** — scope each run to the files that mirror the
changed source. Run the full suite only when asked, or right before a PR/merge.

Test files mirror the source tree under `tests/`. Source-to-test mapping:

| changed source | test scope |
|---|---|
| `kaye_engine/prompt/` | `tests/prompt/` |
| `kaye_engine/api/` | `tests/api/` |
| `kaye_engine/cli/claude/` | `tests/cli/a/` |
| `kaye_engine/cli/cli_continue/` | `tests/cli/c/` |
| `kaye_engine/abbr*` | `tests/abbr/` |

Run the scoped path:

```bash
pytest tests/prompt/
pytest tests/cli/a/s/coder/
pytest tests/cli/c/p/cli-c-p-maintain_changelog_test.py
pytest tests/cli/c/p/cli-c-p-maintain_changelog_test.py::TestHeader::test_name
```

**Do not parallelize** — no `pytest-xdist`, no `-n auto`. The suite is already
fast, worker startup cancels out any gain, and splitting across workers breaks
tests that depend on run order.

Full suite — **only for PR/merge or when explicitly asked**:

```bash
pytest
```

Run the CLI and HTTP API locally. The editable install registers a
`kaye-engine` console script (`[project.scripts]` in `pyproject.toml`), so
`kaye-engine ...` and `python -m kaye_engine ...` are equivalent — prefer the
shorter `kaye-engine` form:

```bash
kaye-engine --help          # show CLI usage
kaye-engine http            # start Flask HTTP API (port 11255)
kaye-engine prompt ls                              # list registered blueprint names
kaye-engine prompt show BLUEPRINT                  # preview a blueprint's structure
kaye-engine prompt generate BLUEPRINT              # render a blueprint into a concrete prompt
kaye-engine continue config                  # export rules to ~/.continue
kaye-engine continue config LOCAL_CONFIG_FOLDER  # export to custom path
kaye-engine continue prompt PROMPTS_FOLDER        # export Continue prompts
kaye-engine claude skill SKILLS_FOLDER            # export blueprints as Skill folders
kaye-engine claude skill -z ZIPS_FOLDER           # create .zip Skill packages
kaye-engine claude plugin PLUGINS_FOLDER          # export blueprints as plugin folder
kaye-engine claude plugin -z PLUGINS_FOLDER       # create .zip package (-n omits version)
kaye-engine claude marketplace                    # export marketplace to ~/.claude/kaye_marketplace (default)
kaye-engine claude marketplace MARKETPLACE        # export to custom folder
kaye-engine claude code                           # export plugin + CLAUDE.md into ~/.claude
kaye-engine claude user-system-prompt             # export Chat blueprint to ~/.claude/CLAUDE.md
kaye-engine claude user-system-prompt -r          # use Rapid blueprint instead of Chat
kaye-engine claude user-system-prompt -c          # append Kaye Peer Coder content
kaye-engine claude vs-code-extension              # export CLAUDE.md + marketplace + settings.json into ~/.claude
```

`claude vs-code-extension` also writes `permissions` (`allow`/`ask`/`deny`
Bash command patterns) into `settings.json`, sourced from
`kaye_engine/cli/claude/permission_cmds.jsonc` (parsed with `json5`, so comments are
allowed).

CLI subcommand aliases: `http` → `h`; `prompt` → `p`;
`prompt generate` → `p g`; `continue` → `c`;
`continue config` → `c c`; `continue prompt` → `c p`;
`claude` → `anthropic`, `a`; `claude code` → `claude c`;
`claude marketplace` → `claude m`; `claude plugin` → `claude p`;
`claude skill` → `claude s`; `claude user-system-prompt` → `claude usp`;
`claude vs-code-extension` → `claude v`.

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

1. **`kaye_engine/prompt/blueprint/registrations.py`** — the single place every
   blueprint is created; call `register_blueprint()` (or the
   `_register_exportable`/`_register_prompt` partials defined near the top
   of the file) with the corpus node, setting `skill_exportable`,
   `continue_exportable`, `always_apply`, `user_invokable`, `llm_invokable`
   as needed. This is the only gate — a blueprint that isn't registered here
   is invisible to every exporter, since `claude skill`, `continue config`,
   and `continue prompt` all iterate `BLUEPRINT_REGISTRIES` directly
2. **`tests/cli/__init__.py`** — add entries to both:
   - `MD_FILENAME2SKILL_NAME`: `"kebab-slug": "Display Name"`
   - `TESTEE_FILE_CONTENT_ALL`: `"kebab-slug": ["string1", "string2", ...]`
3. **`tests/cli/a/s/<group>/cli-a-s-<group>-<slug>_test.py`** — per-skill
   content test (classes `TestBasic`, `TestHeader`, `TestStructure`,
   `TestContent`); group folders: `coder/`, `proj/`, `style/`, `pe/`,
   `others/` (catch-all incl. Elements nodes), `role/` (Role section),
   `prompts/` (workflow prompts registered via `_register_prompt`, see
   below). No separate
   structural-exportability test is needed — `tests/cli/a/__init__.py`'s
   `ALL_CLAUDE_SKILL_NAMES` derives the full skill list straight from
   `BLUEPRINT_REGISTRIES`, so parametrized suites like
   `tests/corpus/corpus-skill_frontmatter_test.py` cover any new
   registration automatically
4. **`tests/cli/c/c/<group>/cli-c-c-bp-<slug>_test.py`** — continue config
   content test; fixture is `testee_rules_folder / (display_name + ".md")`
   (file named by display name, not kebab slug)

Workflow prompts use `_register_prompt` (`llm_invokable=False`) instead of
`_register_exportable` — same `registrations.py` file, no separate module or
pipeline. They live under either `# Projects` (e.g. `Prepare for Feature
Landing`, `Prepare for Version Release`) via `_proj_node`, or `# Kaye Peer
Coder` (e.g. `Gap Review`, `Sync Unit Test`, `Resolve Merge Conflict`, `Plan
for Step By Step`)
via `_kyc_node`. Built with
`PromptBlueprint.create_from_node(<parent_node>["<Name>"])`, adding
`recursively=True` if the corpus node has `####` sub-sections — then follow
steps 2–4 the same way (test group folder `prompts/`, not the blueprint's
topic).

### `c/c` `TestHeader` description/when-to-use pattern

Every `cli-c-c-bp-*_test.py` file's `TestHeader` class has a `test_description`
test; blueprints whose `MD_FILENAME` also has an entry in
`TESTEE_WHEN_TO_USE_CONTENT_ALL` add a `test_when_to_use` test right after it:

```python
class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert assert_continue_blueprint_header_line_name(MD_FILENAME, testee_header)

    def test_description(_, testee_header):
        assert assert_description_in_continue_description_field(MD_FILENAME, testee_header)

    def test_when_to_use(_, testee_header):
        assert assert_when_to_use_in_continue_description_field(MD_FILENAME, testee_header)

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)
```

Omit `test_when_to_use` for blueprints with no `TESTEE_WHEN_TO_USE_CONTENT_ALL`
entry (e.g. `date-and-time-format`, `international-phonetic-alphabet`, most
`role/` blueprints). `assert_description_in_continue_description_field` and
`assert_when_to_use_in_continue_description_field` (`tests/cli/__init__.py`)
each do a real substring check against `TESTEE_DESCRIPTION_CONTENT_ALL` /
`TESTEE_WHEN_TO_USE_CONTENT_ALL` — both corpora were minified to short
substrings so they match regardless of PyYAML's unicode escaping of `/`, `—`,
or `↵` (U+21B5, the separator between `{description}` and `{when_to_use}`) in
the rendered Continue blueprint header.

Every class body in these test files keeps **two** blank lines before the
next `class` line (PEP 8), including before the first class after the
`# Pytest unit tests` banner — a regex-based refactor once dropped this to a
single blank line in files without `test_when_to_use`; watch for the same
regression when scripting edits across this test group.

### Export-policy flags for new blueprints

`register_blueprint()` takes three independent bools, each defaulting per
below — set per-registration in `registrations.py`, there's no separate
allow-list constant:

- `always_apply` (default `False`) — forces unconditional inclusion in the
  exported Continue AI rule regardless of relevance; currently only
  `"Kaye Peer Coder"` and `"Continue Behavior"` set this
- `user_invokable` (default `True`) — whether a human may deliberately
  invoke the entry by name; drives the exported Claude Skill's
  `user-invocable` field
- `llm_invokable` (default `True`) — whether Continue's own relevance
  matching may silently surface the entry without it being named; `True`
  exports as a Continue rule, `False` exports as a Continue Prompt (set by
  `_register_prompt`, used for workflow prompts)

## Security

- do not commit secrets, credentials, or tokens
- `.git`, `venv/`, build artifacts, and generated prompts are git-ignored;
  keep them out of commits
- the HTTP API is intended for trusted local or internal deployment; do not
  expose it publicly without review. `kaye-engine http` serves Flask's development
  server bound to `0.0.0.0`, and `-d/--debug` additionally enables the
  Werkzeug debugger — never run either on an untrusted network

## Documentation Maintenance

After meaningful changes, keep these in sync:

- `README.md` — human-facing overview and quick start
- `docs/` — programmatic API, HTTP API, corpus format, sidecar and dynamic
  nodes, abbreviations, Claude and Dify integration, personality axes
- `CONTEXT.md` — architecture, corpus structure, repository layout
- `CHANGELOG.md` — record notable changes per release
- this `AGENTS.md` — update agent-specific context as structure evolves

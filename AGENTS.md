----
name: kaye AGENTS.md
alwaysApply: true
----

# kaye AGENTS

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
| `kaye/prompt/` | `tests/prompt/` |
| `kaye/api/` | `tests/api/` |
| `kaye/cli/claude/` | `tests/cli/a/` |
| `kaye/cli/cli_continue/` | `tests/cli/c/` |
| `kaye/abbr*` | `tests/abbr/` |
| `kaye/prompt_corpus.md` | `tests/corpus/` |

Run the scoped path (add `-n auto` for a parallel run):

```bash
pytest tests/prompt/
pytest tests/cli/a/s/coder/
pytest tests/cli/c/p/cli-c-p-maintain_changelog_test.py
pytest tests/cli/c/p/cli-c-p-maintain_changelog_test.py::TestHeader::test_name
pytest -n auto tests/cli/a/  # parallel
```

Full suite — **only for PR/merge or when explicitly asked**:

```bash
pytest
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
python -m kaye claude marketplace                    # export marketplace to ~/.claude/kaye_marketplace (default)
python -m kaye claude marketplace MARKETPLACE        # export to custom folder
python -m kaye claude code                           # export plugin + CLAUDE.md into ~/.claude
python -m kaye claude user-system-prompt             # export Chat blueprint to ~/.claude/CLAUDE.md
python -m kaye claude user-system-prompt -r          # use Rapid blueprint instead of Chat
python -m kaye claude user-system-prompt -c          # append Kaye Peer Coder content
python -m kaye claude vs-code-extension              # export CLAUDE.md + marketplace + settings.json into ~/.claude
```

`claude vs-code-extension` also writes `permissions` (`allow`/`ask`/`deny`
Bash command patterns) into `settings.json`, sourced from
`kaye/cli/claude/permission_cmds.jsonc` (parsed with `json5`, so comments are
allowed).

CLI subcommand aliases: `http` → `h`; `continue` → `c`;
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

### `c/c` `TestHeader` description/when-to-use pattern

Every `cli-c-c-bp-*_test.py` file's `TestHeader` class has a `test_description`
test; blueprints whose `MD_FILENAME` also has an entry in
`TESTEE_HOW_TO_USE_CONTENT_ALL` add a `test_when_to_use` test right after it:

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

Omit `test_when_to_use` for blueprints with no `TESTEE_HOW_TO_USE_CONTENT_ALL`
entry (e.g. `date-and-time-format`, `international-phonetic-alphabet`, most
`role/` blueprints). `assert_description_in_continue_description_field` and
`assert_when_to_use_in_continue_description_field` (`tests/cli/__init__.py`)
each do a real substring check against `TESTEE_DESCRIPTION_CONTENT_ALL` /
`TESTEE_HOW_TO_USE_CONTENT_ALL` — both corpora were minified to short
substrings so they match regardless of PyYAML's unicode escaping of `/`, `—`,
or `↵` (U+21B5, the separator between `{description}` and `{when_to_use}`) in
the rendered Continue blueprint header.

Every class body in these test files keeps **two** blank lines before the
next `class` line (PEP 8), including before the first class after the
`# Pytest unit tests` banner — a regex-based refactor once dropped this to a
single blank line in files without `test_when_to_use`; watch for the same
regression when scripting edits across this test group.

### `always_apply` for new blueprints

Defaults to `False`. Only `"Chat"`, `"Coder"`, `"Agent Behavior"`,
`"Continue Behavior"` are in `_ALWAYS_APPLY_BLUEPRINT`
(`kaye/cli/cli_continue/export_blueprint_rules.py`).

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

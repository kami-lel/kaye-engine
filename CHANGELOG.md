# Kaye CHANGELOG

<!-- fixme merge role: Grammar Checker & Etiquette Coach -->
<!-- todo hooks: must update setup.cfg, for version -->

[^format]
















## [Unreleased]

### Added

- dify app `kaye_peer_coder`
- Kaye Flask HTTP API to create prompts dynamically

### Changed

- use hooks-utility as Git Submodule
- add abbreviations to `prompt_corpus.md`
- update Dify Apps to utilize the new API:

  - Kaye Cash Tracker
  - Kaye Commit Sense

dify app `kaye_event_radar`:

- add conversation opener

### Deprecated
### Removed

re `prompt_corpus.md`:

- rm 2D data declaration for role *Kaye Peer Coder*
- *Peer Coder* role (adapted into a dify App)

### Fixed













## [4.10.2] - 2025-12-08
### Changed

- restore basic function of role: Peer Coder

dify app `kaye_cash_tracker`:

- improve push branching logic, add a fail answer node
- improve party_from and party_to extraction in prompt to prefer using given entries














## [4.10.1] - 2025-11-24

### Changed

- role *Prompt Writer*: improvement
- dify app `kaye_cash_tracker`: use `|` for push trigger
- dify app `kaye_event_radar`: generate URLs of various websites for better interactions














## [4.10.0] - 2025-11-20

### Added

- dify app `kaye_event_radar`, based on previous prompt-based role *Event Search*
















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





















## [4.8.0] - 2025-09-17

### Added

- new abbreviations in `prompt_corpus.md`
- Dify App: Kaye Cash Tracker
- Dify App: Kaye Commit Sense

### Changed

- abbreviations in `prompt_corpus.md`
















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













## [4.7.5] - 2025-08-14

### Changed

- improve role `git commit message`













## [4.7.4] - 2025-08-14

### Removed

- blueprint `bibliographer`
- blueprint `book_body`

### Fixed

- update blueprints `librarian` & `librarian_bibliographer` to be used as prompt during chat
- blueprint `kyc` for missing sections













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













## [4.7.2] - 2025-08-12

### Added

- section `Elements` and `Styles` for customized language styles
- section `Briefness Style`
- section `Annotation Markers` & update related blueprints

### Changed

- split the single abbreviation table into 3 sub-lists. Utilize these abbrs in various prompts
- improve role `git_commit_message` to avoid generated output being wordy













## [4.7.1] - 2025-08-11

### Changed

- improve `Conversation Follow Up Generation`, prefix with emoji

### Fixed

- more clearly define `Title Case`
- blueprint settings of `conversation_title_generation` and `conversation_follow_up_generation`













## [4.7.0] - 2025-08-11

### Added

- CLI command `kaye generate_vsc_continue_prompts`: generate `.yaml` prompts that could be utilized by VS Code extension *Continue*
- blueprint `abbreviation`

### Changed

- shuffle content of `Language`, `Formats`, `Standards`
- consolidate content related to *capitalization* under section `Capitalization Style`
- content of `Comment Section Headings` to be 3-level systems











## [4.6.2] - 2025-08-10

### Added

- blueprint `rapid`











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













## [4.5.2] - 2025-07-30

### Added

- `__str__()` of `class PromptBlueprint` may include comment line
- parser flag `--no-comment` for module `kaye prompt gen`

### Changed

- improve *Conversation Follow Up Generation* role in `prompt_corpus.md`, attempt to emphasize to create short-phrase and use title case

### Fixed

- update tests criteria to accommodate new features













## [4.5.1] - 2025-07-27

### Changed

- improve *Conversation Follow Up Generation* role (in `prompt_corpus.md`) to generate answers as follow-ups














## [4.5.0] - 2025-07-27

### Added

- **Changelog Writer** role and blueprint
- **Conversation Follow Up Generation** role and blueprint
- *Commentary Language* blueprint

### Changed

- include more sections & improve in `prompt_writer` blueprint
- minor language fix in `prompt_corpus.md`













## [4.4.1] - 2025-07-09
### Changed
- rename prompt blueprint `kyc` (abbr Kaye Code) from `code`
- create Commentary Language section in `prompt_corpus.md` for comment writing style
- update various tests













## [4.4] - 2025-06-05
### Changed
- prompt_blueprint.py: add render datetime in version
- prompt_corpus.md:
  - improve 2d data declarations section
  - reorder Peer Coder role alphabetically
  - improve Art Tutor role with image orientation, paragraph prompts













## [4.3.1] - 2025-06-03
### Fixed
- fix bug in `tarot_reader.txt`, prompt generation issue
### Changed
- prompt_corpus.md:
  - improve Conversation section for language consistency
  - improve Art Tutor role for better interaction













## [4.3] - 2025-06-03
### Changed
- prompt_corpus.md:
  - reorganize introduction, personality, emotion response format
  - Peer Coder role updates:
    - add QML coding conventions
    - refactor code comment guidelines, add HACK instruction
    - add 2d data declarations section
  - add new Art Tutor role













## [4.2.2] - 2025-06-02
### Changed
- rename prompt role Peer Coder (from Code Assistant)
- add Qt framework support in Peer Coder role
- improve git commit message role for shorter results
- fix bibliographer typo across project













## [4.2.1] - 2025-05-31
### Changed
- add language switch in title generation role













## [4.2] - 2025-05-31
### Added
- new prompt role Tarot Reader
### Changed
- reorganize Kaye personality prompts; move "Sir" mentions to Character section













## [4.1] - 2025-05-24
### Changed
- prompt comments include blueprint name info
- improve CLI `kaye prompt ls` printout layout













## [4.0.2] - 2025-05-24
### Fixed
- include non-Python files (.md) in Python package













## [4.0.1] - 2025-05
### Changed
- improve conversation language consistency in prompt corpus
### Fixed
- fix CLI `kaye prompt show` blueprint retrieval bug
- fix conflicting `-f` CLI flag issue













## [4.0] - 2025-05-13
### Added
- implement CLI for module
- add parsers for:
  - `python -m kaye`
  - `python -m kaye prompt`
  - `python -m kaye prompt ls`
  - `python -m kaye prompt show`
- implement technical blueprints in `prompt_blueprint_loader.py`













## [3.3] - 2025-05-09
### Changed
- refactor prompt corpus from full prompt tree in `gen_prompt`
- refactor prompt blueprint from prompt template
- rewrite docstrings for clarity
- reorganize tests
- append kaye version at end of rendered prompt













## [3.2] - 2025-04-18
### Changed
- merge dev branch













## [3.1] - 2025-03-19
### Added
- implement `PromptTemplate` and tests













## [3.0] - 2025-03-16
### Changed
- rewrite `gen_prompt` module using `anytree`
- remove vscode plugin-related module
- update full prompt













## [2.2.1] - 2025-01-22
### Added
- add prompt for C#
### Changed
- apply minor adjustments













## [2.2] - 2025-03-16
### Added
- add general role
### Changed
- translate CHANGELOG from rst to md format
- update `./kaye/prompt_full.md` for general role
- update DDC tag format in librarian role
- apply minor format adjustments













## [2.1] - 2025-03-16
### Added
- add git diff summary role
### Changed
- split git-related prompts in `prompt_full.md`
- rename commit message writer role to git commit message writer
- update other files to accommodate renaming













## [2.0] - 2025-03-16
### Added
- create `.gitignore` file
- add `requirement.txt`
- distribute kaye as python package with `kaye.get_prompt`, `kaye.update_vsc` submodules
- create `static_prompts` directory with `generate_static_prompts.py` script
- add initial tests













## [1.4] - 2025-03-16
### Added
- add secretary role
- add librarian role
### Changed
- use ISO 639-1 language codes in prompts
- apply other prompt adjustments













## [1.3] - 2025-03-16
### Added
- add editor role
- add encyclopedia role source citation
- add python docstring example for boolean-returning functions













## [1.2] - 2025-03-16
### Added
- add abbreviation list for roles
### Changed
- reorganize prompt around role concept













## [1.1] - 2025-03-16
### Added
- create `prompt/` directory
- add `commit_message.md` file
### Changed
- capitalize Sir reference in `system_message.md`
- rename section mission to task in `system_message.md`













## [1.0] - 2025-03-16
### Added
- initial prompt for Kaye with mission adapted from ChatGPT - Genie AI extension













[unreleased]: https://github.com/kami-lel/kaye/compare/v4.10.2...dev
[4.10.2]: https://github.com/kami-lel/kaye/compare/v4.10.1...v4.10.2
[4.10.1]: https://github.com/kami-lel/kaye/compare/v4.10.0...v4.10.1
[4.10.0]: https://github.com/kami-lel/kaye/compare/v4.9.1...v4.10.0
[4.9.1]: https://github.com/kami-lel/kaye/compare/v4.9.0...v4.9.1
[4.9.0]: https://github.com/kami-lel/kaye/compare/v4.8.1...v4.9.0
[4.8.1]: https://github.com/kami-lel/kaye/compare/v4.8.0...v4.8.1
[4.8.0]: https://github.com/kami-lel/kaye/compare/v4.7.6...v4.8.0
[4.7.6]: https://github.com/kami-lel/kaye/compare/v4.7.5...v4.7.6
[4.7.5]: https://github.com/kami-lel/kaye/compare/v4.7.4...v4.7.5
[4.7.4]: https://github.com/kami-lel/kaye/compare/v4.7.3...v4.7.4
[4.7.3]: https://github.com/kami-lel/kaye/compare/v4.7.2...v4.7.3
[4.7.2]: https://github.com/kami-lel/kaye/compare/v4.7.1...v4.7.2
[4.7.1]: https://github.com/kami-lel/kaye/compare/v4.7.0...v4.7.1
[4.7.0]: https://github.com/kami-lel/kaye/compare/v4.6.2...v4.7.0
[4.6.2]: https://github.com/kami-lel/kaye/compare/v4.6.1...v4.6.2
[4.6.1]: https://github.com/kami-lel/kaye/compare/v4.6.0...v4.6.1
[4.6.0]: https://github.com/kami-lel/kaye/compare/v4.5.2...v4.6.0
[4.5.2]: https://github.com/kami-lel/kaye/compare/v4.5.1...v4.5.2
[4.5.1]: https://github.com/kami-lel/kaye/compare/v4.5.0...v4.5.1
[4.5.0]: https://github.com/kami-lel/kaye/compare/v4.4.1...v4.5.0
[4.4.1]: https://github.com/kami-lel/kaye/compare/v4.4...v4.4.1
[4.4]: https://github.com/kami-lel/kaye/compare/v4.3.1...v4.4
[4.3.1]: https://github.com/kami-lel/kaye/compare/v4.3...v4.3.1
[4.3]: https://github.com/kami-lel/kaye/compare/v4.2.2...v4.3
[4.2.2]: https://github.com/kami-lel/kaye/compare/v4.2.1...v4.2.2
[4.2.1]: https://github.com/kami-lel/kaye/compare/v4.2...v4.2.1
[4.2]: https://github.com/kami-lel/kaye/compare/v4.1...v4.2
[4.1]: https://github.com/kami-lel/kaye/compare/v4.0.2...v4.1
[4.0.2]: https://github.com/kami-lel/kaye/compare/v4.0.1...v4.0.2
[4.0.1]: https://github.com/kami-lel/kaye/compare/v4.0...v4.0.1
[4.0]: https://github.com/kami-lel/kaye/compare/v3.3...v4.0
[3.3]: https://github.com/kami-lel/kaye/compare/v3.2...v3.3
[3.2]: https://github.com/kami-lel/kaye/compare/v3.1...v3.2
[3.1]: https://github.com/kami-lel/kaye/compare/v3.0...v3.1
[3.0]: https://github.com/kami-lel/kaye/compare/v2.2.1...v3.0
[2.2.1]: https://github.com/kami-lel/kaye/compare/v2.2...v2.2.1
[2.2]: https://github.com/kami-lel/kaye/compare/v2.1...v2.2
[2.1]: https://github.com/kami-lel/kaye/compare/v2.0...v2.1
[2.0]: https://github.com/kami-lel/kaye/compare/v1.4...v2.0
[1.4]: https://github.com/kami-lel/kaye/compare/v1.3...v1.4
[1.3]: https://github.com/kami-lel/kaye/compare/v1.2...v1.3
[1.2]: https://github.com/kami-lel/kaye/compare/v1.1...v1.2
[1.1]: https://github.com/kami-lel/kaye/compare/v1.0...v1.1
[1.0]: https://github.com/kami-lel/kaye/releases/tag/v1.0













[^format]: CHANGELOG format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); Version scheme adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
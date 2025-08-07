# Kaye CHANGELOG

[^format]













## [Unreleased]

### Added

- section `Header Separation`

### Changed

- improve section *Conversation* to prevent use of `_` for bold and italics
- some example code blocks' format

### Deprecated
### Removed
### Fixed
### Security













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













[unreleased]: https://github.com/kami-lel/kaye/compare/v4.5.2...dev
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
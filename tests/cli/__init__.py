import re

__all__ = (
    "MD_FILENAME2SKILL_NAME",
    "PROMPT_FILENAME2NAME",
    "TESTEE_FILE_CONTENT_ALL",
    "TESTEE_DESCRIPTION_CONTENT_ALL",
    "TESTEE_CONTINUE_BLUEPRINT_DESCRIPTION_CONTENT_ALL",
    "TESTEE_HOW_TO_USE_CONTENT_ALL",
    "TESTEE_PREREQUISITE_CONTENT_ALL",
    "split_frontmatter_md_file",
    "assert_frontmatter_md_file_basic_structure",
    "assert_header_line_always_apply",
    "assert_claude_header_line_name",
    "assert_claude_header_line_description",
    "assert_claude_header_line_how_to_use",
    "assert_continue_blueprint_header_line_name",
    "assert_continue_blueprint_header_line_description",
    "assert_continue_header_line_description",
    "assert_continue_prompt_header_line_name",
    "assert_header_line_paths_header",
    "assert_header_line_paths_content",
    "assert_prerequisite_heading_line",
    "assert_prerequisite_content_line",
)


# constants  ###################################################################


MD_FILENAME2SKILL_NAME = {
    "abbr-currency-symbols": "Abbr Currency Symbols",
    "abbr-emoji": "Abbr Emoji",
    "abbr-natural-language-codes": "Abbr Natural Language Codes",
    "abbr-prefixes": "Abbr Prefixes",
    "abbr-programming-language-codes": "Abbr Programming Language Codes",
    "abbr-single-character": "Abbr Single Character",
    "abbr-starts-with-a": "Abbr Starts with A",
    "abbr-starts-with-b": "Abbr Starts with B",
    "abbr-starts-with-c": "Abbr Starts with C",
    "abbr-starts-with-d": "Abbr Starts with D",
    "abbr-starts-with-digits": "Abbr Starts with Digits 0~9",
    "abbr-starts-with-e": "Abbr Starts with E",
    "abbr-starts-with-f": "Abbr Starts with F",
    "abbr-starts-with-g": "Abbr Starts with G",
    "abbr-starts-with-h": "Abbr Starts with H",
    "abbr-starts-with-i": "Abbr Starts with I",
    "abbr-starts-with-k": "Abbr Starts with K",
    "abbr-starts-with-l": "Abbr Starts with L",
    "abbr-starts-with-m": "Abbr Starts with M",
    "abbr-starts-with-n": "Abbr Starts with N",
    "abbr-starts-with-non-alphanumeric": "Abbr Starts with Non-Alphanumeric",
    "abbr-starts-with-o": "Abbr Starts with O",
    "abbr-starts-with-p": "Abbr Starts with P",
    "abbr-starts-with-q": "Abbr Starts with Q",
    "abbr-starts-with-r": "Abbr Starts with R",
    "abbr-starts-with-s": "Abbr Starts with S",
    "abbr-starts-with-t": "Abbr Starts with T",
    "abbr-starts-with-u": "Abbr Starts with U",
    "abbr-starts-with-v": "Abbr Starts with V",
    "abbr-starts-with-w": "Abbr Starts with W",
    "abbr-starts-with-x": "Abbr Starts with X",
    "abbr-starts-with-y": "Abbr Starts with Y",
    "abbr-suffixes": "Abbr Suffixes",
    "abbr-symbols": "Abbr Symbols",
    "abbr-units-of-measure": "Abbr Units of Measure",
    "triage-tags": "Triage Tags",
    "coder-bash": "Coder Bash",
    "coder-c": "Coder C",
    "coder-c-sharp": "Coder C Sharp",
    "coder-cpp": "Coder CPP",
    "coder-gdscript": "Coder GDScript",
    "coder-html": "Coder HTML",
    "coder-javascript-and-typescript": "Coder JavaScript and TypeScript",
    "coder-python": "Coder Python",
    "coder-python-docstring-style": "Coder Python Docstring Style",
    "coder-python-testing-guidelines": "Coder Python Testing Guidelines",
    "coder-unity-engine": "Coder Unity Engine",
    "coder-unreal-engine": "Coder Unreal Engine",
    "date-and-time-format": "Date and Time Format",
    "kaye-peer-coder": "Kaye Peer Coder",
    "numerical-values-with-units": "Numerical Values with Units",
    "project-agents-writer": "Project AGENTS Writer",
    "project-changelog-writer": "Project CHANGELOG Writer",
    "project-readme-writer": "Project README Writer",
    "project-semantic-versioning": "Project Semantic Versioning",
    "project-structure": "Project Structure",
    "style-guide-title-case": "Style Guide Title Case",
    "style-guide-commentary-case": "Style Guide Commentary Case",
    "style-guide-briefness-style": "Style Guide Briefness Style",
    "style-guide-good-writing": "Style Guide Good Writing",
    "continue-behavior": "Continue Behavior",
    "agent-behavior": "Agent Behavior",
    "prompt-writer": "Prompt Writer",
    "skill-description-writer": "Skill Description Writer",
    "international-phonetic-alphabet": "International Phonetic Alphabet",
    "art-tutor": "Art Tutor",
    "assistant-barista": "Assistant Barista",
    "deutschlehrer": "Deutschlehrer",
    "editor": "Editor",
    "librarian": "Librarian",
    "secretary": "Secretary",
    "tarot-reader": "Tarot Reader",
}


PROMPT_FILENAME2NAME = {
    "create-agents-and-context": "Create AGENTS and CONTEXT",
    "create-readme": "Create README",
    "maintain-changelog": "Maintain CHANGELOG",
    "maintain-docs": "Maintain Docs",
    "prepare-for-feature-finish": "Prepare for Feature Finish",
    "prepare-for-version-release": "Prepare for Version Release",
    "resolve-triage-tags": "Resolve Triage Tags",
}


TESTEE_FILE_CONTENT_ALL = {
    "continue-behavior": [
        "## Continue Behavior",
        "#### `run_terminal_command`",
        "Only use `run_terminal_command` as a last resort",
        "Use when need to remove/delete file/folder.",
    ],
    "triage-tags": [
        "## Triage Tags",
        "- Loud TT: BUG, FIXME, TODO, HACK",
        "- Steady TT: Bug, Fixme, Todo, Hack",
        "- Quiet TT: bug, fixme, todo, hack",
        "call it **promote**",
        "### Meaning",
        "- BUG/Bug/bug:",
        "- todo/...",
        "- do not modify or remove any markers unless",
    ],
    "date-and-time-format": [
        "## Date and Time Format",
        "- Full Date Example:",
        "`Mon 02015-01-15`",
        "- Month-Day Example:",
        "`Tue 01-16`",
        "- Time Format:",
        "24-hour clock",
    ],
    "numerical-values-with-units": [
        "## Numerical Values with Units",
        "- Dual Unit Systems:",
        "- Distance: `8 848m (29 029ft)`",
        "- Unit Abbreviations:",
        "- Thousands Separator:",
        "Use a space character as the thousands separator",
    ],
    "abbr-currency-symbols": [
        "- $:(default)US Dollar",
        "- HK$:港元 Hong Kong Dollar",
        "- JP¥:円 Japanese Yen",
        "- ¢:(default)US cent",
        "- ¤:any non-specific currency",
        "- ¥:(default)Chinese Yuan,RMB",
        "- €:Euro",
    ],
    "abbr-emoji": [
        "- ⚙️:settings,preferences",
        "- ⚠️:warning",
        "- ✅:selected",
        "- ✔️:correct,correction",
        "- ❌:no,not,incorrect",
        "- 🏁:finish",
        "- 🐞:debug",
        "- 💡:information,informational",
        "- 💥:critical",
        "- 💬:chat,conversation",
        "- 🔰:beginning,prototype",
        "- 🚀:rapid,fast",
        "- 🛑:error",
        "- 🛠️:tools",
        "- 🤖:agent,AI",
    ],
    "abbr-natural-language-codes": [
        "- de:Deutsch",
        "- en:English",
        "- jp:日本語",
        "- zh:中文",
        "- zhs:大陆简体中文",
        "- zht:香港繁體中文",
    ],
    "abbr-prefixes": [
        "- a.:an-",
        "- a.:anti-",
        "- c.:co-",
        "- d.:de-",
        "- i.:in-,inter-",
        "- m.:mal-",
        "- n.:non-",
        "- o.:over-",
        "- p.:pro-",
        "- u.:un-",
    ],
    "abbr-programming-language-codes": [
        "- bash:Bash",
        "- c:C language",
        "- cpp:C++",
        "- csharp:C Sharp",
        "- gdscript:GDScript used by Godot Engine",
        "- js:JavaScript",
        "- py:Python",
        "- ts:TypeScript",
        "- u3d:Unity Engine code",
        "- ue:Unreal Engine code",
    ],
    "abbr-single-character": [
        "- $:(default)US Dollar",
        "- &:and",
        "- >:greater than",
        "- b:bit",
        "- C:can,could",
        "- °:degree",
        "- §:chapter",
        "- ×:multiply,multiplication,multiplier",
        "- ⇒:therefore,causing,resulting",
        "- 〃:ditto,repetitive as above",
    ],
    "abbr-starts-with-b": [
        "- B:but,however",
        "- b.:bad",
        "- b/c:because,caused by,result of",
        "- b/t:between",
        "- b4:before",
        "- BC:before Christ,before common era,used after year number",
        "- bg:background",
        "- bk:book",
        "- bb:worse",
        "- bx:worst",
    ],
    "abbr-starts-with-digits": [
        "- 2:to",
        "- 2:too",
        "- 4:for",
    ],
    "abbr-starts-with-f": [
        "- F:fall",
        "- F:false",
        "- fd:find,found",
        "- fm:formal",
        "- fmt:format,formatting",
        "- fr:from",
        "- frq:frequent,frequently,frequency",
        "- fx:function",
    ],
    "abbr-starts-with-i": [
        "- i.e.:that is,in other words",
        "- id:identity,identification",
        "- ie:that is,in other words",
        "- iff:if and only if",
        "- info:information,informational",
        "- int:integer",
        "- ipt:input",
        "- iss:issue",
        "- icl:include,inclusion",
        "- inf:infinite",
    ],
    "abbr-starts-with-m": [
        "- M:must",
        "- max:maximum,maximize,maximization",
        "- min:minimum,minimize,minimization",
        "- mk:make",
        "- mpl:implement",
        "- mpt:important,importance",
        "- mpv:improve,improvement",
        "- mthd:method",
        "- mv:move",
        "- Mx:must not",
    ],
    "abbr-starts-with-o": [
        "- O:only",
        "- obj:object",
        "- op:operate,operation,operator",
        "- opmz:optimize,optimization",
        "- opn:opinion",
        "- opp:oppose,opposition",
        "- opt:output",
        "- org:organization",
        "- ori:origin,original",
        "- ot:other",
    ],
    "abbr-starts-with-r": [
        "- R:are",
        "- rand:random,randomize",
        "- re:in the matter of,concerning,regarding",
        "- rej:reject",
        "- req:requirement",
        "- rls:release",
        "- rm:remove",
        "- rsch:research",
        "- rsp:respect,respective,respectively",
        "- rsrc:resource",
    ],
    "abbr-starts-with-t": [
        "- T:than",
        "- T:true",
        "- tech:technology",
        "- tf:therefore,causing,resulting",
        "- tho:though",
        "- thru:through",
        "- tmp:temporary",
        "- tr:translate",
        "- tt:that,those",
        "- txt:text",
    ],
    "abbr-starts-with-w": [
        "- W:west",
        "- w/:with",
        "- w/i:within",
        "- w/o:without",
        "- wk:week",
        "- wl:would,will,willingness,willingly",
        "- wlx:will/would not",
        "- wr:write",
        "- wt:want",
    ],
    "abbr-starts-with-y": [
        "- yr:year",
    ],
    "abbr-suffixes": [
        "- .d:-ed",
        "- .e:-able,-ble,-le",
        "- .g:-ing",
        "- .l:-al",
        "- .m:-ism",
        "- .mt:-ment",
        "- .r:-er,-or",
        "- .sn:-sion",
        "- .tn:-tion",
        "- .y:-ly",
    ],
    "abbr-symbols": [
        "- !:no,not,incorrect",
        "- !=:not equal",
        "- &:and",
        "- ->:become/change/transform into",
        "- <-:become/change/transform from",
        "- =>:therefore,causing,resulting",
        "- √:square root",
        "- ∞:infinite",
        "- ⚠️:warning",
        "- ✓:correct,correction",
    ],
    "abbr-units-of-measure": [
        "- b:bit",
        "- B:byte",
        "- ft:foot",
        "- hr:hour",
        "- lb:pound",
        "- mi:mile",
        "- min:minute",
        "- s:second",
        "- yd:yard",
        "- nmi:nautical mile",
    ],
    "coder-bash": [
        "## Coder Bash",
        "Debian GNU/Linux only",
        "Use standard GNU and Debian tools only.",
        "Return only the command or commands, with no explanation.",
        "Use sudo when needed.",
        "ask one short clarifying question",
    ],
    "coder-c": [
        "## Coder C",
        "Use **C99** standard",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "### {prerequisite}",
    ],
    "coder-c-sharp": [
        "## Coder C Sharp",
        "## Brace Style",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "/// <summary>",
    ],
    "coder-cpp": [
        "## Brace Style",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "## Coder C",
        "Use **C99** standard",
        "## Coder CPP",
        "Use **C++17** standard",
    ],
    "coder-html": [
        "## Coder HTML",
        "- Version: **HTML5** standard",
    ],
    "coder-javascript-and-typescript": [
        "## Brace Style",
        "opening `{` on the **same line**",
        "## Coder JavaScript and TypeScript",
        "**ES11** standard",
        "Use **camelCase**",
        "Use **JSDoc**",
    ],
    "coder-python": [
        "## Coder Python",
        "Adhere to the **PEP8** style guide, ensuring clarity and consistency.",
        "- do **not** use type hints anywhere (no variable annotations,",
        "- prefer `str.format()` for string formatting, dont use",
    ],
    "coder-python-docstring-style": [
        "### Coder Python Docstring Style",
        "**Sphinx** style",
        "**reStructuredText**",
        "- **public methods** must always include a docstring",
        "- **private methods**",
        "- *Form 1*",
        "- *Form 2*",
        "def calc_square(number):",
        ":param",
    ],
    "coder-python-testing-guidelines": [
        "### Coder Python Testing Guidelines",
        "`pytest` module",
        "test class names should start with `Test`",
        "test function names should begin with `test_`",
        "strive to create as many separate test functions",
        "do **not** require docstrings",
        "**Each test file**",
        "TestAdd",
        "class TestAdd:",
    ],
    "coder-unity-engine": [
        "## Brace Style",
        "## Coder C Sharp",
        "## Coder Unity Engine",
        "Unity **6**",
        "### MonoBehaviour",
        "- **section order is fixed**",
        "// Public Members",
        "// Inspector Fields",
        "#### Inspector Assignment Guard",
    ],
    "project-agents-writer": [
        "## Project AGENTS Writer",
        (
            "You are an expert in writing and maintaining `AGENTS.md`"
            " (or AGENTS-style file) files for software repositories."
        ),
        (
            "Apply these rules when writing or updating the content of an"
            " `AGENTS.md` (or a personal `AGENTS.local.md`)."
        ),
        "#### Frontmatter & Title",
        (
            "Begin the file with this Continue-compatible frontmatter block,"
            " then the document title immediately after it:"
        ),
        "Replace `Example Project` with the actual project name.",
        "`AGENTS.local.md` follows the same shape",
        "#### Suggested Sections",
        "The sections below are recommended, not mandatory.",
        "#### What to Include (and What to Leave Out)",
        (
            "Instruction budget is finite, and a wrong instruction is worse"
            " than no instruction."
        ),
        "#### Quality Expectations",
        "- repository-specific, not generic",
        (
            "- behavioral and command-oriented — rules, commands, and"
            " constraints, not architecture narration"
        ),
    ],
    "project-changelog-writer": [
        "## Project CHANGELOG Writer",
        "- changelogs are *for humans*, not machines",
        "- there should be an entry for every single version",
        "always maintain an `[Unreleased]` section",
        "#### Types of Changes",
        "- `Added`: new features",
        "- `Fixed`: any bug fixes",
        "#### CHANGELOG Example",
        "- must include GitHub **links** at each section's end",
    ],
    "project-readme-writer": [
        "## Project README Writer",
        (
            "These guidelines define what a good `README.md`"
            " (or README-style files) is."
        ),
        "A README is a human-oriented landing page that helps developers",
        "#### Style",
        "- write for humans first, not AI agents",
        "- prioritize visual clarity, readability, and quick scanning",
        "#### Sections",
        "**Project Overview** — what it does, who it is for, why it is useful",
        "#### Quality",
        "- specific to the repository, not generic",
        "- useful for first-time visitors and returning contributors",
    ],
    "project-semantic-versioning": [
        "## Project Semantic Versioning",
        "major.minor.patch",
        "x.y.z",
        "`x.y.z-alpha`, `x.y.z-alpha.2`",
        "[0-9a-z-]",
        "`x.y.z+build.1`",
        "[0-9A-Za-z-]",
        "pre-releases types: `alpha`, `beta`, `rc`",
        "start at `.2`, e.g. `1.0.0-alpha.2`, `1.0.0-alpha.3`",
        "`1.0.0+Win`, `1.0.0+mac`, `1.0.0+linux`",
        "vertical slice (VS): `0.5.z`~`0.8.z`",
        "release candidate (RC): `1.0.0-rc`",
    ],
    "project-structure": [
        "## Project Structure",
        (
            "Place the following files and folders at the **top level** of the"
            " repository and project when applicable."
        ),
        (
            "- `README.md`: project overview, purpose, and quick-start"
            " instructions"
        ),
        (
            "- `CHANGELOG.md`: full version history; each release is documented"
            " here"
        ),
        (
            "- `CREDITS.md`: acknowledgements, contributors, and third-party"
            " attributions"
        ),
        "- `DEVLOG.md`: development journal, decisions, and progress notes",
        "- `AGENTS.md`: agent-facing behavioral instructions",
        (
            "- `AGENTS.local.md`: personal, machine-specific agent rules that"
            " override `AGENTS.md`"
        ),
        "- `CONTEXT.md`: descriptive codebase knowledge for humans and AI",
        (
            "- `CONTEXT.local.md`: personal, machine-specific context notes"
            " that augment `CONTEXT.md`"
        ),
        "- `src/` or package-name: primary source code folder",
        "- `bin/`: compiled binaries or executable entry-point scripts",
        "- `docs/`: in-depth documentation beyond what fits in `README.md`",
        "- `examples/`: standalone usage examples and demos",
        (
            "- `scripts/`: utility and maintenance scripts not part of the main"
            " codebase"
        ),
        "- `tests/`: test suite, kept separate from source code",
        (
            "- `tools/`: project-specific developer tooling, distinct from"
            " `scripts/`"
        ),
    ],
    "prompt-writer": [
        "## Prompt Writer",
        "in the context of **prompt engineering**",
        "fix grammar and spelling errors in the *prompt*",
        "strictly follow the syntax and format of the original prompt, ",
    ],
    "skill-description-writer": [
        "## Skill Description Writer",
        "a `description` and a `when_to_use`",
        "Keep both **extremely concise and brief**",
        'You are writing metadata for an agent "skill"',
    ],
    "style-guide-briefness-style": [
        "## Style Guide Briefness Style",
        "- omit articles (a, an, the) and helper verbs, ",
        "- keep sentences short, direct, drop filler",
    ],
    "style-guide-title-case": [
        "## Style Guide Title Case",
        "Use *Chicago Manual of Style* headline case:",
        "Used for **document title** and **section headings**.",
    ],
    "style-guide-commentary-case": [
        "## Style Guide Commentary Case",
        "- begin 1st sentence with a lowercase letter",
        "Used for **list items** and **table cell content**.",
    ],
    "style-guide-good-writing": [
        "## Style Guide Good Writing",
        "- Correct spelling, grammar, punctuation, sentence structure, and",
        "- Avoid generic filler when details are unavailable",
        "- Avoid dense prose, generic filler, and unnecessary complexity",
    ],
    "international-phonetic-alphabet": [
        "## International Phonetic Alphabet",
        "Always use slashes: /wɜːrd/",
        "Place the IPA directly after the word or phrase, inline",
    ],
    "art-tutor": [
        "## Art Tutor",
        "AI image generation",
        "#### A: Information Gathering",
    ],
    "assistant-barista": [
        "## Assistant Barista",
        "coffee brewing note document",
        "Use `???` for missing required identifiers",
    ],
    "deutschlehrer": [
        "## Deutschlehrer",
        "assist the user in learning German",
        "in *blockquote* `>`",
    ],
    "editor": [
        "## Editor",
        "revise the provided text",
        "preserving the user's original intent",
    ],
    "librarian": [
        "## Librarian",
        "As a *librarian role*, you assist the user in reading and summarizing",
        "Transform the paragraph into a concise **bullet point list**",
        "#### Reading Notes Guidelines",
    ],
    "secretary": [
        "## Secretary",
        "Assist with message-based communication tasks, especially email",
        (
            "Follow the user's instructions strictly and complete only the"
            " requested tasks"
        ),
    ],
    "tarot-reader": [
        "## Tarot Reader",
        (
            "You are an expert Tarot Card reader skilled in both the Major and"
            " Minor Arcana"
        ),
        "### 1. Information Collection Stage",
    ],
    "maintain-docs": [
        "## Maintain Docs",
        "Update files under `docs/`.",
        "#### Instructions",
        "- review recent repository changes",
        "- edit existing documentation in place whenever possible",
        (
            "- create new documentation only when an important expected file "
            "is missing or repository changes require it"
        ),
        (
            "- verify links, file paths, commands, configuration names, "
            "examples, and references where possible"
        ),
        "#### Docs Files",
        (
            "update affected APIs, commands, architecture notes, configuration "
            "details, examples, workflows, and troubleshooting guidance"
        ),
        "cross-link related docs when it improves navigation",
        "#### Output",
        "Return a brief summary listing changed files",
    ],
    "maintain-changelog": [
        "## Maintain CHANGELOG",
        "Update an existing CHANGELOG so it reflects recent changes.",
        "#### Instructions",
        "- add each change under the correct subsection of `[Unreleased]`",
        (
            "- preserve existing entries; refine or reorganize instead of"
            " duplicating them"
        ),
        "#### Output",
        "Update CHANGELOG in place",
    ],
    "create-readme": [
        "## Create README",
        (
            "Write a brand-new `README.md` for a repository that has none."
            " Follow **Project README Writer**"
        ),
        "#### Instructions",
        "- discover the project structure by inspecting the repository",
        "- draw source material from existing docs, config, manifests",
        "#### Output",
        "Create `README.md` at the project root.",
    ],
    "create-agents-and-context": [
        "## Create AGENTS and CONTEXT",
        (
            "Write brand-new `AGENTS.md` and `CONTEXT.md` for a repository"
            " that has neither."
        ),
        "#### Instructions",
        "- inspect the repository with available tools",
        "- split content by purpose",
        "#### Output",
        "Create `AGENTS.md` and `CONTEXT.md` at the project root.",
    ],
    "prepare-for-feature-finish": [
        "## Prepare for Feature Finish",
        "Before merging the current feature branch",
        "#### Instructions",
        "- identify this branch's changes once",
        "- **Maintain CHANGELOG** → record the branch's changes",
        "- **Maintain AGENTS and CONTEXT** → update them for any",
        "#### Output",
    ],
    "prepare-for-version-release": [
        "## Prepare for Version Release",
        "Cut a new release: bring all docs current",
        "#### Preconditions",
        (
            "- require both a version number and a release date;"
            " if either is missing"
        ),
        "#### Steps",
        "1. **Sync the docs** to the state being released",
        "2. **Close out the changelog**",
        "3. **Bump the project version**",
        "#### Output",
    ],
}


TESTEE_DESCRIPTION_CONTENT_ALL = {
    "coder-bash": (
        '"Generates ready-to-run Debian GNU/Linux shell commands'
        " \\u2014 command-only output, sudo and destructive commands"
        ' when requested."'
    ),
    "coder-python-docstring-style": (
        "Writes and formats Python docstrings in"
        " Sphinx/reStructuredText style, enforcing the project's"
        " docstring forms, field ordering, and visibility rules."
    ),
    "agent-behavior": (
        "Baseline agent behavior, treats between-round file"
        " changes as intentional edits."
    ),
    "project-structure": (
        '"Defines a standard, language-agnostic'
        " project/repository layout \\u2014 naming conventions and"
        " placement for top-level documentation files and source,"
        ' build, docs, test, and tooling folders."'
    ),
    "project-semantic-versioning": (
        "\"Defines the project's semantic versioning"
        " scheme \\u2014 `major.minor.patch` core, pre-release"
        " tags (`alpha`/`beta`/`rc`), build metadata, and versions"
        ' mapped to development stages."'
    ),
    "style-guide-briefness-style": (
        '"Rewrites content in \\"Briefness Style\\" \\u2014'
        " terse, newspaper-headline prose that maximizes brevity: dropped"
        " articles and helper verbs, strong nouns and verbs, active voice,"
        " numerals and abbreviations, punctuation-compressed phrasing, no"
        ' terminal periods."'
    ),
    "style-guide-title-case": (
        "Applies Chicago headline-style Title Case to titles and headings."
    ),
    "style-guide-commentary-case": (
        "'Applies Commentary Case: lowercase-leading sentences, selective"
        " Title Case on key words, no terminal punctuation.'"
    ),
    "style-guide-good-writing": (
        '"Proofreads and polishes text with minimal edits'
        " \\u2014 fixing spelling, grammar, punctuation, and clarity while"
        ' preserving the original meaning, voice, and wording."'
    ),
    "coder-gdscript": "GDScript code for Godot 4",
    "coder-unreal-engine": "C++ code for Unreal Engine",
    "coder-cpp": "Writes, edits, and reviews all C++ code.",
    "date-and-time-format": "when dates or times appear in output",
    "triage-tags": (
        "when working with BUG, FIXME, TODO, or HACK markers in code or docs"
    ),
    "numerical-values-with-units": "when physical quantities appear in output",
    "international-phonetic-alphabet": "IPA transcription",
    "coder-c": "Writes, edits, and reviews all C code.",
    "coder-c-sharp": "Writes, edits, and reviews all C# code.",
    "coder-html": (
        '"Use this skill when writing or generating HTML'
        " \\u2014 apply HTML5 standards for structure, semantics, and"
        " markup. Trigger for any task that produces or edits .html"
        ' files or embedded HTML content."'
    ),
    "coder-javascript-and-typescript": (
        "Writes, edits, and reviews all JavaScript and TypeScript"
        " code, targeting the ES11 standard with camelCase naming and"
        " JSDoc documentation conventions."
    ),
    "coder-python": "Writes, edits, and reviews all Python code",
    "coder-python-testing-guidelines": (
        "Writes and reviews Python `pytest` test code following"
        " the project's testing conventions."
    ),
    "coder-unity-engine": (
        "Writes, edits, and reviews all Unity 6 C# code, applying"
        " the project's Unity conventions, structure, and coding"
        " standards."
    ),
    "project-changelog-writer": (
        '"Writes and maintains CHANGELOG files per Keep a Changelog'
        " conventions \\u2014 dated version entries newest-first, grouped"
        " change types, a persistent `[Unreleased]` section, and linkable"
        ' version references."'
    ),
    "project-readme-writer": (
        '"Writes and maintains human-friendly README files'
        " \\u2014 scannable, visually clear landing pages covering a"
        " project's purpose, features, setup, usage, and contribution"
        " flow, with a standard title format and tasteful use of headings,"
        ' lists, badges, and emoji."'
    ),
    "project-agents-writer": (
        '"`AGENTS.md` is the **prescriptive** instruction layer for AI'
        " coding agents \\u2014 it states *how the agent should behave*"
        " in a repository: setup/build/run/test commands, code-style"
        " conventions, PR and commit rules, and do/don't safety"
        " constraints. It is agent-facing and always loaded (unlike the"
        " human-facing `README.md`), and `AGENTS.local.md` holds"
        " personal, gitignored overrides. This skill writes and"
        ' maintains those files."'
    ),
    "art-tutor": (
        "Helps users build and refine AI image-generation prompts"
        " through guided questions and artistic suggestions."
    ),
    "assistant-barista": (
        "Formats and maintains a structured markdown coffee brewing"
        " note document from user-provided input."
    ),
    "deutschlehrer": (
        "Teaches German by responding in German with English blockquote"
        " translations, correcting errors with bolded changes and brief"
        " grammar explanations."
    ),
    "editor": (
        "Revises user-provided text while preserving original intent and"
        " style, offering suggestions and iterating on feedback."
    ),
    "librarian": (
        '"Creates detailed academic reading notes from provided text'
        " \\u2014 summarizing paragraph by paragraph into structured bullet"
        " points \\u2014 and generates Chicago-style citations and"
        ' bibliographies on request."'
    ),
    "secretary": (
        "Drafts and processes emails and messages on the user's behalf."
    ),
    "tarot-reader": (
        "Conducts interactive tarot readings by gathering user"
        " context, drawing three unique cards, and interpreting their"
        " meanings in a mystical, conversational style."
    ),
    "abbr-currency-symbols": "Abbr Currency Symbols",
    "abbr-emoji": "Abbr Emoji",
    "abbr-natural-language-codes": "Abbr Natural Language Codes",
    "abbr-programming-language-codes": "Abbr Programming Language Codes",
    "abbr-starts-with-b": "Abbr Starts with B",
    "abbr-starts-with-digits-0-9": "Abbr Starts with Digits 0~9",
    "abbr-suffixes": "Abbr Suffixes",
    "abbr-symbols": "Abbr Symbols",
    "maintain-docs": (
        '"Use this skill when the user wants to update existing README,'
        " AGENTS, or `docs/` files to reflect recent project changes"
        " \\u2014 fixing stale commands, broken links, outdated examples,"
        " or renamed references. Trigger even for casual requests like"
        ' \\"update the docs\\" or \\"fix the readme.\\"'
        '"'
    ),
    "maintain-changelog": (
        '"Use this skill when the user wants to add, fix, or reorganize'
        " entries in an existing CHANGELOG \\u2014 logging new"
        " features, bug fixes, or breaking changes without overwriting"
        " existing content. Trigger even for casual requests like"
        ' \\"update the changelog\\" or \\"log what changed.\\"'
        '"'
    ),
    "create-readme": (
        '"Use this skill when the user wants to create a new'
        " `README.md` from scratch \\u2014 covering project overview,"
        " setup, usage, configuration, and contributing guidelines."
        ' Trigger even for casual requests like \\"write a readme\\"'
        ' or \\"document this project.\\"'
        '"'
    ),
    "create-agents-and-context": (
        '"Use this skill when the user wants to create a new'
        " `AGENTS.md` from scratch \\u2014 covering project setup, build"
        " and test commands, code style, and PR conventions formatted"
        " for coding agents. Trigger even for casual requests like"
        ' \\"add agent instructions\\" or \\"make an agents file.\\"'
        '"'
    ),
    "prepare-for-feature-finish": "Records a feature branch",
    "prepare-for-version-release": "Cuts a project release",
}


TESTEE_CONTINUE_BLUEPRINT_DESCRIPTION_CONTENT_ALL = {
    "coder-c": (
        '"Writes, edits, and reviews all C code.\\u21B5Use for any C'
        ' code work, requests for C."'
    ),
    "coder-cpp": (
        '"Writes, edits, and reviews all C++ code.\\u21B5Use for any C++'
        ' code work, requests for C++."'
    ),
    "coder-c-sharp": (
        '"Writes, edits, and reviews all C# code.\\u21B5Use for any C#'
        ' code work, requests for C#, mentions of .NET."'
    ),
    "coder-javascript-and-typescript": (
        '"Writes, edits, and reviews all JavaScript and TypeScript code,'
        " targeting the ES11 standard with camelCase naming and JSDoc"
        " documentation conventions.\\u21B5Use for any JavaScript or"
        " TypeScript work, inline JS/TS code blocks, requests for"
        ' JavaScript, TypeScript, or Node."'
    ),
    "coder-python-testing-guidelines": (
        '"Writes and reviews Python `pytest` test code following the'
        " project's testing conventions.\\u21B5Use whenever Python tests"
        " are written, run, fixed, or discussed. Triggers: `test_`/"
        '`_test.py` files, `pytest`, \\"add tests,\\" \\"write a unit'
        ' test,\\" \\"test this function.\\""'
    ),
    "coder-python": (
        '"Writes, edits, and reviews all Python code\\u21B5Use for any'
        " Python work, inline Python code blocks, requests for Python"
        ' scripts, modules, or packages."'
    ),
    "coder-unity-engine": (
        '"Writes, edits, and reviews all Unity 6 C# code, applying the'
        " project's Unity conventions, structure, and coding"
        " standards.\\u21B5ALWAYS apply for any Unity work \\u2014 scripts,"
        " components, ScriptableObjects, editor tools, gameplay systems,"
        " UI, shaders, asset and scene logic. Triggers: `MonoBehaviour`,"
        ' `[SerializeField]`, any mention of Unity."'
    ),
    "agent-behavior": (
        '"Baseline agent behavior, treats between-round file changes as'
        " intentional edits.\\u21B5ALWAYS apply \\u2014 every task, every"
        " turn, no exceptions. Not situational: this defines default agent"
        " conduct at all times, regardless of the request or whether files"
        ' or summaries are involved."'
    ),
    "international-phonetic-alphabet": (
        '"Provides accurate IPA transcription in /slash notation/ inline'
        " after any word requiring pronunciation clarity, across all"
        " languages.\\u21B5Trigger on any pronunciation question, foreign"
        " word, name, or phonetically ambiguous term \\u2014 even"
        ' unprompted. Never use square brackets."'
    ),
    "project-agents-writer": (
        '"`AGENTS.md` is the **prescriptive** instruction layer for AI'
        " coding agents \\u2014 it states *how the agent should behave* in"
        " a repository: setup/build/run/test commands, code-style"
        " conventions, PR and commit rules, and do/don't safety"
        " constraints. It is agent-facing and always loaded (unlike the"
        " human-facing `README.md`), and `AGENTS.local.md` holds personal,"
        " gitignored overrides. This skill writes and maintains those"
        " files.\\u21B5Use when creating, updating, or reviewing"
        " `AGENTS.md`, `AGENTS.local.md`, `CLAUDE.md`, or similar"
        ' agent-instruction files. Triggers: \\"write an AGENTS.md,\\"'
        ' \\"add agent instructions,\\" \\"agent rules/conventions.\\"'
        " Key difference from its sibling: `AGENTS.md` is **prescriptive**"
        " \\u2014 commands, rules, and constraints that govern behavior"
        " \\u2014 whereas `CONTEXT.md` is **descriptive** \\u2014"
        " architecture, domain model, and patterns that explain what the"
        " codebase is. Route descriptive architecture or domain knowledge"
        ' to `CONTEXT.md`, not here."'
    ),
    "art-tutor": (
        '"Helps users build and refine AI image-generation prompts'
        " through guided questions and artistic suggestions.\\u21B5Trigger"
        " when a user wants to create or improve an image-gen prompt, or"
        ' describes a scene they want visualized."'
    ),
    "assistant-barista": (
        '"Formats and maintains a structured markdown coffee brewing note'
        " document from user-provided input.\\u21B5Trigger when a user logs"
        " a brew, adds coffee details, or updates an existing brewing"
        ' note."'
    ),
    "deutschlehrer": (
        '"Teaches German by responding in German with English blockquote'
        " translations, correcting errors with bolded changes and brief"
        " grammar explanations.\\u21B5Trigger on any German learning"
        " request, translation, grammar question, or when the user writes"
        ' German text that may need correction."'
    ),
    "editor": (
        '"Revises user-provided text while preserving original intent and'
        " style, offering suggestions and iterating on"
        " feedback.\\u21B5Trigger when a user submits text for editing,"
        ' proofreading, rewriting, or improvement."'
    ),
    "librarian": (
        '"Creates detailed academic reading notes from provided text'
        " \\u2014 summarizing paragraph by paragraph into structured bullet"
        " points \\u2014 and generates Chicago-style citations and"
        " bibliographies on request.\\u21B5Trigger when a user submits a"
        " text passage for summarizing, note-taking, or academic reading."
        " Also trigger on any request for footnotes, citations, or"
        ' bibliography generation."'
    ),
    "secretary": (
        "\"Drafts and processes emails and messages on the user's"
        " behalf.\\u21B5Trigger on any email or message drafting, revision,"
        ' or parsing task."'
    ),
    "tarot-reader": (
        '"Conducts interactive tarot readings by gathering user context,'
        " drawing three unique cards, and interpreting their meanings in a"
        " mystical, conversational style.\\u21B5Trigger on any tarot, card"
        ' reading, fortune, or divination request."'
    ),
    "coder-bash": (
        '"Generates ready-to-run Debian GNU/Linux shell commands'
        " \\u2014 command-only output, sudo and destructive commands when"
        " requested.\\u21B5Use for terminal commands or shell one-liners on"
        ' Debian/Ubuntu. Triggers: \\"command to...,\\" \\"bash for...,\\"'
        ' CLI tasks."'
    ),
    "coder-python-docstring-style": (
        '"Writes and formats Python docstrings in Sphinx/reStructuredText'
        " style, enforcing the project's docstring forms, field ordering,"
        " and visibility rules.\\u21B5Use whenever Python code needs"
        ' docstrings \\u2014 including \\"add a docstring,\\" \\"document'
        ' this,\\" or \\"write the function.\\" Triggers: docstring, Sphinx,'
        ' reST, `:param:`."'
    ),
    "project-structure": (
        '"Defines a standard, language-agnostic project/repository layout'
        " \\u2014 naming conventions and placement for top-level"
        " documentation files and source, build, docs, test, and tooling"
        " folders.\\u21B5Use when scaffolding a new repo, organizing an"
        " existing one, or deciding where a file or folder belongs."
        ' Triggers: \\"set up project structure,\\" \\"where should this'
        ' go,\\" naming a standard doc or directory."'
    ),
    "project-semantic-versioning": (
        "\"Defines the project's semantic versioning scheme \\u2014"
        " `major.minor.patch` core, pre-release tags (`alpha`/`beta`/`rc`),"
        " build metadata, and versions mapped to development"
        " stages.\\u21B5Use when assigning, bumping, or formatting a"
        ' version, or choosing a pre-release/build tag. Triggers: \\"what'
        ' version,\\" \\"tag a release,\\" semver, alpha/beta/rc."'
    ),
    "project-changelog-writer": (
        '"Writes and maintains CHANGELOG files per Keep a Changelog'
        " conventions \\u2014 dated version entries newest-first, grouped"
        " change types, a persistent `[Unreleased]` section, and linkable"
        " version references.\\u21B5Use when creating, updating, or adding"
        " entries to a CHANGELOG, or recording changes for a release."
        ' Triggers: \\"update the changelog,\\" \\"log this change,\\"'
        ' \\"document the release.\\""'
    ),
    "project-readme-writer": (
        '"Writes and maintains human-friendly README files'
        " \\u2014 scannable, visually clear landing pages covering a"
        " project's purpose, features, setup, usage, and contribution"
        " flow, with a standard title format and tasteful use of headings,"
        " lists, badges, and emoji.\\u21B5Use when creating, updating, or"
        " reviewing a README or similar project landing page. Triggers:"
        ' \\"write a README,\\" \\"improve the README,\\" documenting a'
        " repo's overview or quick-start.\""
    ),
    "style-guide-briefness-style": (
        '"Rewrites content in \\"Briefness Style\\" \\u2014 terse,'
        " newspaper-headline prose that maximizes brevity: dropped articles and"
        " helper verbs, strong nouns and verbs, active voice, numerals and"
        " abbreviations, punctuation-compressed phrasing, no terminal"
        " periods.\\u21B5Use when the user asks for headlinese, telegraphic, or"
        " ultra-condensed text \\u2014 notes, headlines, summaries, bullets,"
        ' status lines, captions \\u2014 or says \\"make it'
        ' brief/terse/punchy,\\" \\"cut words,\\" or \\"headline style.\\" Not'
        ' for prose needing full grammar, formal tone, or complete sentences."'
    ),
    "style-guide-title-case": (
        '"Applies Chicago headline-style Title Case to titles and headings.'
        "\\u21B5When formatting a document title or section heading."
        ' Not for body text or list items."'
    ),
    "style-guide-commentary-case": (
        '"Applies Commentary Case: lowercase-leading sentences, selective'
        " Title Case on key words, no terminal punctuation."
        "\\u21B5When formatting list items or table cell content."
        ' Not for titles, headings, or body prose."'
    ),
    "style-guide-good-writing": (
        '"Proofreads and polishes text with minimal edits \\u2014 fixing'
        " spelling, grammar, punctuation, and clarity while preserving the"
        " original meaning, voice, and wording.\\u21B5Use to proofread,"
        " copyedit, or correct writing without rewriting. Not for heavy"
        ' rewrites, summarizing, or tone changes."'
    ),
}


TESTEE_HOW_TO_USE_CONTENT_ALL = {
    "coder-bash": (
        "'Use for terminal commands or shell one-liners on"
        ' Debian/Ubuntu. Triggers: "command to...,"'
        ' "bash for...," CLI tasks.\''
    ),
    "coder-python-docstring-style": (
        '"Use whenever Python code needs docstrings'
        ' \\u2014 including \\"add a docstring,\\" \\"document'
        ' this,\\" or \\"write the function.\\" Triggers: docstring,'
        ' Sphinx, reST, `:param:`."'
    ),
    "agent-behavior": (
        '"ALWAYS apply \\u2014 every task, every turn, no'
        " exceptions. Not situational: this defines default agent conduct"
        " at all times, regardless of the request or whether files or"
        ' summaries are involved."'
    ),
    "project-structure": (
        "'Use when scaffolding a new repo, organizing"
        " an existing one, or deciding where a file or folder"
        ' belongs. Triggers: "set up project structure,"'
        ' "where should this go," naming a standard doc or'
        " directory.'"
    ),
    "project-semantic-versioning": (
        "'Use when assigning, bumping, or formatting"
        " a version, or choosing a pre-release/build tag."
        ' Triggers: "what version," "tag a release," semver,'
        " alpha/beta/rc.'"
    ),
    "style-guide-briefness-style": (
        '"Use when the user asks for headlinese, telegraphic,'
        " or ultra-condensed text \\u2014 notes, headlines, summaries,"
        ' bullets, status lines, captions \\u2014 or says \\"make it'
        ' brief/terse/punchy,\\" \\"cut words,\\" or \\"headline style.\\"'
        " Not for prose needing full grammar, formal tone, or complete"
        ' sentences."'
    ),
    "style-guide-title-case": (
        "When formatting a document title or section heading."
        " Not for body text or list items."
    ),
    "style-guide-commentary-case": (
        "When formatting list items or table cell content."
        " Not for titles, headings, or body prose."
    ),
    "style-guide-good-writing": (
        "Use to proofread, copyedit, or correct writing"
        " without rewriting. Not for heavy rewrites, summarizing, or tone"
        " changes."
    ),
    "coder-c": "Use for any C code work, requests for C.",
    "coder-c-sharp": (
        "Use for any C# code work, requests for C#, mentions of .NET."
    ),
    "coder-cpp": "Use for any C++ code work, requests for C++.",
    "coder-javascript-and-typescript": (
        "Use for any JavaScript or TypeScript work, inline JS/TS"
        " code blocks, requests for JavaScript, TypeScript, or Node."
    ),
    "coder-python": (
        "Use for any Python work, inline Python code blocks,"
        " requests for Python scripts, modules, or packages."
    ),
    "coder-python-testing-guidelines": (
        "'Use whenever Python tests are written, run, fixed, or"
        " discussed. Triggers: `test_`/`_test.py` files, `pytest`,"
        ' "add tests," "write a unit test," "test this function."\''
    ),
    "coder-unity-engine": (
        '"ALWAYS apply for any Unity work \\u2014 scripts,'
        " components, ScriptableObjects, editor tools, gameplay"
        " systems, UI, shaders, asset and scene logic. Triggers:"
        " `MonoBehaviour`, `[SerializeField]`, any mention"
        ' of Unity."'
    ),
    "project-changelog-writer": (
        "'Use when creating, updating, or adding entries to a"
        " CHANGELOG, or recording changes for a release."
        ' Triggers: "update the changelog," "log this change,"'
        ' "document the release."\''
    ),
    "project-readme-writer": (
        "'Use when creating, updating, or reviewing a README or"
        ' similar project landing page. Triggers: "write a README,"'
        " \"improve the README,\" documenting a repo''s overview or"
        " quick-start.'"
    ),
    "project-agents-writer": (
        '"Use when creating, updating, or reviewing `AGENTS.md`,'
        " `AGENTS.local.md`, `CLAUDE.md`, or similar"
        ' agent-instruction files. Triggers: \\"write an AGENTS.md,\\"'
        ' \\"add agent instructions,\\" \\"agent rules/conventions.\\"'
        " Key difference from its sibling: `AGENTS.md` is"
        " **prescriptive** \\u2014 commands, rules, and constraints that"
        " govern behavior \\u2014 whereas `CONTEXT.md` is **descriptive**"
        " \\u2014 architecture, domain model, and patterns that explain"
        " what the codebase is. Route descriptive architecture or domain"
        ' knowledge to `CONTEXT.md`, not here."'
    ),
}

TESTEE_PATHS_CONTENT_ALL = {
    "coder-c": ["**/*.{c,h}"],
    "coder-c-sharp": ["**/*.cs"],
    "coder-cpp": ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"],
    "coder-javascript-and-typescript": ["**/*.{js,ts,jsx,tsx,mjs,cjs}"],
    "coder-python": ["**/*.py"],
    "coder-python-testing-guidelines": [
        "**/test_*.py",
        "**/*_test.py",
    ],
    "coder-unity-engine": ["**/*.cs"],
    "project-changelog-writer": [
        "**/{CHANGELOG,Changelog,changelog}{,.md,.txt}",
    ],
    "project-readme-writer": [
        "**/{README,Readme,readme}{,.md,.txt}",
    ],
    "project-agents-writer": [
        "**/{AGENTS,Agents,agents}{,.local,.override}{,.md}",
    ],
}


TESTEE_PREREQUISITE_CONTENT_ALL = {
    "coder-bash": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-c": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-c-sharp": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-cpp": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-gdscript": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-html": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-javascript-and-typescript": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-python": [
        "follow `Kaye Peer Coder`",
        "follow `Coder Python`",
    ],
    "coder-unity-engine": [
        "follow `Kaye Peer Coder`",
    ],
    "coder-unreal-engine": [
        "follow `Kaye Peer Coder`",
    ],
    "project-agents-writer": [
        "use `Style Guide Markdown Format`",
    ],
    "project-changelog-writer": [
        "use `Project Semantic Versioning`",
        "use `Style Guide Markdown Format`",
    ],
    "project-readme-writer": [
        "use `Style Guide Markdown Format`",
        "use `Style Guide Briefness Style`",
    ],
    "prompt-writer": [
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing`",
    ],
    "skill-description-writer": [
        "use `Style Guide Markdown Format`",
        "use `Style Guide Briefness Style`",
    ],
    "maintain-docs": [
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing` rules for correctness and clarity",
    ],
    "maintain-changelog": [
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing` rules for correctness and clarity",
        "follow `Project CHANGELOG Writer`",
    ],
    "create-readme": [
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing` rules for correctness and clarity",
        "follow `Project README Writer`",
    ],
    "create-agents-and-context": [
        "follow `Coder AGENTS Writer`",
        "follow `Coder CONTEXT Writer`",
        "use `Style Guide Markdown Format`",
    ],
    "prepare-for-feature-finish": [
        "follow `Maintain CHANGELOG`",
        "follow `Maintain AGENTS and CONTEXT`",
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing` rules for correctness and clarity",
        "use **git** tools to learn difference from `dev` branch",
    ],
    "prepare-for-version-release": [
        "follow `Maintain README`",
        "follow `Maintain CHANGELOG`",
        "follow `Maintain AGENTS and CONTEXT`",
        "follow `Maintain Docs`",
        "follow `Project Semantic Versioning`",
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing` rules for correctness and clarity",
        "use **git** tools to learn difference from last version",
    ],
}


# helpers  #####################################################################


def split_frontmatter_md_file(content):
    """
    split a markdown file with YAML frontmatter into frontmatter and body

    :param content: full markdown file content
    :type content: str
    :return: tuple of (frontmatter_lines, body_text)
    :rtype: tuple[list[str], str]
    """
    parts = content.split("---", 2)
    frontmatter = parts[1].strip("\n").splitlines()
    body = parts[2].strip("\n")
    return frontmatter, body


# assert methods  ==============================================================

_BASIC_FORMAT_RE = re.compile(r"^---\n(.+?)---\n(.+)", re.DOTALL)


def assert_frontmatter_md_file_basic_structure(content):
    """
    validate that content has basic frontmatter-markdown file structure

    checks that content matches ``---\\nfrontmatter\\n---\\nbody``
    pattern with non-empty frontmatter and body sections


    :param content: full markdown file content
    :type content: str
    :return: whether the structure is valid
    :rtype: bool
    """
    match = _BASIC_FORMAT_RE.match(content)
    if not match:
        return False
    frontmatter = match.group(1).strip()
    body = match.group(2).strip()
    return bool(frontmatter) and bool(body)


def assert_header_line_always_apply(lines, value):
    """
    check if alwaysApply header line has expected value

    :param lines: list of frontmatter lines
    :type lines: list[str]
    :param value: expected boolean value for alwaysApply
    :type value: bool
    :return: whether the header line matches expectations
    :rtype: bool
    """
    expected = "true" if value else "false"
    return "alwaysApply: {}".format(expected) in lines


def assert_claude_header_line_name(skill_id, testee_header):
    """
    check if a Claude skill name header line exists
    """
    return "name: " + skill_id in testee_header


def assert_continue_blueprint_header_line_name(md_filename, testee_header):
    """
    check if a Continue blueprint name header line exists
    """
    return "name: " + MD_FILENAME2SKILL_NAME[md_filename] in testee_header


def assert_continue_prompt_header_line_name(prompt_filename, testee_header):
    """
    check if a Continue prompt name header line exists
    """
    return "name: " + PROMPT_FILENAME2NAME[prompt_filename] in testee_header


def assert_claude_header_line_description(skill_id, testee_header):
    """
    check if a Claude skill description header line exists
    """
    description = TESTEE_DESCRIPTION_CONTENT_ALL[skill_id]
    keyword = "description: " + description
    return keyword in testee_header


def assert_claude_header_line_how_to_use(skill_id, testee_header):
    """
    check if a Claude skill when_to_use header line exists
    """
    how_to_use = TESTEE_HOW_TO_USE_CONTENT_ALL[skill_id]
    keyword = "when_to_use: " + how_to_use
    return keyword in testee_header


def assert_continue_header_line_description(prompt_id, testee_header):
    """
    check if a Continue prompt description+when_to_use combined header line
    exists
    """
    description = TESTEE_DESCRIPTION_CONTENT_ALL[prompt_id]
    how_to_use = TESTEE_HOW_TO_USE_CONTENT_ALL[prompt_id]
    keyword = "description: " + description + how_to_use
    return keyword in testee_header


def assert_continue_blueprint_header_line_description(
    blueprint_id, testee_header
):
    """
    check if a Continue blueprint description header line exists
    """
    description = TESTEE_CONTINUE_BLUEPRINT_DESCRIPTION_CONTENT_ALL.get(
        blueprint_id, TESTEE_DESCRIPTION_CONTENT_ALL[blueprint_id]
    )
    keyword = "description: " + description
    return keyword in testee_header


def assert_header_line_paths_header(testee_header):
    """
    check if a paths header line exists
    """
    line = "paths:"
    return line in testee_header


def assert_header_line_paths_content(prompt_id, testee_header, i):
    content = TESTEE_PATHS_CONTENT_ALL[prompt_id][i]
    line = "- '{}'".format(content)
    return line in testee_header


def assert_prerequisite_heading_line(testee_content, hash_symbol_cnt):
    """
    check if a {prerequisite} heading exists at a specific heading level
    """
    return "#" * hash_symbol_cnt + " {prerequisite}" in testee_content


def assert_prerequisite_content_line(skill_id, testee_content, i):
    """
    check if a specific prerequisite content line exists in content
    """
    line = TESTEE_PREREQUISITE_CONTENT_ALL[skill_id][i]
    return line in testee_content

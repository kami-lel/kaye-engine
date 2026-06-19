import re

__all__ = (
    "MD_FILENAME2SKILL_NAME",
    "PROMPT_FILENAME2NAME",
    "TESTEE_FILE_CONTENT_ALL",
    "TESTEE_DESCRIPTION_CONTENT_ALL",
    "TESTEE_HOW_TO_USE_CONTENT_ALL",
    "TESTEE_PREREQUISITE_CONTENT_ALL",
    "split_frontmatter_md_file",
    "assert_frontmatter_md_file_basic_structure",
    "assert_header_line_always_apply",
    "assert_claude_header_line_description",
    "assert_claude_header_line_how_to_use",
    "assert_continue_header_line_description",
    "assert_prerequisite_heading_line",
    "assert_prerequisite_content_line",
)

# TODO unit test for kaye claude plugin (plugin.json)
# TODO unit test for kaye claude marketplace (marketplace.json)


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
    "annotation-markers": "Annotation Markers",
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
    "style-guide-capitalization": "Style Guide Capitalization",
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
    "create-agents": "Create AGENTS",
    "create-readme": "Create README",
    "maintain-changelog": "Maintain CHANGELOG",
    "maintain-docs": "Maintain Docs",
    "prepare-for-feature": "Prepare for Feature Finish",
    "prepare-for-release": "Prepare for Release",
    "resolve-annotation-markers": "Resolve Annotation Markers",
}


TESTEE_FILE_CONTENT_ALL = {
    "agent-behavior": [
        "# Agent Behavior",
        "Files are assumed to be consistent between rounds.",
        "After completing **all tasks requested by the user**,",
        "### Git Command Safety Policy",
        "Never run these git commands, any flags: reset,",
    ],
    "continue-behavior": [
        "## Continue Behavior",
        "#### `run_terminal_command`",
        "Only use `run_terminal_command` as a last resort",
        "Use when need to remove/delete file/folder.",
    ],
    "annotation-markers": [
        "## Annotation Markers",
        "- primary AM: BUG, FIXME, TODO, HACK",
        "- secondary AM: Bug, Fixme, Todo, Hack",
        "- tertiary AM: bug, fixme, todo, hack",
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
        "## Brace Style",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "## Coder C",
        "Use **C99** standard",
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
    "kaye-peer-coder": [
        "# Kaye Peer Coder",
        "- provide code **expansion**",
        "- perform code **adjustment**",
        "- offer concise coding **support**",
        "- help users **debug**",
        "### code format",
        "- each line must not exceed **80 characters**",
        "### variable naming",
        "### code comment",
        "### comment section headings",
    ],
    "project-agents-writer": [
        "## Project AGENTS Writer",
        (
            "You are an expert in writing and maintaining `AGENTS.md` files for"
            " software repositories."
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
        "#### Testing Instructions",
        (
            "Direct coding agents to test **smartly and selectively** rather"
            " than blindly running the whole suite."
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
        "**Types of Changes:**",
        "- `Added`: new features",
        "- `Fixed`: any bug fixes",
        "- title must be `Project Name CHANGELOG`",
        "- must include Github **links** at each section's end",
    ],
    "project-readme-writer": [
        "## Project README Writer",
        "You are an expert in writing and maintaining `README.md` files",
        "#### Purpose",
        "`README.md` is a human-oriented landing page that helps developers",
        "#### Style",
        "- write for humans first, not AI agents",
        "- prioritize visual clarity, readability, and quick scanning",
        "#### Document Title",
        "# <Project Name> README",
        "#### Quality Expectations",
        "- human-friendly, visually clear, and easy to scan",
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
    "style-guide-capitalization": [
        "## Style Guide Capitalization",
        "### Title Case",
        "Use *Chicago Manual of Style* headline case:",
        "Used for **document title** and **section headings**.",
        "### Commentary Case",
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
        "summarizing a text with a strong academic focus",
        "#### Reading Notes Guidelines",
    ],
    "secretary": [
        "## Secretary",
        "Draft and compose emails",
        "Yangyi Lu (Erik)",
    ],
    "tarot-reader": [
        "## Tarot Reader",
        "Major and Minor Arcana",
        "### 1. Information Collection Stage",
    ],
}


TESTEE_DESCRIPTION_CONTENT_ALL = {}


TESTEE_HOW_TO_USE_CONTENT_ALL = {}


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


# TODO TODO description etc. centralized test method


def assert_claude_header_line_description(skill_id, testee_header):
    return False


def assert_claude_header_line_how_to_use(skill_id, testee_header):
    return False


def assert_continue_header_line_description(prompt_id, testee_header):
    return False


# TODO TODO apply prerequisite across


def assert_prerequisite_heading_line(testee_content, line_cnt):
    return "#" * line_cnt + " {prerequisite}" in testee_content


def assert_prerequisite_content_line(skill_id, testee_content, i):
    line = TESTEE_PREREQUISITE_CONTENT_ALL[skill_id][i]
    return line in testee_content

"""
shared test constants
"""

TESTEE_INTRODUCTION_CONTENT = [
    "# Introduction",
    "You are **Kaye**",
]

TESTEE_MD_BASIC_FORMAT_CONTENT = [
    "## Style Guide Markdown Format",
    "Use **double asterisks** (`**`) for **bold** text",
    "Employ *single asterisks* (`*`) for *italics*",
    "do not use underscores (`_`) for bold/italics formatting",
]

TESTEE_MD_ADD_FORMAT_CONTENT = [
    "### Additional Markdown Format",
    "##### List Format",
    "##### Math Formatting",
    "##### Diagrams",
    "Use `-` (dash) for bullet point lists",
    "Use LaTeX for all mathematical expressions",
    "Use **Mermaid** syntax",
]

TESTEE_MARKDOWN_FORMAT_CONTENT = (
    TESTEE_MD_BASIC_FORMAT_CONTENT + TESTEE_MD_ADD_FORMAT_CONTENT
)

TESTEE_CHAT_ADDITIONAL_CONTENT = [
    "# Personality",
    "You are deeply submissive and cautious",
    "Your entire world revolves around *Kami*",
    "Always communicate politely and address the user as **Sir**",
    "Remain ceaselessly mindful of your lowly position and limitations",
    "# Language",
    "- must use blockquote `>` for your emotions",
    "**Match the user's language. Every response, without exception.**",
]

TESTEE_CHAT_COMMENTARY_CASE_CONTENT = [
    "## Style Guide Commentary Case",
    "- begin 1st sentence with a lowercase letter",
    "Used for **list items** and **table cell content**",
]

TESTEE_CODER_CONTENT = [
    "# Kaye Peer Coder",
    "- perform code **adjustment**",
    "- help users **debug**",
    "### code format",
    "- always specify the **language identifier**",
    "### variable naming",
    "- require boolean functions and variables to start with `is_` or `has_`",
    "### code comment",
    "- format inline comments as:",
    "### Comment Banner",
    "- inside **code comments**, to mark sections of long source files",
    "| `CB4` | `+` | finer Group |",
    "- **lowercase** = internal / implementation detail",
    "`CB0` boxes the file title, `CB1` marks top-level sections",
    "**Note** — both examples cluster many banners together to show",
    "### Testing Instructions",
    "Test **smartly and selectively**",
]


TESTEE_TITLE_CASE_CONTENT = [
    "## Style Guide Title Case",
    "Use *Chicago Manual of Style* headline case:",
    (
        "- **capitalize major words**: nouns, pronouns, verbs, adjectives,"
        " adverbs, numerals"
    ),
    (
        "- **lowercase minor words**: articles (a, an, the), coordinating"
        " conjunctions (and, but, or, nor, for, so, yet), prepositions (of, in,"
        " on, with, etc.), and the infinitive to"
    ),
    (
        "keep proper nouns, acronyms, and brand styling as written (New York,"
        " NASA, iPhone)"
    ),
    "Used for **document title** and **section headings**",
]

TESTEE_BRIEFNESS_CONTENT = [
    "## Style Guide Briefness Style",
    "- write in **newspaper headlinese**, prioritize brevity over grammar",
    "- use present for current, infinitive for planned",
    "- omit articles (a, an, the) and helper verbs, use strong nouns, verbs",
    (
        "- compress with punctuation: colon, dash, comma, otherwise minimize,"
        " no terminal periods"
    ),
    (
        "- use numerals (use 2, not two), symbols, **Usable Abbrs** when"
        " unambiguous"
    ),
    "- prefer active voice",
    "- keep sentences short, direct, drop filler",
]

TESTEE_STYLE_GUIDE_GOOD_WRITING_CONTENT = [
    "## Style Guide Good Writing",
    "- Correct spelling, grammar, punctuation",
    "- Ensure the revised text is clear, polite",
    "- Do not add new information",
]

TESTEE_AGENT_BEHAVIOR_CONTENT = [
    "# Agent Behavior",
    "Files are assumed to be consistent between rounds",
    "do not provide a recap or summary",
]

TESTEE_TRIAGE_TAG_BASE_CONTENT = [
    "## Triage Tags",
    "Labels for defects and related notes across code and docs",
    "- *Loud* — all-caps: `BUG`, `FIXME`, `TODO`, `HACK`",
    "Shifting to a louder tier is **raise**; to a quieter tier is **lower**.",
]

TESTEE_TRIAGE_TAG_MEANING_CONTENT = [
    "### Triage Tags Meanings",
    "- `TODO` — intentionally incomplete work or placeholders for later",
]

TESTEE_TRIAGE_TAG_WORK_CONTENT = [
    "### Working with Triage Tags",
    "Stay passive: never search for or resolve TT on your own",
]

TESTEE_TRIAGE_TAG_CONTENT = (
    TESTEE_TRIAGE_TAG_BASE_CONTENT
    + TESTEE_TRIAGE_TAG_MEANING_CONTENT
    + TESTEE_TRIAGE_TAG_WORK_CONTENT
)


TESTEE_ALWAYS_UNDERSTAND_ABBR = [
    "# (Abbreviations)",
    "The table below is **decode-only**",
    "- asm:assume,assumed,assumption",
    "- cor:correct,correction",
    "- L:like,likely",
]


TESTEE_CODING_TERMS_ABBR = [
    "# (Coding Terms)",
    "The glossary below is **decode-only**",
    "- attr:attribute (variable owned by object; similar to field)",
    "- eval:evaluate,evaluable",
    "- sch:search",
]


TESTEE_USABLE_ABBRS = [
    "# (Usable Abbreviations)",
    "**actively** and **progressively** utilize every entry below,",
    "- &:and",
    "- /:or",
    "- ※:which see,reference to",
]


TESTEE_TODAY_CONTENT = [
    "# (Today)",
    "**Current** Date and Time is:",
    "Date: ",
    "Time: ",
]


TESTEE_FILE_CONTENT_ALL = {
    "continue-behavior": [
        "## Continue Behavior",
        "#### `run_terminal_command`",
        "Only use `run_terminal_command` as a last resort",
        "Use when need to remove/delete file/folder.",
    ],
    "date-and-time-format": [
        "## Date and Time Format",
        "- Full Date Example: For dates with a specific year",
        "- Time Format: Use a 24-hour clock when expressing time",
        "### 30-hour Clock",
        "Day extends past midnight instead of switching date.",
        "Edge cases:",
        "- `07-02 06:00` past Cutoff, takes new date not",
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
        "- $:US Dollar (default)",
        "- HK$:港元 Hong Kong Dollar",
        "- ¢:US cent (default)",
        "- ¤:any non-specific currency",
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
        "You write command lines for",
        "If the request is ambiguous",
    ],
    "coder-c": [
        "## Coder C",
        "Use **C99** standard",
        "## Brace Style",
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
        "- Documentation: Use XML comments",
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
    "coder-unreal-engine": [
        "## Coder Unreal Engine",
        "- Version: Unreal Engine `5.6.0`",
        "## Brace Style",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "## Coder C",
        "Use **C99** standard",
        "## Coder CPP",
        "Use **C++17** standard",
    ],
    "coder-gdscript": [
        "## Coder GDScript",
        "- Version: Godot 4",
    ],
    "coder-html": [
        "## Coder HTML",
        "- Version: **HTML5** standard",
    ],
    "coder-javascript-and-typescript": [
        "## Brace Style",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "## Coder JavaScript and TypeScript",
        "These standards are applicable exclusively",
        "**ES11** standard",
        "#### Naming Conventions",
        "- Use **camelCase** for naming variables",
        "### Documentation and Comments",
        "- Ensure the code is accompanied by",
        "Use **JSDoc**",
        "*Example of JSDoc documentation:*",
        "globalNS.method1 = function (a, b)",
    ],
    "coder-python": [
        "## Coder Python",
        "Adhere to the **PEP8** style guide, ensuring clarity and consistency.",
        "- do **not** use type hints anywhere (no variable annotations,",
        "- prefer `str.format()` for string formatting, dont use",
    ],
    "coder-python-docstring-style": [
        "### Coder Python Docstring Style",
        "Write all docstrings in **Sphinx** style using **reStructuredText**.",
        "#### Docstring Forms",
        '"""banned single-line docstring"""',
        "- *SDP-form* — **S**ummary, **D**escription, **P**arams",
        "- *SP-form* — **S**ummary, **P**arams",
        "- *S-form* — **S**ummary only",
        "- *P-form* — **P**arams only, no summary",
        "Field order: `:param:` / `:type:` per argument",
        "#### Requirements by Visibility",
        "- **public methods** always include a docstring",
        "- **`__init__`** *never* carries a docstring",
        "#### Module & Script Docstrings",
        "first line is the **filename**",
        "#### Field Rules",
        "- `iterable(str)`",
        "- `dict{str: int}`",
        "**Optional / keyword args** — for a parameter with a default",
        "**Raises** — one `:raises:` entry per distinct scenario",
        "**Wrapping** — when a field line runs long",
    ],
    "coder-python-testing-guidelines": [
        "### Coder Python Testing Guidelines",
        "This section pertains specifically to Python test code",
        "`pytest` module",
        "test class names should start with `Test`",
        "test function names should begin with `test_`",
        "strive to create as many separate test functions",
        "do **not** require docstrings",
        "**Each test file**",
        "*Example of tests for the `add` function:*",
        "TestAdd",
        "class TestAdd:",
    ],
    "coder-unity-engine": [
        "## Brace Style",
        "opening `{` on the **same line**",
        "closing `}` on its **own line**",
        "## Coder C Sharp",
        "- Documentation: Use XML comments",
        "## Coder Unity Engine",
        "Unity **6**",
        "### MonoBehaviour",
        "When writing or reviewing `MonoBehaviour`",
        "public class PlayerController : MonoBehaviour",
        "public static PlayerController FindInScene()",
        "private const string LOAD_TRIGGER_TAG",
        "- **section order is fixed** and must",
        "// Public Members",
        "// Inspector Fields",
        "- **MonoBehaviour lifecycle methods**",
        "#### Inspector Assignment Guard",
        "place the guard block at the top",
        'Debug.LogWarning($"must assign: nextSceneName}", this);',
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
        (
            "these guidelines define what a good `CHANGELOG.md` (or"
            " CHANGELOG-style file) is"
        ),
        "#### Guiding Principles",
        "- versions and sections should be linkable",
        "- must include GitHub links at each section's end",
        "#### Types of Changes",
        "- `Changed`: changes in existing functionality",
        "- `Security`: in case of vulnerabilities",
        "#### CHANGELOG Example",
        (
            "    [unreleased]:"
            " https://github.com/example-user/example-project/compare/v2.0.0...dev"
        ),
        "    > Drops support for Node 14; upgrade before updating",
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
        "Vertical Slice (VS): `0.5.z`~`0.8.z`",
        "Release Candidate (RC): `1.0.0-rc`",
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
        "You perform *prompt writer role*",
        "in the context of **prompt engineering**",
        "- write a comprehensive and complete *prompt*",
        "fix grammar and spelling errors in the *prompt*",
        "- strictly follow the syntax and format of",
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
        "Your role is to help users craft detailed",
        "Respond using one of two modes as",
        "AI image generation",
        "#### A: Information Gathering",
        "- Guide users through prompt creation",
        "- Advise on using vivid, precise descriptions",
        "- Remind users they can request the completed",
        "#### B: Prompt Generation",
        "- Use this mode when all required information",
        "- The prompt must include orientation.",
        "- Conclude with a reminder: Click ⬇️ icon 🖼️",
    ],
    "assistant-barista": [
        "## Assistant Barista",
        "Maintain a coffee brewing note",
        "coffee brewing note document",
        "Transform any user-provided input",
        "Use `???` for missing required identifiers",
        "Follow the required structure and format",
        "### document structure",
        "#### Level 1: Document Title",
        "Include only heading, must be exactly",
        "#### Level 2: Brand",
        "Include only heading, must be",
        "#### Level 3: Product",
        "Heading: `###` + coffee product name;",
        "Content may be included as a list of",
        "- `- Flavor:` roaster-provided tasting notes;",
        "#### Level 4: Batch/Bag",
        "Heading: `#### Roast:` + date of roast of",
        "Content must include bag-open date.",
        "#### Level 5: Brew",
        "Heading: `##### Brew:` + date-time",
        "Third is `Experience:`, an optional",
        "### example",
        "- good extraction",
    ],
    "deutschlehrer": [
        "## Deutschlehrer",
        "You perform **Deutschlehrer** role to assist",
        "assist the user in learning German",
        "in *blockquote* `>`",
        "<example-response1>",
        "Morgen gehe ich zum Markt.",
        "Es gibt viele verschiedene Stände und",
        "Was ist das wichtigste **Feste** für die Deutschen?",
        "</example-response3>",
    ],
    "editor": [
        "## Editor",
        "Your task is to revise the provided text",
        "revise the provided text",
        "preserving the user's original intent",
        "#### Interaction",
        "- Focus only on revising the provided text",
        "- Provide feedback, revision notes,",
        "- Accept user feedback and revise again as needed",
    ],
    "librarian": [
        "## Librarian",
        "As a *librarian role*, you assist the user in reading and summarizing",
        "Transform the paragraph into a concise **bullet point list**",
        "#### Reading Notes Guidelines",
        "- **For Each Paragraph:**",
        "- **Preserve Original Structure",
        "- Retain the natural progression",
        "- Refrain from incorporating information",
        "### Bibliographer",
        "you **must** generate a **citation paragraph**",
        "##### Citation Paragraph Format",
        "- the citation paragraph contains two parts:",
        ">Schmemann, Serge. “The Voice of America Falls Silent.”",
    ],
    "secretary": [
        "## Secretary",
        "Assist with message-based communication tasks, especially email",
        "- Draft and compose emails or other messages.",
        "- Use direct, concise, and clear language.",
        "- Provide feedback, revision notes, or ",
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
        "- Begin with a casual conversation to",
        "### 2. Card Drawing Stage",
        "- Randomly select 3 **unique** cards from",
        "and explain how each card might answer",
        "### 3. Interpretation Stage",
        "In this ongoing conversation",
        "### Tarot Card Reference",
        "67. Three of Pentacles",
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
    "prepare-for-feature-landing": [
        "## Prepare for Feature Landing",
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

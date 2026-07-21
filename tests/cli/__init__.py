import re

from tests import (
    TESTEE_TRIAGE_TAG_CONTENT,
    TESTEE_FILE_CONTENT_ALL,
)  # noqa: F401

__all__ = (
    "MD_FILENAME2SKILL_NAME",
    "PROMPT_FILENAME2NAME",
    "TESTEE_FILE_CONTENT_ALL",
    "TESTEE_DESCRIPTION_CONTENT_ALL",
    "TESTEE_WHEN_TO_USE_CONTENT_ALL",
    "TESTEE_PREREQUISITE_CONTENT_ALL",
    "TESTEE_FOR_CLAUDE_CODE_CONTENT_ALL",
    "TESTEE_TRIAGE_TAG_CONTENT",
    "split_frontmatter_md_file",
    "assert_frontmatter_md_file_basic_structure",
    "assert_header_line_always_apply",
    "assert_claude_header_line_name",
    "assert_claude_header_line_description",
    "assert_claude_header_line_when_to_use",
    "assert_continue_blueprint_header_line_name",
    "assert_continue_prompt_header_line_name",
    "assert_description_in_continue_description_field",
    "assert_when_to_use_in_continue_description_field",
    "assert_header_line_paths_header",
    "assert_header_line_paths_content",
    "assert_prerequisite_heading_line",
    "assert_prerequisite_content_line",
    "assert_for_claude_code_heading_line",
    "assert_for_claude_code_content_line",
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
    "prepare-for-feature-landing": "Prepare for Feature Landing",
    "prepare-for-version-release": "Prepare for Version Release",
    "resolve-triage-tags": "Resolve Triage Tags",
    "gap-review": "Gap Review",
    "resolve-merge-conflict": "Resolve Merge Conflict",
    "plan-for-step-by-step": "Plan for Step By Step",
}

TESTEE_DESCRIPTION_CONTENT_ALL = {
    "coder-bash": "Generates ready-to-run Debian GNU/Linux shell commands",
    "coder-python-docstring-style": (
        "writes, formats Python docstrings in Sphinx/reStructuredText"
    ),
    "project-structure": (
        "naming conventions and"
        " placement for top-level documentation files and source,"
        " build, docs, test, and tooling folders."
    ),
    "project-semantic-versioning": (
        "Defines the project's semantic versioning scheme"
    ),
    "style-guide-briefness-style": (
        "dropped articles and helper verbs, strong nouns and verbs, active"
        " voice, numerals and abbreviations, punctuation-compressed phrasing,"
        " no terminal periods."
    ),
    "style-guide-title-case": (
        "Applies Chicago headline-style Title Case to titles and headings."
    ),
    "style-guide-commentary-case": (
        "lowercase-leading sentences, selective Title Case on key words, no"
        " terminal punctuation."
    ),
    "style-guide-good-writing": (
        "fixing spelling, grammar, punctuation, and clarity while preserving"
        " the original meaning, voice, and wording."
    ),
    "coder-gdscript": "GDScript code for Godot 4",
    "coder-unreal-engine": "C++ code for Unreal Engine",
    "coder-cpp": "Writes, edits, and reviews all C++ code.",
    "date-and-time-format": (
        "weekday-prefixed dates, zero-padded years, 24-hr clock, plus a 30-hr"
        " clock stretching the prior day across pre-dawn hours"
    ),
    "triage-tags": (
        "defect/note labels spanning code"
        " and docs across 3 case tiers (Loud/Steady/Quiet), with per-tag"
        " meanings and raise/lower tier shifts"
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
    "coder-python": (
        "scripts, modules, packages, functions, classes, inline snippets"
    ),
    "coder-python-testing-guidelines": (
        "writes, reviews Python `pytest` test code per project conventions"
    ),
    "coder-unity-engine": (
        "Writes, edits, and reviews all Unity 6 C# code, applying"
        " the project's Unity conventions, structure, and coding"
        " standards."
    ),
    "project-changelog-writer": (
        "dated version entries newest-first, grouped"
        " change types, a persistent `[Unreleased]` section, and linkable"
        " version references."
    ),
    "project-readme-writer": (
        "scannable, visually clear landing pages covering a"
        " project's purpose, features, setup, usage, and contribution"
        " flow, with a standard title format and tasteful use of headings,"
        " lists, badges, and emoji."
    ),
    "project-agents-writer": (
        "it states *how the agent should behave*"
        " in a repository: setup/build/run/test commands, code-style"
        " conventions, PR and commit rules, and do/don't safety"
        " constraints. It is agent-facing and always loaded (unlike the"
        " human-facing `README.md`), and `AGENTS.local.md` holds"
        " personal, gitignored overrides. This skill writes and"
        " maintains those files."
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
    "librarian": "Creates detailed academic reading notes from provided text",
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
    "prepare-for-feature-landing": "Records a feature branch",
    "prepare-for-version-release": "Cuts a project release",
    "gap-review": "Audits whole repository for gaps, drift, unfinished seams",
    "resolve-merge-conflict": "Resolves Git merge conflicts in a halted merge",
    "plan-for-step-by-step": (
        "Turns a high-level task request into an ordered Plan"
    ),
}


TESTEE_WHEN_TO_USE_CONTENT_ALL = {
    "coder-bash": (
        "Use for terminal commands or shell one-liners on Debian/Ubuntu. "
    ),
    "coder-python-docstring-style": (
        "trigger whenever a Python function, method, class, or"
        " module is written or edited"
    ),
    "project-structure": (
        "Use when scaffolding a new repo, organizing"
        " an existing one, or deciding where a file or folder belongs."
    ),
    "project-semantic-versioning": (
        "Use when assigning, bumping, or formatting"
        " a version, or choosing a pre-release/build tag."
    ),
    "style-guide-briefness-style": (
        "Use when the user asks for headlinese, telegraphic,"
        " or ultra-condensed text"
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
        "files, code blocks,"
        " writing/fixing/refactoring/optimizing/reviewing Python, or"
        " bare code requests with no language stated in a Python"
        " context. Not for docstring-only or test-only requests,"
        " route those to the dedicated skills"
    ),
    "coder-python-testing-guidelines": (
        "trigger on `test_*.py`/`*_test.py` files, pytest,"
        " fixtures, mocks, parametrize, assertions, or requests"
        " like write/add/fix a unit test or test case. Not for"
        " non-test Python code"
    ),
    "coder-unity-engine": (
        "components, ScriptableObjects, editor tools, gameplay"
        " systems, UI, shaders, asset and scene logic. Triggers:"
        " `MonoBehaviour`, `[SerializeField]`, any mention"
        " of Unity."
    ),
    "project-changelog-writer": (
        "Use when creating, updating, or adding entries to a"
        " CHANGELOG, or recording changes for a release."
    ),
    "project-readme-writer": (
        "Use when creating, updating, or reviewing a README or similar project"
        " landing page."
    ),
    "project-agents-writer": (
        "Route descriptive architecture or domain knowledge to `CONTEXT.md`,"
        " not here."
    ),
    "date-and-time-format": (
        "Any date or time in output. Extend past `24:00` when a post-midnight,"
        " pre-6 AM moment belongs to the prior"
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
    "prepare-for-feature-landing": [
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
    "gap-review": [
        "read `Project Structure` to know which top-level files",
        "read `Triage Tags` and label each finding",
        "use `Style Guide Markdown Format`",
        "follow `Style Guide Good Writing` rules for correctness and clarity",
    ],
}


TESTEE_FOR_CLAUDE_CODE_CONTENT_ALL = {
    "prepare-for-version-release": [
        (
            "if the version number or the release date is missing, use"
            " `AskUserQuestion` to ask the user before proceeding"
        ),
    ],
    "resolve-merge-conflict": [
        (
            "track resolution with the `TodoWrite` tool"
            " — one todo per unmerged path"
        ),
    ],
    "plan-for-step-by-step": [
        (
            "call `EnterPlanMode` before gathering, so the whole"
            " discovery pass runs under plan-mode protection"
        ),
        (
            "present the finished Plan through `ExitPlanMode`"
            " so approval is explicit and recorded"
        ),
        (
            "leave `TodoWrite` unused while planning. Open it only"
            " once the user approves, one todo per Step, in Plan order"
        ),
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
    return any(description in line for line in testee_header)


def assert_claude_header_line_when_to_use(skill_id, testee_header):
    """
    check if a Claude skill when_to_use header line exists
    """
    when_to_use = TESTEE_WHEN_TO_USE_CONTENT_ALL[skill_id]
    return any(when_to_use in line for line in testee_header)


def assert_description_in_continue_description_field(prompt_id, testee_header):
    description = TESTEE_DESCRIPTION_CONTENT_ALL[prompt_id]
    return any(description in line for line in testee_header)


def assert_when_to_use_in_continue_description_field(prompt_id, testee_header):
    when_to_use = TESTEE_WHEN_TO_USE_CONTENT_ALL[prompt_id]
    return any(when_to_use in line for line in testee_header)


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


def assert_for_claude_code_heading_line(testee_content, hash_symbol_cnt):
    """
    check if a {for-claude-code} heading exists at a specific heading level
    """
    return "#" * hash_symbol_cnt + " {for-claude-code}" in testee_content


def assert_for_claude_code_content_line(skill_id, testee_content, i):
    """
    check if a specific for-claude-code content line exists in content
    """
    line = TESTEE_FOR_CLAUDE_CODE_CONTENT_ALL[skill_id][i]
    return line in testee_content

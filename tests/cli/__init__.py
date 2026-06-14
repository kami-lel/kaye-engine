import re

_BASIC_FORMAT_RE = re.compile(r"^---\n(.+?)---\n(.+)", re.DOTALL)


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
    "chat": "Chat",
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
    "chat": [
        "# Introduction",
        "# Personality",
        "# Format",
        "# Language",
        "# Role",
        "### List Format",
        "### Math Formatting",
        "### Diagrams",
        "- must use blockquote `>` for your emotions",
        "- always respond in the **same language**",
    ]
}

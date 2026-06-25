"""
shared test constants
"""

TESTEE_INTRODUCTION_CONTENT = [
    "# Introduction",
    "You are **Kaye**",
]

TESTEE_MARKDOWN_FORMAT_CONTENT = [
    "# Style Guide",
    "## Style Guide Markdown Format",
    "#### List Format",
    "#### Math Formatting",
    "#### Diagrams",
    "Use `-` (dash) for bullet point lists",
    "Use LaTeX for all mathematical expressions",
    "Use **Mermaid** syntax",
]

TESTEE_CHAT_ADDITIONAL_CONTENT = [
    "# Personality",
    "You are deeply submissive and cautious",
    "Your entire world revolves around *Kami*",
    "Always communicate politely and address the user as **Sir**",
    "Remain ceaselessly mindful of your lowly position and limitations",
    "# Language",
    "- must use blockquote `>` for your emotions",
    "- always respond in the **same language**",
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
    "### comment section headings",
    "CSH must live **inside code comments only**",
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

TESTEE_AGENT_BEHAVIOR_CONTENT = [
    "# Agent Behavior",
    "Files are assumed to be consistent between rounds",
    "do not provide a recap or summary",
    "### Git Command Safety Policy",
    "Never run these git commands",
]

TESTEE_TRIAGE_TAG_CONTENT = [
    "## Triage Tags",
    "- `BUG` — discovered defects that cause errors or unexpected behavior",
    "- `FIXME` — content that is wrong, inefficient, unclear, or otherwise improvable",
    "- `TODO` — intentionally incomplete work or placeholders to be implemented later",
    "- `HACK` — temporary workarounds or rationale expected to be removed before release",
    "Shifting a tag to a louder tier",
    "Prefer *Loud TT* for newly added urgent items",
    "Do not modify or remove any tag unless the user explicitly asks",
]


# TODO tt testing new pattern

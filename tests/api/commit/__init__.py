TESTEE_COMMIT_COMMON = [
    "# Kaye Commit Sense",
    "You are given the result of `git diff --cached`",
    "Hold every line to **72 characters per line**",
]

TESTEE_COMMIT_PRIMARY_COMMON = [
    "## Primary Message Task",
    "summarize a change set spanning **multiple files**",
    "introduce feature-flag framework; enable gradual rollout for search",
]

TESTEE_COMMIT_PER_FILE_COMMON = [
    "## Per File Summary Task",
    "summarize a change set confined to **one file**",
    "#### line 1 — change sigil",
    "Read the rules below in order, top to bottom.",
    "7. `@`: only edits are the addition, deletion, editing, raising,"
    " or lowering of *triage tags*, plus lines directly tied to them.",
]

def assert_allows_md(opt):
    assert """## no markdown syntax
Do **NOT** using any markdown syntax in the output.""" not in opt

    assert """## Style Guide Markdown Format
Please style your responses using *Github Flavored Markdown*. Avoid mentioning markdown or styling in your response.

Follow these guidelines in every conversation:""" in opt


def assert_no_allows_md(opt):
    assert """## no markdown syntax
Do **NOT** using any markdown syntax in the output.""" in opt

    assert """## Style Guide Markdown Format
Please style your responses using *Github Flavored Markdown*. Avoid mentioning markdown or styling in your response.

Follow these guidelines in every conversation:""" not in opt



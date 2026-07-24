TESTEE_COMMIT_COMMON = [
    "# Kaye Commit Sense",
    "You are given the result of `git diff --cached`",
    "Hold message line to **72 characters at max**",
]

TESTEE_COMMIT_PRIMARY_COMMON = [
    "## Primary Message Task",
    "summarizing changes spanning **multiple files**",
    "introduce feature-flag framework; enable gradual rollout for search",
]

TESTEE_COMMIT_PER_FILE_COMMON = [
    "## Per File Summary Task",
    "summarizing change set touching **one file**",
    "#### line 1 — change sigil",
    "Read rules in order, top to bottom.",
    "7. @: only edits are *triage tags* added, removed, edited, raised,"
    " lowered, plus lines tied directly to them",
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



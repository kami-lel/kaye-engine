TESTEE_COMMIT_COMMON = [
    "# Kaye Commit Sense",
    "You are given the result of `git diff --cached`",
    "**You must produce a single-line, ultra-concise summary**",
]

TESTEE_COMMIT_PRIMARY_COMMON = [
    "## Primary Message Task",
    "Produce a concise summary of changes across **multiple** files",
    "modularize payment processing; split into gateway adapters",
]

TESTEE_COMMIT_PER_FILE_COMMON = [
    "## Per File Summary Task",
    "Produce a concise summary of changes of a **single** file",
    "### Prefix Symbol",
    "Select ONE prefix for the changed file",
    "6. `@` — only edits are to triage tags",
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



from tests.api import assert_briefness_style

# FIXME use new pattern testing
# HACK remove all print out in unit tests


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


def assert_commit_sense_common(opt):
    assert """## Style Guide Commentary Case
- begin 1st sentence with a lowercase letter; use standard sentence capitalization for the 2nd and subsequent sentences
- use *Title Case* for **a few important words** within a sentence
- the last sentence should not end with punctuation""" in opt

    assert_briefness_style(opt)


def assert_per_file_common(opt):
    assert """## Per File Summary Task
Produce a concise summary of changes of a **single** file.

Eg:

- refactor date parsing to reduce duplication
- fix null-pointer crash in payment processor""" in opt

    assert """### Prefix Symbol
You are to select a single prefix that best describes the primary nature of the change to a given file. Use the following prefixes, in **priority order**. Apply the **first rule that matches**:

1. `^`: new file
2. `!`: deleted file""" in opt

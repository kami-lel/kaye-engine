def assert_allows_md(opt):
    assert """## no markdown syntax
Do **NOT** using any markdown syntax in the output.""" not in opt

    assert """# Format
Please style your responses using *Github Flavored Markdown*. Avoid mentioning markdown or styling in your response.

Follow these guidelines in every conversation:""" in opt


def assert_no_allows_md(opt):
    assert """## no markdown syntax
Do **NOT** using any markdown syntax in the output.""" in opt

    assert """# Format
Please style your responses using *Github Flavored Markdown*. Avoid mentioning markdown or styling in your response.

Follow these guidelines in every conversation:""" not in opt


def assert_commit_sense_common(opt):
    assert """### Commentary Case
- begin 1st sentence with a lowercase letter; use standard sentence capitalization for the 2nd and subsequent sentences
- use *Title Case* for **a few important words** within a sentence
- the last sentence should not end with punctuation""" in opt

    assert """## Briefness Style
- write in **newspaper headlinese**, prioritize brevity over grammar
- use present for current, infinitive for planned
- omit articles (a, an, the) and helper verbs, use strong nouns, verbs""" in opt

    assert """# Kaye Commit Sense
You are given the result of `git diff --cached`; interpret it as the changes ready to be committed for the file(s).

- strictly use *Briefness Style* language""" in opt


def assert_per_file_common(opt):
    assert """## Annotation Markers
Used to label defects and related notes across code and documentation. You must refer them as *annotation markers* or *AM*:

- primary AM: BUG, FIXME, TODO, HACK""" in opt

    assert """## Per File Summary Task
Produce a concise summary of changes of a **single** file.

Eg:

- refactor date parsing to reduce duplication
- fix null-pointer crash in payment processor""" in opt

    assert """### Prefix Symbol
You are to select a single prefix that best describes the primary nature of the change to a given file. Use the following prefixes, in **priority order**. Apply the **first rule that matches**:

1. `^`: new file
2. `!`: deleted file""" in opt

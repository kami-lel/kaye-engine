"""
prompt-bp-prompt_test.py

Unit Tests (using pytest) for: PromptBlueprint.generate_prompt()
"""

# BUG

import re

import pytest

from kaye.prompt import PromptBlueprint

from tests import TESTEE_USABLE_ABBRS
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_EMPTY,
    _split_content_and_comment,
)


class Test1:  # with PROMPT1  ##################################################

    def test_full(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = bp.generate_prompt(show_comment=True)

        print(opt)
        content, comment = _split_content_and_comment(opt)

        assert content == """# Project Title
## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License."""

        # test comment structure
        assert re.fullmatch("<!-- Kaye v.+ -->", comment)

    def test_part1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_1
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License."""

    def test_part2(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_2
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """# Project Title
## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License."""

    def test_empty(_, corpus_testee1):
        bp_text = BLUEPRINT_1_EMPTY
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == ""


class Test2:  # with PROMPT2  ##################################################

    def test_full(_, corpus_testee2):
        bp_text = BLUEPRINT_2_FULL
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """# Project Title
## Description
A brief overview of the project, its purpose, and goals.

## Installation
1. Clone the repo
2. Install dependencies
3. Run the application

## Usage
Provide instructions on how to use the application.

## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request

### description
A step-by-step guide of how to contribute

## License
This project is licensed under the MIT License."""

    def test_part1(_, bp_testee2pa1):
        bp = bp_testee2pa1

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """# Project Title
## Installation
1. Clone the repo
2. Install dependencies
3. Run the application

## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test_empty(_, corpus_testee2):
        bp_text = BLUEPRINT_2_EMPTY
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == ""


class Test3:  # with PROMPT3  ##################################################

    def test_full(_, corpus_testee3):
        bp_text = BLUEPRINT_3_FULL
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """# Main Title
## Introduction
Brief introduction to the topic.

### Background
Context or history relevant to the topic.

#### Importance
Why this topic matters in the current scenario.

##### Objective
The primary goal of this document.

## Methods
Overview of the methodologies used.

### Data Collection
How data was gathered for analysis.

#### Tools Used
List of tools utilized during the project.

##### Future Work
Suggestions for future research or tasks.

## Conclusion
Summarizing the findings and implications."""

    def test_part1(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_1
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """# Main Title
## Introduction
Brief introduction to the topic.

### Background
Context or history relevant to the topic.

#### Importance
Why this topic matters in the current scenario.

##### Objective
The primary goal of this document.

## Conclusion
Summarizing the findings and implications."""

    def test_part2(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == """# Main Title
### Background
Context or history relevant to the topic.

##### Objective
The primary goal of this document.

### Data Collection
How data was gathered for analysis.

##### Future Work
Suggestions for future research or tasks."""

    def test_empty(_, corpus_testee3):
        bp_text = BLUEPRINT_3_EMPTY
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_prompt(show_comment=False)

        print(opt)
        assert opt == ""

    def test_no_top(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2
        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        opt = bp.generate_prompt(show_comment=False, disable_first_heading=True)

        print(opt)
        assert opt == """### Background
Context or history relevant to the topic.

##### Objective
The primary goal of this document.

### Data Collection
How data was gathered for analysis.

##### Future Work
Suggestions for future research or tasks."""


@pytest.fixture(scope="class")
def opt(corpus_dynamic_testee2):
    corpus = corpus_dynamic_testee2

    bp_text = """    ○
[ ] └── Project Title
[x] │   ├── Description
[x] │   ├── Installation
[x] │   └── License
[x] └── (Usable Abbreviations)"""

    bp = PromptBlueprint.parse(bp_text, corpus_override=corpus)

    return bp.generate_prompt(show_comment=False)


class TestDynamicNodes:  #######################################################

    def test_starts_with(_, opt):
        print(opt)
        assert opt.startswith("""## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License.""")

    @pytest.mark.parametrize("marker", TESTEE_USABLE_ABBRS)
    def test_usable_abbrs(_, opt, marker):
        assert marker in opt

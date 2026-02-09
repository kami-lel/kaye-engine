"""
prompt-bp-prompt_test.py

Unit Tests (using pytest) for: PromptBlueprint.generate_prompt()
"""

# FIXME

import re


from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_2_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_EMPTY,
    _split_content_and_comment,
)


class XTest1:  # with PROMPT1  ##################################################

    def test_full(self):
        bp_text = BLUEPRINT_1_FULL
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=False)

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

    def test_part1(self):
        bp_text = BLUEPRINT_1_PARTIAL_1
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

        print(opt)
        assert opt == """## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License."""

    def test_part2(self):
        bp_text = BLUEPRINT_1_PARTIAL_2
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

        print(opt)
        assert opt == """# Project Title

## Installation
Clone the repo and install dependencies.

## License
Licensed under the MIT License."""

    def test_empty(self):
        bp_text = BLUEPRINT_1_EMPTY
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

        print(opt)
        assert opt == ""


class XTest2:  # with PROMPT2  ##################################################

    def test_full(self):
        bp_text = BLUEPRINT_2_FULL
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

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

## License
This project is licensed under the MIT License."""

    def test_part1(self):
        bp_text = BLUEPRINT_2_PARTIAL_1
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

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

    def test_empty(self):
        bp_text = BLUEPRINT_2_EMPTY
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

        print(opt)
        assert opt == ""


class XTest3:  # with PROMPT3  ##################################################

    def test_full(self):
        bp_text = BLUEPRINT_3_FULL
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

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

    def test_part1(self):
        bp_text = BLUEPRINT_3_PARTIAL_1
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

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

    def test_part2(self):
        bp_text = BLUEPRINT_3_PARTIAL_2
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

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

    def test_empty(self):
        bp_text = BLUEPRINT_3_EMPTY
        bp = PromptBlueprint.parse(self.corpus, bp_text)

        opt = bp.generate_prompt(hide_comment=True)

        print(opt)
        assert opt == ""

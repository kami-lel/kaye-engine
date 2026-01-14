"""
prompt_blueprint_prompt_test.py

Unit Tests (using pytest) for: PromptBlueprint.generate_prompt()
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode


from tests.gen_prompt import PROMPT1, PROMPT2


class Test1:  # use PROMPT1

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test1(self):
        blueprint_text = """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    # BUG
    def test2(self):
        blueprint_text = """    ○
[x] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """
# Project Title

## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test3(self):
        blueprint_text = """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Project Title

## Installation
1. Clone the repo
2. Install dependencies
3. Run the application

## Usage
Provide instructions on how to use the application."""

    def test4(self):
        blueprint_text = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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


class Test2:  # use PROMPT2

    corpus = PromptCorpusNode.parse(PROMPT2)

    def test1(self):
        blueprint_text = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test2(self):
        blueprint_text = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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

    def test3(self):
        blueprint_text = """    ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Main Title

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

    def test4(self):
        blueprint_text = """    ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Main Title

## Methods
Overview of the methodologies used.

### Data Collection
How data was gathered for analysis.

## Conclusion
Summarizing the findings and implications."""

    def test_full(self):
        blueprint_text = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptBlueprint.parse(self.corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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

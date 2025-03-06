"""
test parsing for PromptTreeNode
"""

from kaye.gen_prompt import FullPromptTreeNode


class TestRepr1:

    src = """
# Project Title

## Description
Brief overview of the project and its purpose.

## Installation
Clone the repo and install dependencies.


## License

Licensed under the MIT License.
"""

    def test(self):
        tree = FullPromptTreeNode(self.src)
        assert repr(tree) == """Project Title
    Description
                Brief overview of the project and its purpose.
    Installation
                Clone the repo and install dependencies.
    License
                Licensed under the MIT License.⏎
"""


class TestRepr2:

    src = """
# Project Title
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
This project is licensed under the MIT License.
"""

    def test(self):
        tree = FullPromptTreeNode(self.src)
        assert repr(tree) == """Project Title
    Description
                A brief overview of the project, its purpose, and goals.
    Installation
                1. Clone the repo⏎2. Install dependencies⏎3. Run the applicatio
    Usage
                Provide instructions on how to use the application.
    Contributing
                1. Fork the repo⏎2. Create a new branch⏎3. Submit a pull reques
    License
                This project is licensed under the MIT License.⏎
"""


class TestRepr3:

    src = """
# Main Title

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
Summarizing the findings and implications.
"""

    def test(self):
        tree = FullPromptTreeNode(self.src)
        assert repr(tree) == """Main Title
    Introduction
                Brief introduction to the topic.
        Background
                    Context or history relevant to the topic.
            Importance
                        Why this topic matters in the current scenario.
                Objective
                            The primary goal of this document.
    Methods
                Overview of the methodologies used.
        Data Collection
                    How data was gathered for analysis.
            Tools Used
                        List of tools utilized during the project.
                Future Work
                            Suggestions for future research or tasks.
    Conclusion
                Summarizing the findings and implications.⏎
"""

"""
tests features of ``PromptTemplate`` using a example full prompt
"""

from kaye.gen_prompt import PromptTemplate, FullPromptParserNode

FULL_PROMPT = """
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


example_tree = FullPromptParserNode.parse(FULL_PROMPT)


class TestRepr:

    def test_dft(_):
        pt = PromptTemplate(example_tree)
        opt = repr(pt)
        print(opt)
        assert opt == """[x]○
[ ]└── Project Title
[ ]    ├── Description
       │   A brief overview of the project, its purpose, and goals.
[ ]    ├── Installation
       │   1. Clone the repo
       │   2. Install dependencies
       │   3. Run the application
[ ]    ├── Usage
       │   Provide instructions on how to use the application.
[ ]    ├── Contributing
       │   1. Fork the repo
       │   2. Create a new branch
       │   3. Submit a pull request
[ ]    └── License
           This project is licensed under the MIT License."""

    def test_no_content(_):
        pt = PromptTemplate(example_tree)
        opt = pt.__repr__(preview_line_count=0)
        print(opt)
        assert opt == """[x]○
[ ]└── Project Title
[ ]    ├── Description
[ ]    ├── Installation
[ ]    ├── Usage
[ ]    ├── Contributing
[ ]    └── License"""

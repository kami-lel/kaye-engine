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
        pt = PromptTemplate(full_prompt_tree=example_tree)
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
        pt = PromptTemplate(full_prompt_tree=example_tree)
        opt = pt.__repr__(preview_line_count=0)
        print(opt)
        assert opt == """[x]○
[ ]└── Project Title
[ ]    ├── Description
[ ]    ├── Installation
[ ]    ├── Usage
[ ]    ├── Contributing
[ ]    └── License"""


class TestDetachedMode:  # test detached mdoe

    def test_init_set(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names

    def test_init_unset(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_init_dft(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_set1(_):  # set by set_unset_detached_mode()
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_set2(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_unset1(_):  # unset by set_unset_detached_mode()
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_unset2(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_is_dm1(_):  # test is_detached_mode
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert pt.is_detached_mode

    def test_is_dm2(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert not pt.is_detached_mode


class TestParseSavable:  # TODO
    pass

"""
tests features of ``PromptBlueprint`` using a full PROMPT1
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt.prompt_blueprint.testees import PROMPT1

example_corpus = PromptCorpusNode.parse(PROMPT1)


class TestDetachedMode:  # test detached mdoe

    def test_init_set(_):
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names

    def test_init_unset(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_init_dft(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_set1(_):  # set by set_unset_detached_mode()
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_set2(_):
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_unset1(_):  # unset by set_unset_detached_mode()
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_unset2(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_is_dm1(_):  # test is_detached_mode
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert pt.is_detached_mode

    def test_is_dm2(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert not pt.is_detached_mode


class TestStr:

    def test1(_):
        blueprint_text = """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test2(_):
        blueprint_text = """    ○
[x] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Project Title
## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test3(_):
        blueprint_text = """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Project Title
## Installation
1. Clone the repo
2. Install dependencies
3. Run the application
## Usage
Provide instructions on how to use the application."""

    def test4(_):
        blueprint_text = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

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


class TestStrDetach:  # test detached mode

    def test1(_):
        blueprint_text = """[ ] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test2(_):
        blueprint_text = """[ ] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test2_no_ver(_):
        blueprint_text = """[ ] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test3(_):
        blueprint_text = """[ ] ○
[ ] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """## Installation
1. Clone the repo
2. Install dependencies
3. Run the application
## Usage
Provide instructions on how to use the application."""

    def test4(_):
        blueprint_text = """[ ] ○
[ ] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """## Description
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

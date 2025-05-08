"""
tests features of ``PromptBlueprint`` using a example full prompt
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt.pb.pb_testee_corpus import PROMPT1

example_corpus = PromptCorpusNode.parse(PROMPT1)


class TestRepr:

    def test_dft(_):
        pt = PromptBlueprint(example_corpus)
        opt = repr(pt)
        print(opt)
        assert opt == """[x] ○
[ ] └── Project Title
[ ]     ├── Description
        │   A brief overview of the project, its purpose, and goals.
[ ]     ├── Installation
        │   1. Clone the repo
        │   2. Install dependencies
        │   3. Run the application
[ ]     ├── Usage
        │   Provide instructions on how to use the application.
[ ]     ├── Contributing
        │   1. Fork the repo
        │   2. Create a new branch
        │   3. Submit a pull request
[ ]     └── License
            This project is licensed under the MIT License."""

    def test_no_content(_):
        pt = PromptBlueprint(example_corpus)
        opt = pt.__repr__(preview_line_count=0)
        print(opt)
        assert opt == """[x] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""


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


class TestParseSavable:

    def test1(_):
        blueprint_text = """[x] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        assert len(pt.enabled_nodes_names) == 1
        assert "○" in pt.enabled_nodes_names
        assert "Project Title" not in pt.enabled_nodes_names
        assert "Description" not in pt.enabled_nodes_names
        assert "Installation" not in pt.enabled_nodes_names
        assert "Usage" not in pt.enabled_nodes_names
        assert "Contributing" not in pt.enabled_nodes_names
        assert "License" not in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test2(_):
        blueprint_text = """[x] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        assert len(pt.enabled_nodes_names) == 2
        assert "○" in pt.enabled_nodes_names
        assert "Project Title" not in pt.enabled_nodes_names
        assert "Description" not in pt.enabled_nodes_names
        assert "Installation" not in pt.enabled_nodes_names
        assert "Usage" not in pt.enabled_nodes_names
        assert "Contributing" in pt.enabled_nodes_names
        assert "License" not in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test3(_):
        blueprint_text = """[x] ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        assert len(pt.enabled_nodes_names) == 4
        assert "○" in pt.enabled_nodes_names
        assert "Project Title" in pt.enabled_nodes_names
        assert "Description" not in pt.enabled_nodes_names
        assert "Installation" in pt.enabled_nodes_names
        assert "Usage" not in pt.enabled_nodes_names
        assert "Contributing" in pt.enabled_nodes_names
        assert "License" not in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test4(_):
        blueprint_text = """[x] ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        assert len(pt.enabled_nodes_names) == 7
        assert "○" in pt.enabled_nodes_names
        assert "Project Title" in pt.enabled_nodes_names
        assert "Description" in pt.enabled_nodes_names
        assert "Installation" in pt.enabled_nodes_names
        assert "Usage" in pt.enabled_nodes_names
        assert "Contributing" in pt.enabled_nodes_names
        assert "License" in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test_detached_mode(_):
        blueprint_text = """[ ] ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        assert len(pt.enabled_nodes_names) == 3
        assert "○" not in pt.enabled_nodes_names
        assert "Project Title" in pt.enabled_nodes_names
        assert "Description" not in pt.enabled_nodes_names
        assert "Installation" in pt.enabled_nodes_names
        assert "Usage" not in pt.enabled_nodes_names
        assert "Contributing" in pt.enabled_nodes_names
        assert "License" not in pt.enabled_nodes_names

        assert pt.is_detached_mode


class TestStr:

    def test1(_):
        blueprint_text = """[x] ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = str(pt)
        print(opt)
        assert opt == ""

    def test2(_):
        blueprint_text = """[x] ○
[x] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = str(pt)
        print(opt)
        assert opt == """# Project Title
## Contributing
1. Fork the repo
2. Create a new branch
3. Submit a pull request"""

    def test3(_):
        blueprint_text = """[x] ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = str(pt)
        print(opt)
        assert opt == """# Project Title
## Installation
1. Clone the repo
2. Install dependencies
3. Run the application
## Usage
Provide instructions on how to use the application."""

    def test4(_):
        blueprint_text = """[x] ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = str(pt)
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

        opt = str(pt)
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

        opt = str(pt)
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

        opt = str(pt)
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

        opt = str(pt)
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


class TestCFPB:  # test classmethod create_full_prompt_blueprint()
    def test1(_):
        pass

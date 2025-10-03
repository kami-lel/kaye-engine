"""
test __init__(), ie text parsing, when the tree is partial
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt.prompt_blueprint.testees import PROMPT1, PROMPT2


class Test1:  # use PROMPT1

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test1(self):
        blueprint_text = """    ○
[ ] └── Project Title
[ ]     └── License"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        assert len(pt.enabled) == 0

        assert ("Project Title",) not in enabled_names_path
        assert ("Project Title", "Description") not in enabled_names_path
        assert ("Project Title", "Installation") not in enabled_names_path
        assert ("Project Title", "Usage") not in enabled_names_path
        assert ("Project Title", "Contributing") not in enabled_names_path
        assert ("Project Title", "License") not in enabled_names_path

    def test2(self):
        blueprint_text = """    ○
[ ] └── Project Title
[x]     └── Contributing"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        assert len(pt.enabled) == 1
        assert ("Project Title",) not in enabled_names_path
        assert ("Project Title", "Description") not in enabled_names_path
        assert ("Project Title", "Installation") not in enabled_names_path
        assert ("Project Title", "Usage") not in enabled_names_path
        assert ("Project Title", "Contributing") in enabled_names_path
        assert ("Project Title", "License") not in enabled_names_path

    def test3(self):
        blueprint_text = """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     ├── Contributing
[ ]     └── License"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        assert len(pt.enabled) == 3
        assert ("Project Title",) in enabled_names_path
        assert ("Project Title", "Description") not in enabled_names_path
        assert ("Project Title", "Installation") in enabled_names_path
        assert ("Project Title", "Usage") not in enabled_names_path
        assert ("Project Title", "Contributing") in enabled_names_path
        assert ("Project Title", "License") not in enabled_names_path


class Test2:  # use PROMPT2

    corpus = PromptCorpusNode.parse(PROMPT2)

    def test_empty(self):
        blueprint_text = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     └── Conclusion"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        assert len(pt.enabled) == 0
        assert ("Main Title",) not in enabled_names_path
        assert ("Main Title", "Introduction") not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        ) not in enabled_names_path
        assert ("Main Title", "Methods") not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        ) not in enabled_names_path
        assert ("Main Title", "Conclusion") not in enabled_names_path

    def test1(self):
        blueprint_text = """    ○
[x] └── Main Title
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        assert len(pt.enabled) == 3
        assert ("Main Title",) in enabled_names_path
        assert ("Main Title", "Introduction") not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        ) not in enabled_names_path
        assert ("Main Title", "Methods") not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        ) in enabled_names_path
        assert ("Main Title", "Conclusion") in enabled_names_path

    def test2(self):
        blueprint_text = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[ ]     └── Conclusion"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        assert len(pt.enabled) == 4
        assert ("Main Title",) not in enabled_names_path
        assert ("Main Title", "Introduction") not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
        ) in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        ) not in enabled_names_path
        assert ("Main Title", "Methods") in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
        ) in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        ) in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        ) not in enabled_names_path
        assert ("Main Title", "Conclusion") not in enabled_names_path

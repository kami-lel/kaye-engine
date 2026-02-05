"""
prompt_node_lineage_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.generate_id_lineage()
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.prompt import (
    PROMPT1,
    PROMPT3,
)


class TestPrompt1:  ############################################################

    tree = PromptCorpusNode.parse(PROMPT1)

    def test_root(self):
        node = self.tree

        lineage = node.generate_id_lineage()

        print(lineage)
        assert isinstance(lineage, list)
        assert lineage == []

    def test_project(self):
        project = self.tree.children[0]

        lineage = project.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title"]

    def test_sub1(self):
        project = self.tree.children[0]
        sub = project.children[0]

        lineage = sub.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title", "Description"]

    def test_sub2(self):
        project = self.tree.children[0]
        sub = project.children[1]

        lineage = sub.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title", "Installation"]

    def test_sub3(self):
        project = self.tree.children[0]
        sub = project.children[2]

        lineage = sub.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title", "License"]


class TestPrompt3:  ############################################################

    tree = PromptCorpusNode.parse(PROMPT3)

    def test_intro(self):
        project = self.tree.children[0]
        node = project.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Introduction"]

    def test_intro_bg(self):
        project = self.tree.children[0]
        parent = project.children[0]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Introduction", "Background"]

    def test_intro_bg_mpt(self):
        project = self.tree.children[0]
        parent = project.children[0].children[0]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == [
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        ]

    def test_intro_bg_mpt_obj(self):
        project = self.tree.children[0]
        parent = project.children[0].children[0].children[0]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == [
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        ]

    def test_met(self):
        project = self.tree.children[0]
        node = project.children[1]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Methods"]

    def test_met_dc(self):
        project = self.tree.children[0]
        parent = project.children[1]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == [
            "Main Title",
            "Methods",
            "Data Collection",
        ]

    def test_met_dc_tu(self):
        project = self.tree.children[0]
        parent = project.children[1].children[0]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == [
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        ]

    def test_met_dc_tu_fw(self):
        project = self.tree.children[0]
        parent = project.children[1].children[0].children[0]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == [
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        ]

    def test_concl(self):
        project = self.tree.children[0]
        node = project.children[2]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Conclusion"]

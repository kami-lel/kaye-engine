"""
prompt_node_lineage_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.generate_id_lineage()
"""


class TestPrompt1:  ############################################################

    def test_root(_, corpus_testee1):
        node = corpus_testee1

        lineage = node.generate_id_lineage()

        print(lineage)
        assert isinstance(lineage, list)
        assert lineage == []

    def test_project(_, corpus_testee1):
        project = corpus_testee1.children[0]

        lineage = project.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title"]

    def test_sub1(_, corpus_testee1):
        project = corpus_testee1.children[0]
        sub = project.children[0]

        lineage = sub.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title", "Description"]

    def test_sub2(_, corpus_testee1):
        project = corpus_testee1.children[0]
        sub = project.children[1]

        lineage = sub.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title", "Installation"]

    def test_sub3(_, corpus_testee1):
        project = corpus_testee1.children[0]
        sub = project.children[2]

        lineage = sub.generate_id_lineage()

        print(lineage)
        assert lineage == ["Project Title", "License"]


class TestPrompt3:  ############################################################

    def test_intro(_, corpus_testee3):
        project = corpus_testee3.children[0]
        node = project.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Introduction"]

    def test_intro_bg(_, corpus_testee3):
        project = corpus_testee3.children[0]
        parent = project.children[0]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Introduction", "Background"]

    def test_intro_bg_mpt(_, corpus_testee3):
        project = corpus_testee3.children[0]
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

    def test_intro_bg_mpt_obj(_, corpus_testee3):
        project = corpus_testee3.children[0]
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

    def test_met(_, corpus_testee3):
        project = corpus_testee3.children[0]
        node = project.children[1]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Methods"]

    def test_met_dc(_, corpus_testee3):
        project = corpus_testee3.children[0]
        parent = project.children[1]
        node = parent.children[0]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == [
            "Main Title",
            "Methods",
            "Data Collection",
        ]

    def test_met_dc_tu(_, corpus_testee3):
        project = corpus_testee3.children[0]
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

    def test_met_dc_tu_fw(_, corpus_testee3):
        project = corpus_testee3.children[0]
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

    def test_concl(_, corpus_testee3):
        project = corpus_testee3.children[0]
        node = project.children[2]

        lineage = node.generate_id_lineage()

        print(lineage)
        assert lineage == ["Main Title", "Conclusion"]

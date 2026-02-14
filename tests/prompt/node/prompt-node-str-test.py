"""
prompt_node_str_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.__str__()
"""


class TestPrompt1:  ############################################################

    def test_root(_, corpus_testee1):
        node = corpus_testee1

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(_, corpus_testee1):
        node = corpus_testee1.children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title)"

    def test2(_, corpus_testee1):
        node = corpus_testee1.children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Description)"


class TestPrompt2:  ############################################################

    def test_root(_, corpus_testee2):
        node = corpus_testee2

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(_, corpus_testee2):
        node = corpus_testee2.children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title)"

    def test2(_, corpus_testee2):
        node = corpus_testee2.children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Description)"

    def test3(_, corpus_testee2):
        node = corpus_testee2.children[0].children[1]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Installation)"

    def test4(_, corpus_testee2):
        node = corpus_testee2.children[0].children[2]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Usage)"

    def test5(_, corpus_testee2):
        node = corpus_testee2.children[0].children[3]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Contributing)"

    def test6(_, corpus_testee2):
        node = corpus_testee2.children[0].children[4]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#License)"


class TestPrompt3:  ############################################################

    def test_root(_, corpus_testee3):
        node = corpus_testee3

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(_, corpus_testee3):
        node = corpus_testee3.children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title)"

    def test2(_, corpus_testee3):
        node = corpus_testee3.children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Introduction)"

    def test3(_, corpus_testee3):
        node = corpus_testee3.children[0].children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Introduction#Background)"

    def test4(_, corpus_testee3):
        node = corpus_testee3.children[0].children[0].children[0].children[0]

        opt = str(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode(Main Title#Introduction#Background#Importance)"
        )

    def test5(_, corpus_testee3):
        node = (
            corpus_testee3.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )

        opt = str(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode"
            "(Main Title#Introduction#Background#Importance#Objective)"
        )

    def test21(_, corpus_testee3):
        node = corpus_testee3.children[0].children[1]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Methods)"

    def test22(_, corpus_testee3):
        node = corpus_testee3.children[0].children[1].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Methods#Data Collection)"

    def test23(_, corpus_testee3):
        node = corpus_testee3.children[0].children[1].children[0].children[0]

        opt = str(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode(Main Title#Methods#Data Collection#Tools Used)"
        )

    def test24(_, corpus_testee3):
        node = (
            corpus_testee3.children[0]
            .children[1]
            .children[0]
            .children[0]
            .children[0]
        )

        opt = str(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode"
            "(Main Title#Methods#Data Collection#Tools Used#Future Work)"
        )

    def test31(_, corpus_testee3):
        node = corpus_testee3.children[0].children[2]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Conclusion)"

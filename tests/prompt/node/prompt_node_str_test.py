"""
prompt_node_str_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.__str__()
"""


class TestPrompt1:  ############################################################

    def test_root(_, test_prompt_corpus_tree1):
        node = test_prompt_corpus_tree1

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(_, test_prompt_corpus_tree1):
        node = test_prompt_corpus_tree1.children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title)"

    def test2(_, test_prompt_corpus_tree1):
        node = test_prompt_corpus_tree1.children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Description)"


class TestPrompt2:  ############################################################

    def test_root(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2.children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title)"

    def test2(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2.children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Description)"

    def test3(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2.children[0].children[1]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Installation)"

    def test4(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2.children[0].children[2]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Usage)"

    def test5(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2.children[0].children[3]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#Contributing)"

    def test6(_, test_prompt_corpus_tree2):
        node = test_prompt_corpus_tree2.children[0].children[4]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Project Title#License)"


class TestPrompt3:  ############################################################

    def test_root(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode()"

    def test1(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3.children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title)"

    def test2(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3.children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Introduction)"

    def test3(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3.children[0].children[0].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Introduction#Background)"

    def test4(_, test_prompt_corpus_tree3):
        node = (
            test_prompt_corpus_tree3.children[0]
            .children[0]
            .children[0]
            .children[0]
        )

        opt = str(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode(Main Title#Introduction#Background#Importance)"
        )

    def test5(_, test_prompt_corpus_tree3):
        node = (
            test_prompt_corpus_tree3.children[0]
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

    def test21(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3.children[0].children[1]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Methods)"

    def test22(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3.children[0].children[1].children[0]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Methods#Data Collection)"

    def test23(_, test_prompt_corpus_tree3):
        node = (
            test_prompt_corpus_tree3.children[0]
            .children[1]
            .children[0]
            .children[0]
        )

        opt = str(node)
        print(opt)

        assert (
            opt
            == "PromptCorpusNode(Main Title#Methods#Data Collection#Tools Used)"
        )

    def test24(_, test_prompt_corpus_tree3):
        node = (
            test_prompt_corpus_tree3.children[0]
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

    def test31(_, test_prompt_corpus_tree3):
        node = test_prompt_corpus_tree3.children[0].children[2]

        opt = str(node)
        print(opt)

        assert opt == "PromptCorpusNode(Main Title#Conclusion)"

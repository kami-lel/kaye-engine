"""
prompt_node_getitem_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.__getitem__()
"""

import pytest


class TestRoot:

    def test_parent(_, test_corpus3):
        node = test_corpus3

        with pytest.raises(TypeError) as exec_info:
            node[None]

        opt = exec_info.value.args[0]
        assert opt == f"{type(node).__name__} index must be int/str: None"

    def test_int1(_, test_corpus3):
        node = test_corpus3
        opt = node[0]

        print(opt)

        assert opt is test_corpus3.children[0]

    def test_str1(_, test_corpus3):
        node = test_corpus3
        opt = node["Main Title"]

        print(opt)

        assert opt is test_corpus3.children[0]

    def test_bad_int1(_, test_corpus3):
        node = test_corpus3
        with pytest.raises(IndexError) as exec_info:
            node[99]

        opt = exec_info.value.args[0]
        expected = f"index out of range for {str(node)}: 99"
        assert opt == expected

    def test_bad_str1(_, test_corpus3):
        node = test_corpus3
        with pytest.raises(KeyError) as exec_info:
            node["???"]

        opt = exec_info.value.args[0]
        expected = f"{str(node)} contains no child with name/id of '???'"
        assert opt == expected

    def test_bad_type(_, test_corpus3):
        node = test_corpus3
        with pytest.raises(TypeError) as exec_info:
            node[12.5]

        opt = exec_info.value.args[0]
        expected = f"{type(node).__name__} index must be int/str: 12.5"
        assert opt == expected


class TestMain:

    def test_parent(_, test_corpus3):
        node = test_corpus3.children[0]
        with pytest.raises(TypeError) as exec_info:
            node[None]

        opt = exec_info.value.args[0]
        assert opt == f"{type(node).__name__} index must be int/str: None"

    def test_int1(_, test_corpus3):
        node = test_corpus3.children[0]
        opt = node[0]

        print(opt)

        assert opt is test_corpus3.children[0].children[0]

    def test_int2(_, test_corpus3):
        node = test_corpus3.children[0]
        opt = node[1]

        print(opt)

        assert opt is test_corpus3.children[0].children[1]

    def test_int3(_, test_corpus3):
        node = test_corpus3.children[0]
        opt = node[2]

        print(opt)

        assert opt is test_corpus3.children[0].children[2]

    def test_str1(_, test_corpus3):
        node = test_corpus3.children[0]
        opt = node["Introduction"]

        print(opt)

        assert opt is test_corpus3.children[0].children[0]

    def test_str2(_, test_corpus3):
        node = test_corpus3.children[0]
        opt = node["Methods"]

        print(opt)

        assert opt is test_corpus3.children[0].children[1]

    def test_str3(_, test_corpus3):
        node = test_corpus3.children[0]
        opt = node["Conclusion"]

        print(opt)

        assert opt is test_corpus3.children[0].children[2]

    def test_bad_int1(_, test_corpus3):
        node = test_corpus3.children[0]
        with pytest.raises(IndexError) as exec_info:
            node[99]

        opt = exec_info.value.args[0]
        expected = f"index out of range for {str(node)}: 99"
        assert opt == expected

    def test_bad_str1(_, test_corpus3):
        node = test_corpus3.children[0]
        with pytest.raises(KeyError) as exec_info:
            node["???"]

        opt = exec_info.value.args[0]
        expected = f"{str(node)} contains no child with name/id of '???'"
        assert opt == expected

    def test_bad_type(_, test_corpus3):
        node = test_corpus3.children[0]
        with pytest.raises(TypeError) as exec_info:
            node[12.5]

        opt = exec_info.value.args[0]
        expected = f"{type(node).__name__} index must be int/str: 12.5"
        assert opt == expected


class TestImportance:

    def test_parent(_, test_corpus3):
        node = test_corpus3.children[0].children[0].children[0].children[0]

        with pytest.raises(TypeError) as exec_info:
            node[None]

        opt = exec_info.value.args[0]
        assert opt == f"{type(node).__name__} index must be int/str: None"

    def test_int1(_, test_corpus3):
        node = test_corpus3.children[0].children[0].children[0].children[0]

        opt = node[0]

        print(opt)

        assert (
            opt
            is test_corpus3.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )

    def test_str1(_, test_corpus3):
        node = test_corpus3.children[0].children[0].children[0].children[0]

        opt = node["Objective"]

        print(opt)

        assert (
            opt
            is test_corpus3.children[0]
            .children[0]
            .children[0]
            .children[0]
            .children[0]
        )

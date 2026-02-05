"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

BasePromptNode.__getitem__()
"""

import pytest

from tests.prompt.base import *


class TestByInt:  ##############################################################
    pass  # TODO


class TestByStr:  ##############################################################
    pass  # TODO


# bad type  ####################################################################


class TestBadType:

    def test1(_):
        key = []
        node = WORLD

        with pytest.raises(TypeError) as exec_info:
            node[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "UnitTestNode index must be int/str: []"

    def test2(_):
        key = {"a": 5}
        node = FOREST

        with pytest.raises(TypeError) as exec_info:
            node[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "UnitTestNode index must be int/str: {'a': 5}"

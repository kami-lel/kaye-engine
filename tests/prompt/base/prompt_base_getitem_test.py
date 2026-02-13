"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

BasePromptNode.__getitem__()
"""

import pytest

from tests.prompt.base import *


class TestByInt:  ##############################################################

    def test_world0(_):
        src = world_testee
        key = 0

        opt = src[key]

        print(opt)
        assert opt is mountain_testee

    def test_world1(_):
        src = world_testee
        key = 1

        opt = src[key]

        print(opt)
        assert opt is forest_testee

    def test_world2(_):
        src = world_testee
        key = 2

        opt = src[key]

        print(opt)
        assert opt is village_testee

    def test_mountain0(_):
        src = mountain_testee
        key = 0

        opt = src[key]

        print(opt)
        assert opt is peak_testee

    def test_mountain1(_):
        src = mountain_testee
        key = 1

        opt = src[key]

        print(opt)
        assert opt is lake_testee

    def test_peak0(_):
        src = peak_testee
        key = 0

        opt = src[key]

        print(opt)
        assert opt is cave_testee

    def test_forest0(_):
        src = forest_testee
        key = 0

        opt = src[key]

        print(opt)
        assert opt is glade_testee

    def test_forest1(_):
        src = forest_testee
        key = 1

        opt = src[key]

        print(opt)
        assert opt is stream_testee

    def test_village0(_):
        src = village_testee
        key = 0

        opt = src[key]

        print(opt)
        assert opt is market_testee

    # fail cases  --------------------------------------------------------------

    def test_leaf1(_):
        src = cave_testee
        key = 0

        with pytest.raises(IndexError) as exec_info:
            src[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "index out of range for "
            "UnitTestNode(Mountain Range#High Peak!#Dark Cave): "
            "0"
        )

    def test_leaf2(_):
        src = market_testee
        key = 0

        with pytest.raises(IndexError) as exec_info:
            src[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "index out of range for "
            "UnitTestNode(Old Village#Market Square): "
            "0"
        )

    def test_oor1(_):
        src = world_testee
        key = 100

        with pytest.raises(Exception) as exec_info:
            src[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "index out of range for UnitTestNode(): 100"


class TestByName:  #############################################################

    def test1(_):
        src = world_testee
        key = "Mountain Range"

        opt = src[key]

        print(opt)
        assert opt is mountain_testee

    def test2(_):
        src = mountain_testee
        key = "High Peak!"

        opt = src[key]

        print(opt)
        assert opt is peak_testee

    def test3(_):
        src = peak_testee
        key = "Dark Cave"

        opt = src[key]

        print(opt)
        assert opt is cave_testee

    # fail cases  --------------------------------------------------------------

    def test_no_found1(_):
        src = mountain_testee
        key = "aaa"

        with pytest.raises(KeyError) as exec_info:
            src[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "UnitTestNode(Mountain Range) "
            "contains no child with name/id of 'aaa'"
        )


class TestById:  ###############################################################

    def test1(_):
        src = world_testee
        key = "mountain_testee RANGE"

        opt = src[key]

        print(opt)
        assert opt is mountain_testee

    def test2(_):
        src = mountain_testee
        key = "HIGH peak_testee!"

        opt = src[key]

        print(opt)
        assert opt is peak_testee

    def test3(_):
        src = peak_testee
        key = "DARK cave_testee"

        opt = src[key]

        print(opt)
        assert opt is cave_testee


# bad type  ####################################################################
class TestBadType:

    def test1(_):
        key = []
        node = world_testee

        with pytest.raises(TypeError) as exec_info:
            node[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "UnitTestNode index must be int/str: []"

    def test2(_):
        key = {"a": 5}
        node = forest_testee

        with pytest.raises(TypeError) as exec_info:
            node[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "UnitTestNode index must be int/str: {'a': 5}"

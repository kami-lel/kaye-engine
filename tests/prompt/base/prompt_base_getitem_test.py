"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

BasePromptNode.__getitem__()
"""

import pytest

from tests.prompt.base import *


class TestByInt:  ##############################################################

    def test_world0(_):
        src = WORLD
        key = 0

        opt = src[key]

        print(opt)
        assert opt is MOUNTAIN

    def test_world1(_):
        src = WORLD
        key = 1

        opt = src[key]

        print(opt)
        assert opt is FOREST

    def test_world2(_):
        src = WORLD
        key = 2

        opt = src[key]

        print(opt)
        assert opt is VILLAGE

    def test_mountain0(_):
        src = MOUNTAIN
        key = 0

        opt = src[key]

        print(opt)
        assert opt is PEAK

    def test_mountain1(_):
        src = MOUNTAIN
        key = 1

        opt = src[key]

        print(opt)
        assert opt is LAKE

    def test_peak0(_):
        src = PEAK
        key = 0

        opt = src[key]

        print(opt)
        assert opt is CAVE

    def test_forest0(_):
        src = FOREST
        key = 0

        opt = src[key]

        print(opt)
        assert opt is GLADE

    def test_forest1(_):
        src = FOREST
        key = 1

        opt = src[key]

        print(opt)
        assert opt is STREAM

    def test_village0(_):
        src = VILLAGE
        key = 0

        opt = src[key]

        print(opt)
        assert opt is MARKET

    # fail cases  --------------------------------------------------------------

    def test_leaf1(_):
        src = CAVE
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
        src = MARKET
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
        src = WORLD
        key = 100

        with pytest.raises(Exception) as exec_info:
            src[key]
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "index out of range for UnitTestNode(): 100"


class TestByName:  #############################################################

    def test1(_):
        src = WORLD
        key = "Mountain Range"

        opt = src[key]

        print(opt)
        assert opt is MOUNTAIN

    def test2(_):
        src = MOUNTAIN
        key = "High Peak!"

        opt = src[key]

        print(opt)
        assert opt is PEAK

    def test3(_):
        src = PEAK
        key = "Dark Cave"

        opt = src[key]

        print(opt)
        assert opt is CAVE

    # fail cases  --------------------------------------------------------------

    def test_no_found1(_):
        src = MOUNTAIN
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
        src = WORLD
        key = "MOUNTAIN RANGE"

        opt = src[key]

        print(opt)
        assert opt is MOUNTAIN

    def test2(_):
        src = MOUNTAIN
        key = "HIGH PEAK!"

        opt = src[key]

        print(opt)
        assert opt is PEAK

    def test3(_):
        src = PEAK
        key = "DARK CAVE"

        opt = src[key]

        print(opt)
        assert opt is CAVE


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

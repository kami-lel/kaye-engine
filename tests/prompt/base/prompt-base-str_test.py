"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

BasePromptNode.__str__()
"""

from tests.prompt.base import *


class TestStr:

    def test_root(_, world_testee):
        node = world_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode()"

    def test_mountain(_, mountain_testee):
        node = mountain_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range)"

    def test_peak(_, peak_testee):
        node = peak_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range#High Peak!)"

    def test_cave(_, cave_testee):
        node = cave_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range#High Peak!#Dark Cave)"

    def test_lake(_, lake_testee):
        node = lake_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range#Serene Lake)"

    def test_forest(_, forest_testee):
        node = forest_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest)"

    def test_glade(_, glade_testee):
        node = glade_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest#Sunny Glade)"

    def test_stream(_, stream_testee):
        node = stream_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest#Hidden Stream)"

    def test_village(_, village_testee):
        node = village_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Old Village)"

    def test_market(_, market_testee):
        node = market_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Old Village#Market Square)"

"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

BasePromptNode.__str__()
"""

from tests.prompt.base import *


class TestStr:

    def test_root(self):
        node = world_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode()"

    def test_mountain(self):
        node = mountain_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range)"

    def test_peak(self):
        node = peak_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range#High Peak!)"

    def test_cave(self):
        node = cave_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range#High Peak!#Dark Cave)"

    def test_lake(self):
        node = lake_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range#Serene Lake)"

    def test_forest(self):
        node = forest_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest)"

    def test_glade(self):
        node = glade_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest#Sunny Glade)"

    def test_stream(self):
        node = stream_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest#Hidden Stream)"

    def test_village(self):
        node = village_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Old Village)"

    def test_market(self):
        node = market_testee
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Old Village#Market Square)"

"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

BasePromptNode.__str__()
"""

from tests.prompt.base import *


class TestStr:

    # BUG wrong

    def test_root(self):
        node = WORLD
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode()"

    def test_mountain(self):
        node = MOUNTAIN
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Mountain Range)"

    def test_peak(self):
        node = PEAK
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(High Peak!)"

    def test_cave(self):
        node = CAVE
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Dark Cave)"

    def test_lake(self):
        node = LAKE
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Serene Lake)"

    def test_forest(self):
        node = FOREST
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Ancient Forest)"

    def test_glade(self):
        node = GLADE
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Sunny Glade)"

    def test_stream(self):
        node = STREAM
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Hidden Stream)"

    def test_village(self):
        node = VILLAGE
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Old Village)"

    def test_market(self):
        node = MARKET
        opt = str(node)
        print(opt)
        assert opt == "UnitTestNode(Market Square)"

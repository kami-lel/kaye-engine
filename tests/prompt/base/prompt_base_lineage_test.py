"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

- BasePromptNode.generate_lineage()
"""

from tests.prompt.base import *


class TestGenLineage:

    def test_root(self):
        node = WORLD
        opt = node.generate_lineage()
        print(opt)
        assert opt == [""]

    def test_mountain(self):
        node = MOUNTAIN
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "MOUNTAIN"]

    def test_peak(self):
        node = PEAK
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "MOUNTAIN", "PEAK"]

    def test_cave(self):
        node = CAVE
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "MOUNTAIN", "PEAK", "CAVE"]

    def test_lake(self):
        node = LAKE
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "MOUNTAIN", "LAKE"]

    def test_forest(self):
        node = FOREST
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "FOREST"]

    def test_glade(self):
        node = GLADE
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "FOREST", "GLADE"]

    def test_stream(self):
        node = STREAM
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "FOREST", "STREAM"]

    def test_village(self):
        node = VILLAGE
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "VILLAGE"]

    def test_market(self):
        node = MARKET
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["", "VILLAGE", "MARKET"]

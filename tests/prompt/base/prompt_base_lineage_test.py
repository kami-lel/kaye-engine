"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

- BasePromptNode.generate_lineage()
"""

from tests.prompt.base import *


class TestGenLineage:

    def test_root(self):
        node = WORLD
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == []

    def test_mountain(self):
        node = MOUNTAIN
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE"]

    def test_peak(self):
        node = PEAK
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE", "HIGH PEAK!"]

    def test_cave(self):
        node = CAVE
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE", "HIGH PEAK!", "DARK CAVE"]

    def test_lake(self):
        node = LAKE
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE", "SERENE LAKE"]

    def test_forest(self):
        node = FOREST
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["ANCIENT FOREST"]

    def test_glade(self):
        node = GLADE
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["ANCIENT FOREST", "SUNNY GLADE"]

    def test_stream(self):
        node = STREAM
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["ANCIENT FOREST", "HIDDEN STREAM"]

    def test_village(self):
        node = VILLAGE
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["OLD VILLAGE"]

    def test_market(self):
        node = MARKET
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["OLD VILLAGE", "MARKET SQUARE"]

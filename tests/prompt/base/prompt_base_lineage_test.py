"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

- BasePromptNode.generate_lineage()
"""

from tests.prompt.base import *


class TestGenLineage:

    def test_root(self):
        node = world_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == []

    def test_mountain(self):
        node = mountain_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["mountain_testee RANGE"]

    def test_peak(self):
        node = peak_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["mountain_testee RANGE", "HIGH peak_testee!"]

    def test_cave(self):
        node = cave_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == [
            "mountain_testee RANGE",
            "HIGH peak_testee!",
            "DARK cave_testee",
        ]

    def test_lake(self):
        node = lake_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["mountain_testee RANGE", "SERENE lake_testee"]

    def test_forest(self):
        node = forest_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["ANCIENT forest_testee"]

    def test_glade(self):
        node = glade_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["ANCIENT forest_testee", "SUNNY glade_testee"]

    def test_stream(self):
        node = stream_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["ANCIENT forest_testee", "HIDDEN stream_testee"]

    def test_village(self):
        node = village_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["OLD village_testee"]

    def test_market(self):
        node = market_testee
        opt = node.generate_id_lineage()
        print(opt)
        assert opt == ["OLD village_testee", "market_testee SQUARE"]

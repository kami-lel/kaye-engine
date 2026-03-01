"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

- BasePromptNode.generate_lineage()
"""

from tests.prompt.base import *


class TestGenLineage:

    def test_root(_, world_testee):
        node = world_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == []

    def test_mountain(_, mountain_testee):
        node = mountain_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE"]

    def test_peak(_, peak_testee):
        node = peak_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE", "HIGH PEAK!"]

    def test_cave(_, cave_testee):
        node = cave_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == [
            "MOUNTAIN RANGE",
            "HIGH PEAK!",
            "DARK CAVE",
        ]

    def test_lake(_, lake_testee):
        node = lake_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["MOUNTAIN RANGE", "SERENE LAKE"]

    def test_forest(_, forest_testee):
        node = forest_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["ANCIENT FOREST"]

    def test_glade(_, glade_testee):
        node = glade_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["ANCIENT FOREST", "SUNNY GLADE"]

    def test_stream(_, stream_testee):
        node = stream_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["ANCIENT FOREST", "HIDDEN STREAM"]

    def test_village(_, village_testee):
        node = village_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["OLD VILLAGE"]

    def test_market(_, market_testee):
        node = market_testee
        opt = node.generate_identifier_lineage()
        print(opt)
        assert opt == ["OLD VILLAGE", "MARKET SQUARE"]

"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

- BasePromptNode.generate_lineage()
"""

from tests.prompt.base import *


class TestGenLineage:

    def test_root(_, world_testee):
        node = world_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == []

    def test_mountain(_, mountain_testee):
        node = mountain_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Mountain Range"]

    def test_peak(_, peak_testee):
        node = peak_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Mountain Range", "High Peak!"]

    def test_cave(_, cave_testee):
        node = cave_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == [
            "Mountain Range",
            "High Peak!",
            "Dark Cave",
        ]

    def test_lake(_, lake_testee):
        node = lake_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Mountain Range", "Serene Lake"]

    def test_forest(_, forest_testee):
        node = forest_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Ancient Forest"]

    def test_glade(_, glade_testee):
        node = glade_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Ancient Forest", "Sunny Glade"]

    def test_stream(_, stream_testee):
        node = stream_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Ancient Forest", "Hidden Stream"]

    def test_village(_, village_testee):
        node = village_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Old Village"]

    def test_market(_, market_testee):
        node = market_testee
        opt = node.generate_lineage()
        print(opt)
        assert opt == ["Old Village", "Market Square"]

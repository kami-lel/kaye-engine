"""
prompt_base_getitem_test.py

Unit Tests (using pytest) for:

- BasePromptNode.generate_prompt_tree_preview()
- BasePromptNode.__repr__()
"""

import pytest

from tests.prompt.base import *

DFT_OPT = """World
├── Mountain Range
│   A jagged spine of rock rising sharply from the plain.
│   Paths climb steeply and are often lost in fog.
│   Old gods were said to have carved these peaks.
│   ├── High Peak!
│   │   High Peak! stands above all, crowned with eternal snow.
│   │   Climbers leave tokens here: strips of cloth, small carve
│   │   and prayers written on thin paper that flutters like mot
│   │   └── Dark Cave
│   │       Dark Cave is a place of cool stones and quiet drip.
│   │       Stalactites like teeth hang from the ceiling.
│   │       Locals tell stories of an old miner who never return
│   └── Serene Lake
│       Serene Lake glassed the sky and mirrors the moon.
│       Its water is clear enough to read the reflection of a fa
│       Fishermen avoid one inlet where the current runs cold an
├── Ancient Forest
│   Ancient Forest: trees older than most kingdoms.
│   ├── Sunny Glade
│   │   Sunny Glade opens like a smile in the heart of the woods
│   │   Wildflowers bloom in impossible colors; bees hum like co
│   │   It is a favored spot for picnics and secret meetings ben
│   └── Hidden Stream
│       Hidden Stream runs clear and quick beneath ferns.
│       Children dam it with hands and laugh; maps rarely show i
│       At spring melt, it rushes bright and silver.
└── Old Village
    Old Village has stone cottages and crooked chimneys.
    Market days fill the square with color and the smell of spic
    People keep old grudges and older songs.
    └── Market Square
        Market Square: a clamor of cries, cloth, and coins.
        Stalls display everything from carved toys to rare spice
        At night the square empties and the lamps leave puddles """


# tree preview  ################################################################
class TestTreePreview:

    def test1(_, world_testee):
        node = world_testee

        opt = node.generate_prompt_tree_preview()

        print(opt)
        assert opt == DFT_OPT

    def test2(_, world_testee):
        node = world_testee

        opt = node.generate_prompt_tree_preview(content_preview_lines=0)

        print(opt)
        assert opt == """World
├── Mountain Range
│   ├── High Peak!
│   │   └── Dark Cave
│   └── Serene Lake
├── Ancient Forest
│   ├── Sunny Glade
│   └── Hidden Stream
└── Old Village
    └── Market Square"""

    def test3(_, world_testee):
        node = world_testee

        opt = node.generate_prompt_tree_preview(content_preview_width=30)

        print(opt)
        assert opt == """World
├── Mountain Range
│   A jagged spine of rock ris
│   Paths climb steeply and ar
│   Old gods were said to have
│   ├── High Peak!
│   │   High Peak! stands abov
│   │   Climbers leave tokens 
│   │   and prayers written on
│   │   └── Dark Cave
│   │       Dark Cave is a pla
│   │       Stalactites like t
│   │       Locals tell storie
│   └── Serene Lake
│       Serene Lake glassed th
│       Its water is clear eno
│       Fishermen avoid one in
├── Ancient Forest
│   Ancient Forest: trees olde
│   ├── Sunny Glade
│   │   Sunny Glade opens like
│   │   Wildflowers bloom in i
│   │   It is a favored spot f
│   └── Hidden Stream
│       Hidden Stream runs cle
│       Children dam it with h
│       At spring melt, it rus
└── Old Village
    Old Village has stone cott
    Market days fill the squar
    People keep old grudges an
    └── Market Square
        Market Square: a clamo
        Stalls display everyth
        At night the square em"""

    def test_non_root1(_, peak_testee):
        node = peak_testee

        with pytest.raises(NotImplementedError) as exec_info:
            node.generate_prompt_tree_preview()

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt == ".generate_prompt_tree_preview() is only possible for root"
        )


# repr  ########################################################################
class TestRepr:

    def test1(_, world_testee):
        node = world_testee

        opt = repr(node)

        print(opt)
        assert opt == DFT_OPT

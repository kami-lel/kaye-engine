from kaye.gen_prompt.base_prompt_node import BasePromptNode

__all__ = [
    "UnitTestNode",
    "WORLD",
    "MOUNTAIN",
    "PEAK",
    "CAVE",
    "LAKE",
    "FOREST",
    "GLADE",
    "STREAM",
    "VILLAGE",
    "MARKET",
]


class UnitTestNode(BasePromptNode):

    @property
    def id(self):
        return self.name.upper()

    @property
    def content_lines(self):
        return self.content_lines


WORLD = UnitTestNode("World")
MOUNTAIN = UnitTestNode("Mountain Range", parent=WORLD)
PEAK = UnitTestNode("High Peak!", parent=MOUNTAIN)
CAVE = UnitTestNode("Dark Cave", parent=PEAK)
LAKE = UnitTestNode("Serene Lake", parent=MOUNTAIN)
FOREST = UnitTestNode("Ancient Forest", parent=WORLD)
GLADE = UnitTestNode("Sunny Glade", parent=FOREST)
STREAM = UnitTestNode("Hidden Stream", parent=FOREST)
VILLAGE = UnitTestNode("Old Village", parent=WORLD)
MARKET = UnitTestNode("Market Square", parent=VILLAGE)

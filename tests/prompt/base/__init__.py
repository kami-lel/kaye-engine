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
    def name_in_lineage(self):
        return self.name.upper()

    @property
    def content_lines(self):
        return self.content_lines


# Node declarations outside class with ALL CAPS names
WORLD = UnitTestNode("WORLD")
MOUNTAIN = UnitTestNode("MOUNTAIN", parent=WORLD)
PEAK = UnitTestNode("PEAK", parent=MOUNTAIN)
CAVE = UnitTestNode("CAVE", parent=PEAK)
LAKE = UnitTestNode("LAKE", parent=MOUNTAIN)
FOREST = UnitTestNode("FOREST", parent=WORLD)
GLADE = UnitTestNode("GLADE", parent=FOREST)
STREAM = UnitTestNode("STREAM", parent=FOREST)
VILLAGE = UnitTestNode("VILLAGE", parent=WORLD)
MARKET = UnitTestNode("MARKET", parent=VILLAGE)

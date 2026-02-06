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

    def content_lines(self, query=""):
        return self.lines


WORLD = UnitTestNode("World", lines=[])

MOUNTAIN = UnitTestNode(
    "Mountain Range",
    parent=WORLD,
    lines=[
        "A jagged spine of rock rising sharply from the plain.",
        "Paths climb steeply and are often lost in fog.",
        "Old gods were said to have carved these peaks.",
        "The wind here carries the taste of iron and the echo of avalanches.",
    ],
)

PEAK = UnitTestNode(
    "High Peak!",
    parent=MOUNTAIN,
    lines=[
        "High Peak! stands above all, crowned with eternal snow.",
        "Climbers leave tokens here: strips of cloth, small carved stones,",
        (
            "and prayers written on thin paper that flutters "
            "like moth-wings across the ridge."
        ),
        (
            "From the summit one can see the curve of rivers and the faint"
            " smoke of distant villages;"
        ),
        "the air is thin and sharp.",
    ],
)

CAVE = UnitTestNode(
    "Dark Cave",
    parent=PEAK,
    lines=[
        "Dark Cave is a place of cool stones and quiet drip.",
        "Stalactites like teeth hang from the ceiling.",
        "Locals tell stories of an old miner who never returned;",
        "sometimes a lantern light is glimpsed deep inside.",
        (
            "Echoes travel in strange ways; footsteps may sound like two people"
            " when only one goes in."
        ),
    ],
)

LAKE = UnitTestNode(
    "Serene Lake",
    parent=MOUNTAIN,
    lines=[
        "Serene Lake glassed the sky and mirrors the moon.",
        (
            "Its water is clear enough to read the reflection of a face, "
            "and deep enough to hide secrets."
        ),
        (
            "Fishermen avoid one inlet where the current runs cold "
            "and almost feels alive —"
        ),
        "a shiver in the water that refuses to settle.",
    ],
)

FOREST = UnitTestNode(
    "Ancient Forest",
    parent=WORLD,
    lines=[
        "Ancient Forest: trees older than most kingdoms.",
    ],
)

GLADE = UnitTestNode(
    "Sunny Glade",
    parent=FOREST,
    lines=[
        "Sunny Glade opens like a smile in the heart of the woods.",
        (
            "Wildflowers bloom in impossible colors; "
            "bees hum like contented little engines."
        ),
        (
            "It is a favored spot for picnics "
            "and secret meetings beneath the warm sky."
        ),
    ],
)

STREAM = UnitTestNode(
    "Hidden Stream",
    parent=FOREST,
    lines=[
        "Hidden Stream runs clear and quick beneath ferns.",
        (
            "Children dam it with hands and laugh; "
            "maps rarely show its true course."
        ),
        "At spring melt, it rushes bright and silver.",
        (
            "Listen for a small bell hung on a branch; "
            "it means someone has come this way."
        ),
    ],
)

VILLAGE = UnitTestNode(
    "Old Village",
    parent=WORLD,
    lines=[
        "Old Village has stone cottages and crooked chimneys.",
        "Market days fill the square with color and the smell of spice.",
        "People keep old grudges and older songs.",
        "A bell tower chimes at dawn, though no one knows when it was built.",
    ],
)

MARKET = UnitTestNode(
    "Market Square",
    parent=VILLAGE,
    lines=[
        "Market Square: a clamor of cries, cloth, and coins.",
        (
            "Stalls display everything from carved toys to rare spices;"
            " bargaining is an art here."
        ),
        (
            "At night the square empties and the lamps leave puddles of light"
            " on the cobbles—footprints fade but stories linger."
        ),
    ],
)

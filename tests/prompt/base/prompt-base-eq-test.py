"""
prompt-base-eq-test.py

Unit Tests (using pytest) for:

- BasePromptNode.__eq__()
"""

import pytest


from tests.prompt.base import UnitTestNode


# fixtures  ####################################################################
@pytest.fixture
def compare_world_testee():
    world_testee = UnitTestNode("World", lines=[])

    mountain_testee = UnitTestNode(
        "Mountain Range",
        parent=world_testee,
        lines=[],
    )

    peak_testee = UnitTestNode(
        "High Peak!",
        parent=mountain_testee,
        lines=[],
    )

    UnitTestNode(
        "Dark Cave",
        parent=peak_testee,
        lines=[],
    )

    UnitTestNode(
        "Serene Lake",
        parent=mountain_testee,
        lines=[],
    )

    forest_testee = UnitTestNode(
        "Ancient Forest",
        parent=world_testee,
        lines=[],
    )

    UnitTestNode(
        "Sunny Glade",
        parent=forest_testee,
        lines=[],
    )

    UnitTestNode(
        "Hidden Stream",
        parent=forest_testee,
        lines=[],
    )

    village_testee = UnitTestNode(
        "Old Village",
        parent=world_testee,
        lines=[
            "Old Village has stone cottages and crooked chimneys.",
            "Market days fill the square with color and the smell of spice.",
            "People keep old grudges and older songs.",
            (
                "A bell tower chimes at dawn, though no one knows when it was"
                " built."
            ),
        ],
    )

    UnitTestNode(
        "Market Square",
        parent=village_testee,
        lines=[],
    )

    return world_testee


# test  ########################################################################


def test_eq(world_testee, compare_world_testee):
    world_testee == compare_world_testee

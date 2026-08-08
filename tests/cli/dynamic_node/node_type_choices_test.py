"""
tests/cli/dynamic_node/node_type_choices_test.py

Unit Tests (using pytest) for:

list_all_node_type_names
"""

from kaye_engine.abbr_collection import abbr_glossary_registry
from kaye_engine.cli.dynamic_node.node_type_choices import (
    list_all_node_type_names,
)
from kaye_engine.prompt.dynamic_nodes import ABBR_TAG_NODE_MEMBERS


# pytest  ######################################################################
class TestListAllNodeTypeNames:

    def test_ordering(_):
        opt = list_all_node_type_names()

        print(opt)

        expected_tag_names = [abbr_tag.name for abbr_tag in ABBR_TAG_NODE_MEMBERS]
        expected_glossary_names = sorted(abbr_glossary_registry)

        assert opt == (
            ["today", "shorthand"]
            + expected_tag_names
            + expected_glossary_names
        )

    def test_abbr_tag_block_excludes_composite_and_always_understand(_):
        opt = list_all_node_type_names()

        print(opt)
        assert "always_understand" not in opt
        assert "WORD_CHARACTER" not in opt
        assert "ASCII" not in opt

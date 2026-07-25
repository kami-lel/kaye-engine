"""
prompt-bp-parse-dynamics-test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye_engine.prompt.dynamic_nodes import (
    TodayNode,
    AbbrNode,
    PLCNode,
    UsableAbbrNode,
)


class TestDynamics:

    def test_today(_, dynamic_bp_testee2):
        bp = dynamic_bp_testee2
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["(Today)"]
        assert isinstance(node, TodayNode)
        assert node in bp
        assert bp.is_checkmarked(node)

    def test_abbr_node(_, dynamic_bp_testee3):
        bp = dynamic_bp_testee3
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["(Abbreviations)"]
        assert isinstance(node, AbbrNode)
        assert node in bp
        assert bp.is_checkmarked(node)

    def test_plc(_, dynamic_bp_testee4):
        bp = dynamic_bp_testee4
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["(Programming Languages Code)"]
        assert isinstance(node, PLCNode)
        assert node in bp
        assert bp.is_checkmarked(node)

    def test_usable_abbr(_, dynamic_bp_testee5):
        bp = dynamic_bp_testee5
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["(Usable Abbreviations)"]
        assert isinstance(node, UsableAbbrNode)
        assert node in bp
        assert bp.is_checkmarked(node)

    # use dynamic_bp_testee1  --------------------------------------------------

    def test_mux_abbr(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["(Abbreviations)"]

        assert isinstance(node, AbbrNode)

    def test_mux_plc(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["(Programming Languages Code)"]

        assert isinstance(node, PLCNode)

    def test_mux_today(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["(Today)"]

        assert isinstance(node, TodayNode)

    def test_mux_usable(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["(Usable Abbreviations)"]

        assert isinstance(node, UsableAbbrNode)

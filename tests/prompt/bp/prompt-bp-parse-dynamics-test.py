"""
prompt-bp-parse-dynamics-test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye.gen_prompt.today_node import TodayNode
from kaye.gen_prompt.abbr_nodes import AbbrNode, PLCNode


class TestDynamics:

    def test_today(_, dynamic_bp_testee2):
        bp = dynamic_bp_testee2
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["{Today}"]
        assert isinstance(node, TodayNode)
        assert node in bp
        assert bp.is_checkmarked(node)

    def test_abbr_node(_, dynamic_bp_testee3):
        bp = dynamic_bp_testee3
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["{Abbreviations}"]
        assert isinstance(node, AbbrNode)
        assert node in bp
        assert bp.is_checkmarked(node)

    def test_plc(_, dynamic_bp_testee4):
        bp = dynamic_bp_testee4
        print(bp.generate_blueprint(content_preview_lines=0))

        node = bp.corpus["{Programming Languages Code}"]
        assert isinstance(node, PLCNode)
        assert node in bp
        assert not bp.is_checkmarked(node)

    # use dynamic_bp_testee1  --------------------------------------------------

    def test_mux_abbr(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["Main Title"]["Introduction"][
            "Background"
        ]["Importance"]["Abbreviations"]

        assert isinstance(node, AbbrNode)

    def test_mux_plc(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Programming Languages Code"
        ]

        assert isinstance(node, PLCNode)

    def test_mux_today(_, dynamic_bp_testee1):
        print(dynamic_bp_testee1.generate_blueprint(content_preview_lines=0))

        node = dynamic_bp_testee1.corpus["Main Title"]["Methods"][
            "Data Collection"
        ]["Tools Used"]["Future Work"]["Today"]

        assert isinstance(node, TodayNode)

"""
prompt-bp-parse-dynamics-test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from kaye.gen_prompt.today_node import TodayNode
from kaye.gen_prompt.abbr_nodes import AbbrNode


class TestDynamics:

    def test_today1(_, corpus_testee3):
        bp_text = """ ○
[ ] └── {Today}"""

        bp = PromptBlueprint.parse(
            bp_text, corpus_override=corpus_testee3, disable_prune=True
        )

        node = bp.corpus["{Today}"]

        print(bp.generate_blueprint(content_preview_lines=0))

        assert node in bp.corpus
        assert node in bp
        assert not bp.is_checkmarked(node)

    def test_mux(_, dynamic_nodes_testee1):

        print(dynamic_nodes_testee1.generate_blueprint(content_preview_lines=0))

    def test1(_):
        # TODO
        pass

    def test_mux(_, dynamic_nodes_testee1):
        # TODO
        pass

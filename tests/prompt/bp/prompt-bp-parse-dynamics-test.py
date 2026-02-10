"""
prompt-bp-parse-dynamics-test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from kaye.gen_prompt.today_node import TodayNode
from kaye.gen_prompt.abbr_nodes import AbbrNode


class TestDynamics:

    def test1(_):
        bp_text = """ ○
[ ] └── {Abbreviations}"""

        bp = PromptBlueprint.parse(bp_text)

        abbr_node = bp.corpus["{Abbreviations}"]

        print(bp.generate_blueprint(content_preview_lines=0))

        assert abbr_node in bp
        assert not bp.is_checkmarked(abbr_node)


# TODO

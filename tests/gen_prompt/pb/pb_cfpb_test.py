"""
test classmethod ``create_full_prompt_blueprint("test", )`` of class ``PromptBlueprint``
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt.pb.pb_testee_corpus import PROMPT1, PROMPT2


class TestCFPB:

    def test1(_):  # using prompt1
        corpus = PromptCorpusNode.parse(PROMPT1)
        blueprint = PromptBlueprint.create_full_prompt_blueprint(corpus)

        opt = blueprint.__repr__(preview_line_count=0, hide_comment=True)
        print(opt)
        assert opt == """[x] ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     └── License"""

    def test2(_):  # using prompt2
        corpus = PromptCorpusNode.parse(PROMPT2)
        blueprint = PromptBlueprint.create_full_prompt_blueprint(corpus)

        opt = blueprint.__repr__(preview_line_count=0, hide_comment=True)
        print(opt)
        assert opt == """[x] ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

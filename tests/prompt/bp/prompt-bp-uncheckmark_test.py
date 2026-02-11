"""
prompt-bp-uncheckmark_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .uncheckmark()
- __isub__()
"""

import pytest

from kaye.gen_prompt import PromptBlueprint
from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
)


# test_prompt1  ################################################################
class Test11:  # ===============================================================

    src = BLUEPRINT_1_FULL
    dest = BLUEPRINT_1_PARTIAL_1

    def test1_uncheckmark_by_obj(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee1["Project Title"]
        opt.uncheckmark(node)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test1_uncheckmark_by_hash(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee1["Project Title"]
        node_hash = hash(node)
        opt.uncheckmark(node_hash)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test1_isub_by_obj(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee1["Project Title"]
        opt -= node

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test1_isub_by_hash(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee1["Project Title"]
        node_hash = hash(node)
        opt -= node_hash

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    # err handling  ------------------------------------------------------------
    def test_bad_type(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        with pytest.raises(TypeError) as exec_info:
            opt.uncheckmark(12.5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must be BasePromptNode or hash value: 12.5"

    def test_bad_hash(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        with pytest.raises(KeyError) as exec_info:
            opt.uncheckmark(5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "node absent in this blueprint: 5"

    def test_bad_obj(self, corpus_testee1, corpus_testee3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )
        bad_node = corpus_testee3["Main Title"]

        with pytest.raises(KeyError) as exec_info:
            opt.uncheckmark(bad_node)

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt == "node absent in this blueprint: PromptCorpusNode(Main Title)"
        )


class Test12:  # ===============================================================

    src = BLUEPRINT_1_FULL
    dest = BLUEPRINT_1_PARTIAL_2

    def test2_uncheckmark_by_obj(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee1["Project Title"]["Description"]
        opt.uncheckmark(node)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test2_uncheckmark_by_hash(self, corpus_testee1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee1["Project Title"]["Description"]
        node_hash = hash(node)
        opt.uncheckmark(node_hash)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest


class Test2:  # test_prompt2  ##################################################

    src = BLUEPRINT_2_FULL
    dest = BLUEPRINT_2_PARTIAL_1

    def test1_uncheckmark_by_obj(self, corpus_testee2):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee2
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        proj_node = corpus_testee2["Project Title"]
        opt.uncheckmark(proj_node["Description"]).uncheckmark(
            proj_node["Usage"]
        ).uncheckmark(proj_node["License"])

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test1_uncheckmark_by_hash(self, corpus_testee2):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee2
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        proj_node = corpus_testee2["Project Title"]
        for h in [
            hash(proj_node[name])
            for name in ("Description", "Usage", "License")
        ]:
            opt.uncheckmark(h)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest


# test_prompt3  ################################################################
class Test31:  # ===============================================================

    src = BLUEPRINT_3_FULL
    dest = BLUEPRINT_3_PARTIAL_1

    def test1_uncheckmark_by_obj(self, corpus_testee3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee3["Main Title"]["Methods"]
        opt.uncheckmark(node)
        node = node["Data Collection"]
        opt.uncheckmark(node)
        node = node["Tools Used"]
        opt.uncheckmark(node)
        node = node["Future Work"]
        opt.uncheckmark(node)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test1_uncheckmark_by_hash(self, corpus_testee3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        node = corpus_testee3["Main Title"]["Methods"]
        opt.uncheckmark(hash(node))
        node = node["Data Collection"]
        opt.uncheckmark(hash(node))
        node = node["Tools Used"]
        opt.uncheckmark(hash(node))
        node = node["Future Work"]
        opt.uncheckmark(hash(node))

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest


class Test32:  # ===============================================================

    src = BLUEPRINT_3_FULL
    dest = BLUEPRINT_3_PARTIAL_2

    def test2_uncheckmark_by_obj(self, corpus_testee3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        main_node = corpus_testee3["Main Title"]
        node = main_node["Introduction"]
        opt.uncheckmark(node)
        node = node["Background"]["Importance"]
        opt.uncheckmark(node)
        node = main_node["Methods"]
        opt.uncheckmark(node)
        node = node["Data Collection"]["Tools Used"]
        opt.uncheckmark(node)
        node = main_node["Conclusion"]
        opt.uncheckmark(node)

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

    def test2_uncheckmark_by_hash(self, corpus_testee3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        print(
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
        )

        main_node = corpus_testee3["Main Title"]
        node = main_node["Introduction"]
        opt.uncheckmark(hash(node))
        node = node["Background"]["Importance"]
        opt.uncheckmark(hash(node))
        node = main_node["Methods"]
        opt.uncheckmark(hash(node))
        node = node["Data Collection"]["Tools Used"]
        opt.uncheckmark(hash(node))
        node = main_node["Conclusion"]
        opt.uncheckmark(hash(node))

        bp_text = opt.generate_blueprint(
            content_preview_lines=0, show_comment=False
        )
        print("#" * 80)
        print(bp_text)

        assert bp_text == self.dest

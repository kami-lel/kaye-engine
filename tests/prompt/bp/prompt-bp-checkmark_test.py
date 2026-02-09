"""
prompt-bp-checkmark_test.py

Unit Tests (using pytest) for: PromptBlueprint:

- .checkmark()
- .__iadd__()
"""

# FIXME


import pytest

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
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

    src = BLUEPRINT_1_PARTIAL_1
    dest = BLUEPRINT_1_FULL

    def test1_checkmark_by_obj(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        print(opt)

        node = test_corpus1["Project Title"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test1_checkmark_by_hash(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        print(opt)

        node = test_corpus1["Project Title"]
        node_hash = hash(node)
        opt.checkmark(node_hash)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test1_iadd_by_obj(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        print(opt)

        node = test_corpus1["Project Title"]
        opt += node

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test1_iadd_by_hash(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        print(opt)

        node = test_corpus1["Project Title"]
        node_hash = hash(node)
        opt += node_hash

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    # err handling  ------------------------------------------------------------
    def test_bad_type(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )

        with pytest.raises(TypeError) as exec_info:
            opt.checkmark(12.5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must be BasePromptNode or hash value: 12.5"

    def test_bad_hash(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )

        with pytest.raises(ValueError) as exec_info:
            opt.checkmark(5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "node absent in prompt corpus tree: 5"

    def test_bad_obj(self, test_corpus1, test_corpus3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        bad_node = test_corpus3.children[0]

        with pytest.raises(ValueError) as exec_info:
            opt.checkmark(bad_node)

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "node absent in prompt corpus tree: PromptCorpusNode(Main Title)"
        )


class Test12:  # ===============================================================

    src = BLUEPRINT_1_PARTIAL_2
    dest = BLUEPRINT_1_FULL

    def test2_checkmark_by_obj(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        print(opt)

        node = test_corpus1["Project Title"]["Description"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test2_checkmark_by_hash(self, test_corpus1):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus1
        )
        print(opt)

        node = test_corpus1["Project Title"]["Description"]
        node_hash = hash(node)
        opt.checkmark(node_hash)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )


# test_prompt2  ################################################################
class Test2:  # ================================================================

    src = BLUEPRINT_2_PARTIAL_1
    dest = BLUEPRINT_2_FULL

    def test1_checkmark_by_obj(self, test_corpus2):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus2
        )
        print(opt)

        proj_node = test_corpus2["Project Title"]
        opt.checkmark(proj_node["Description"]).checkmark(
            proj_node["Usage"]
        ).checkmark(proj_node["License"])

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test1_checkmark_by_hash(self, test_corpus2):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus2
        )
        print(opt)

        proj_node = test_corpus2["Project Title"]
        for h in [
            hash(proj_node[name])
            for name in ("Description", "Usage", "License")
        ]:
            opt.checkmark(h)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )


# test_prompt3  ################################################################
class Test31:  # ===============================================================

    src = BLUEPRINT_3_PARTIAL_1
    dest = BLUEPRINT_3_FULL

    def test1_checkmark_by_obj(self, test_corpus3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus3
        )
        print(opt)

        node = test_corpus3["Main Title"]["Methods"]
        opt.checkmark(node)
        node = node["Data Collection"]
        opt.checkmark(node)
        node = node["Tools Used"]
        opt.checkmark(node)
        node = node["Future Work"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test1_checkmark_by_hash(self, test_corpus3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus3
        )
        print(opt)

        node = test_corpus3["Main Title"]["Methods"]
        opt.checkmark(hash(node))
        node = node["Data Collection"]
        opt.checkmark(hash(node))
        node = node["Tools Used"]
        opt.checkmark(hash(node))
        node = node["Future Work"]
        opt.checkmark(hash(node))

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )


class Test32:  # ===============================================================

    src = BLUEPRINT_3_PARTIAL_2
    dest = BLUEPRINT_3_FULL

    def test2_checkmark_by_obj(self, test_corpus3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus3
        )
        print(opt)

        main_node = test_corpus3["Main Title"]
        node = main_node["Introduction"]
        opt.checkmark(node)
        node = node["Background"]["Importance"]
        opt.checkmark(node)
        node = main_node["Methods"]
        opt.checkmark(node)
        node = node["Data Collection"]["Tools Used"]
        opt.checkmark(node)
        node = main_node["Conclusion"]
        opt.checkmark(node)

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

    def test2_checkmark_by_hash(self, test_corpus3):
        bp_text = self.src
        opt = PromptBlueprint.parse(
            bp_text, disable_prune=True, prompt_corpus_override=test_corpus3
        )
        print(opt)

        main_node = test_corpus3["Main Title"]
        node = main_node["Introduction"]
        opt.checkmark(hash(node))
        node = node["Background"]["Importance"]
        opt.checkmark(hash(node))
        node = main_node["Methods"]
        opt.checkmark(hash(node))
        node = node["Data Collection"]["Tools Used"]
        opt.checkmark(hash(node))
        node = main_node["Conclusion"]
        opt.checkmark(hash(node))

        print("#" * 80)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == self.dest
        )

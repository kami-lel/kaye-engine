from kaye.gen_prompt import get_prompt_tree_root, PromptTreeNode


class TestGetPromptTreeRoot:  # test get_prompt_tree_root()

    def test_type(_):
        root = get_prompt_tree_root()
        assert isinstance(root, PromptTreeNode)

from kaye.gen_prompt import get_prompt_tree_root, PromptTreeNode


class TestGetPromptTreeRoot:  # test get_prompt_tree_root()

    def test_type(_):
        root = get_prompt_tree_root()
        assert isinstance(root, PromptTreeNode)

    def test_chapter1(_):
        cp_name = "Personality"

        root = get_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], PromptTreeNode)

    def test_chapter2(_):
        cp_name = "Conversation"

        root = get_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], PromptTreeNode)

    def test_chapter3(_):
        cp_name = "Format Guidelines"

        root = get_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], PromptTreeNode)

    def test_chapter4(_):
        cp_name = "Role"

        root = get_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], PromptTreeNode)

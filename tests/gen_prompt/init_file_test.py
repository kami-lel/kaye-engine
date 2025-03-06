from kaye.gen_prompt import get_full_prompt_tree_root, FullPromptTreeNode


class TestGetPromptTreeRoot:  # test get_prompt_tree_root()

    def test_type(_):
        root = get_full_prompt_tree_root()
        assert isinstance(root, FullPromptTreeNode)

    def test_chapter1(_):
        cp_name = "Personality"

        root = get_full_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], FullPromptTreeNode)

    def test_chapter2(_):
        cp_name = "Conversation"

        root = get_full_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], FullPromptTreeNode)

    def test_chapter3(_):
        cp_name = "Format Guidelines"

        root = get_full_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], FullPromptTreeNode)

    def test_chapter4(_):
        cp_name = "Role"

        root = get_full_prompt_tree_root()
        assert cp_name in root
        assert isinstance(root[cp_name], FullPromptTreeNode)

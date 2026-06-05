"""
cli-ce-c-structure_test.py

tests for the Python CLI command ``continue`` with creating correct structure
"""

# Pytest unit tests  ###########################################################


class TestMain:

    def test_exits(_, testee_rules_folder):
        assert testee_rules_folder.exists()

    def test_is_dir(_, testee_rules_folder):
        assert testee_rules_folder.is_dir()


class TestAlt:

    def test_exits(_, testee_rules_folder_alt):
        assert testee_rules_folder_alt.exists()

    def test_is_dir(_, testee_rules_folder_alt):
        assert testee_rules_folder_alt.is_dir()

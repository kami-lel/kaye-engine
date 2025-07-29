"""
test function ``get_embedded_prompt_blueprints_names()``
"""

from kaye.gen_prompt import get_embedded_prompt_blueprints_names

# !!! need change with folder prompt_blueprints
EXPECTED_NON_TECH_BLUEPRINTS = [
    "art_tutor",
    "book_body",
    "changelog_writer",
    "commentary_language",
    "conversation_follow_up_generation",
    "conversation_tag_generation",
    "conversation_title_generation",
    "conversation",
    "deutschlehrer",
    "editor",
    "email_secretary",
    "encyclopedic",
    "etiquette_coach",
    "event_search",
    "git_commit_message",
    "kyc",
    "librarian",
    "prompt_writer",
    "tarot_reader",
    "translator",
]


class Test:

    def test_dft(_):
        opt = get_embedded_prompt_blueprints_names()
        print(opt)
        expected = EXPECTED_NON_TECH_BLUEPRINTS + [
            "full",
            "empty",
        ]
        # Assert that both lists contain the same elements regardless of order
        assert set(opt) == set(expected)

    def test_exclude(_):  # exclude tech blueprints
        opt = get_embedded_prompt_blueprints_names(True)
        print(opt)
        # Assert that both lists contain the same elements regardless of order
        assert set(opt) == set(EXPECTED_NON_TECH_BLUEPRINTS)

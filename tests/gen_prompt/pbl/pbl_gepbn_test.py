"""
test function ``get_embedded_prompt_blueprints_names()``
"""

from kaye.gen_prompt import get_embedded_prompt_blueprints_names


class Test:

    # !!! this test change with folder prompt_blueprints
    def test1(_):
        opt = get_embedded_prompt_blueprints_names()
        print(opt)
        expected = [
            "etiquette_coach",
            "code",
            "email_secretary",
            "translator",
            "editor",
            "encyclopedic",
            "conversation_title_generation",
            "deutschlehrer",
            "book_body",
            "librarian",
            "prompt_writer",
            "conversation_tag_generation",
            "conversation",
            "event_search",
            "full",
        ]
        # Assert that both lists contain the same elements regardless of order
        assert set(opt) == set(expected)

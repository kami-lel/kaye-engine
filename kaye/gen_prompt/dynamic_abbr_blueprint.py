from .prompt_blueprint import PromptBlueprint


class DynamicAbbrBlueprint(PromptBlueprint):

    # TODO always/chat abbr type? always provided during chat

    def generate_prompt(self, *, hide_comment=False, query=None):
        content, comment = self._generate_prompt_split_content_and_comment(
            hide_comment
        )

        if query:
            # TODO TODO abbr type (how to interpret the abbr)
            abbr_content = ""
        else:
            abbr_content = ""

        return content + abbr_content + comment

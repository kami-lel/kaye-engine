from .prompt_blueprint import PromptBlueprint


class DynamicAbbrBlueprint(PromptBlueprint):

    def generate_prompt(self, *, hide_comment=False, query=None):
        pass

        # TODO TODO abbr type (how to interpret the abbr)

    # TODO always/chat abbr type? always provided during chat

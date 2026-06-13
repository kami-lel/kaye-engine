"""
blueprint_meta_fields.py

define ``BlueprintMetaFields``
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint


class BlueprintMetaNodes:

    @property
    def description(self):
        return self._convert_node2content(self.description_node)

    @property
    def when_to_use(self):
        return self._convert_node2content(self.when_to_use_node)

    @property
    def description_and_when_to_use(self):
        return self.description + " " + self.when_to_use

    @property
    def globs(self):
        return []

    def __init__(self, main_node=None):
        self.description_node = None
        self.when_to_use_node = None
        self.globs_node = None

        if main_node:
            pass  # TODO

    @staticmethod
    def _convert_node2content(node):
        if not node:
            return ""

        bp = PromptBlueprint.create_from_node(node)
        return bp.generate_prompt(disable_first_heading=True)

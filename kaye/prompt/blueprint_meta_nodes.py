"""
blueprint_meta_fields.py

define ``BlueprintMetaFields``
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint


class BlueprintMetaNodes:  #####################################################

    @property
    def description(self):
        return self._convert_node2content(self.description_node)

    @property
    def when_to_use(self):
        return self._convert_node2content(self.when_to_use_node)

    @property
    def description_and_when_to_use(self):
        return self.description + self._NEWLINE_SYMBOL + self.when_to_use

    @property
    def globs(self):
        return []  # TODO extract globs out

    # constructor  =============================================================

    def __init__(self, *, main_node=None):
        self.description_node = None
        self.when_to_use_node = None
        self.globs_node = None

        if main_node:
            try:
                self.description_node = main_node["{description}"]
            except KeyError:
                pass

            try:
                self.when_to_use_node = main_node["{when_to_use}"]
            except KeyError:
                pass

            try:
                self.globs_node = main_node["{globs}"]
            except KeyError:
                pass

    # helpers  =================================================================

    _NEWLINE_SYMBOL = "↵"

    @classmethod
    def _convert_node2content(cls, node):
        if not node:
            return ""

        bp = PromptBlueprint.create_from_node(node)
        return cls._NEWLINE_SYMBOL.join(
            bp.generate_prompt_lines(disable_first_heading=True)
        )

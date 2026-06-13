"""
blueprint_meta_fields.py

define ``BlueprintMetaFields``
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

# TODO docstrings


class BlueprintMetaNodes:  #####################################################

    @property
    def description(self):
        return self._NEWLINE_SYMBOL.join(
            self._convert_node2content_lines(self.description_node)
        )

    @property
    def when_to_use(self):
        return self._NEWLINE_SYMBOL.join(
            self._convert_node2content_lines(self.when_to_use_node)
        )

    @property
    def description_and_when_to_use(self):
        return self._NEWLINE_SYMBOL.join(
            self._convert_node2content_lines(self.description_node)
            + self._convert_node2content_lines(self.when_to_use_node)
        )

    @property
    def globs(self):
        lines = self._convert_node2content_lines(self.globs_node)

        results = []
        in_block = False

        for line in lines:
            if line == "```glob":
                in_block = True
                continue

            if line == "```" and in_block:
                break

            if in_block:
                results.append(line)

        return results

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

    @staticmethod
    def _convert_node2content_lines(node):
        if not node:
            return []

        bp = PromptBlueprint.create_from_node(node)
        return bp.generate_prompt_lines(disable_first_heading=True)

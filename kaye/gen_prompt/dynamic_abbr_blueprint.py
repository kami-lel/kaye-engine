# pylint: disable=c-extension-no-member

from pathlib import Path
from itertools import chain
import json

import ahocorasick

from .prompt_blueprint import PromptBlueprint

JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"

__all__ = ("DynamicAbbrBlueprint",)


class DynamicAbbrBlueprint(PromptBlueprint):

    _automaton = None

    @classmethod
    def load_abbrs_json(cls):
        if cls._automaton is not None:
            return  # load once, thus skip loading

        cls._automaton = ahocorasick.Automaton()

        # read lines
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:  # read only
            try:
                data = json.load(f)
            except json.JSONDecodeError as err:
                msg = err.args[0]  # improve message
                raise json.JSONDecodeError(
                    msg, err.args[1], err.args[2]
                ) from err

            # TODO load data

    def generate_prompt(
        self, *, hide_comment=False, query=None, add_usable_abbr=False
    ):
        # TODO mpl add usable abbr
        content, comment = self._generate_prompt_split_content_and_comment(
            hide_comment
        )

        self.__class__.load_abbrs_json()

        if query:
            # TODO TODO abbr type (how to interpret the abbr)
            abbr_content = ""
        else:
            abbr_content = ""

        return content + abbr_content + comment

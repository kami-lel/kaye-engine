# pylint: disable=c-extension-no-member

from pathlib import Path
from itertools import chain
import json

import ahocorasick

from .prompt_blueprint import PromptBlueprint

ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"

__all__ = ("DynamicAbbrBlueprint",)


class DynamicAbbrBlueprint(PromptBlueprint):

    _automaton = None

    @classmethod
    def load_abbrs_json(cls, *, abbrs_json_file_path_override=None):
        if cls._automaton is not None:
            return  # load once, thus skip loading

        # init Aho–Corasick automation
        cls._automaton = ahocorasick.Automaton()

        # load abbrs from file to automation
        file_path = abbrs_json_file_path_override or ABBRS_JSON_FILE_PATH
        with open(file_path, "r", encoding="utf-8") as f:  # read only
            try:
                data = json.load(f)
            except json.JSONDecodeError as err:
                raise json.JSONDecodeError(
                    "fail to parse abbrs.json: " + err.msg,
                    err.doc,
                    err.pos,
                ) from err

            if any(key not in data for key in ("abbrs", "alt")):
                pass

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

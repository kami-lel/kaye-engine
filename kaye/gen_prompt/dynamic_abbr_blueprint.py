from pathlib import Path
import ahocorasick
from .prompt_blueprint import PromptBlueprint

JSON_FILE_PATH = Path(__file__).resolve().parent / "abbrs.json"


class DynamicAbbrBlueprint(PromptBlueprint):

    _automaton = None

    @classmethod
    def load_abbrs_json(cls):
        if cls._automaton is not None:
            return  # load once, thus skip loading

        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:  # read only
            lines = f.read()
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
